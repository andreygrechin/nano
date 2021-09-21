"""Webex notification action."""
# pylint:disable=too-many-arguments, protected-access, too-many-locals
import datetime as dt
import json
import re
from os import environ, path
from typing import Any, Optional

import ncs  # type: ignore
from jinja2 import Environment, FileSystemLoader  # type: ignore
from ncs.dp import Action  # type: ignore
from webexteamssdk import WebexTeamsAPI  # type: ignore

SERVICE_KPATH = "/nano:nano/nano{{{}}}"
SERVICE_XPATH = "/nano:nano/nano[id='{}']"
TMPL_SUBFOLDER = "templates"
file_path = path.dirname(path.abspath(__file__))
tmpl_folder = path.join(file_path, TMPL_SUBFOLDER)
j2_env = Environment(
    loader=FileSystemLoader(searchpath=tmpl_folder),
    autoescape=True,
    trim_blocks=True,
)


def _env_var(string: str) -> Optional[str]:
    """Return a value between curly braces, if detect `%ENV{}` pattern.

    Parameters
    ----------
    string: str
        String to check

    Returns
    -------
    Optional[str]
        Return env variable name if the pattern is detected
    """
    if not isinstance(string, str):
        string = str(string)
    pattern = re.compile(r"^%ENV{(?P<env_name>[a-zA-Z0-9]+[a-zA-Z0-9_-]*)}$")
    match = pattern.fullmatch(string)
    return match.group("env_name") if match else None


def _id_from_xpath(string: str) -> Optional[str]:
    """Return a service id from a given xpath string.

    Parameters
    ----------
    string: str
        String to check

    Returns
    -------
    Optional[str]
        Return env variable name if the pattern is detected

    Notes
    -----
    "/nano:nano/nano:nano[nano:id='123']"
    """
    pattern = re.compile(r"/nano:nano/nano:nano\[nano:id='(?P<id>[a-zA-Z0-9_-]+)'\]")
    match = pattern.fullmatch(string)
    return match.group("id") if match else None


def webex_settings() -> dict[str, str]:
    """Return webex settings as a dict.

    Returns
    -------
    dict[str, str]
        a dictionary with webex settings

    Raises
    ------
    ValueError
        In case of missing env variables
    """
    with ncs.maapi.single_read_trans("admin", "python") as t:
        root = ncs.maagic.get_root(t)
        bot_token = root.nano__nano.sla.webex.bot_token
        room_id = root.nano__nano.sla.webex.room_id
    try:
        if env_bot_token := _env_var(bot_token):
            bot_token = environ[env_bot_token]
        if env_room_id := _env_var(room_id):
            room_id = environ[env_room_id]
    except KeyError as err:
        raise ValueError("Error: env variable is not defined.") from err
    return {"bot_token": bot_token, "room_id": room_id}


def get_input_dict(
    uinfo: ncs.UserInfo,
    name: str,
    kp: ncs.HKeypathRef,
    a_input: ncs.maagic.ActionParams,
) -> dict[str, str]:
    """Return a dictionary for given ncs.maagic.ActionParams.

    Parameters
    ----------
    uinfo : ncs.UserInfo
        a UserInfo object
    name : str
        name of the invoked service action
    kp : ncs.HKeypathRef
        service path
    a_input : ncs.maagic.ActionParams
        input node

    Returns
    -------
    dict[str, str]
        a dictionary for given input ncs.maagic.ActionParams
    """
    # convert an input to a dictionary
    params = {elem.split(":")[1]: a_input[elem] for elem in a_input}
    # add known params
    params["name"] = name
    # add extra params from CDB
    with ncs.maapi.single_read_trans("admin", "python") as t:
        _path = ncs.maagic.get_node(t, kp)
    print(f"{_path=}, {str(_path)=}")
    # add service specific params
    if name == "notify-approver":  # notify on a new service
        svc_id = _path._parent.id
        params["id"] = svc_id
    if name == "timeout":  # notify on a broken SLA
        svc_id = _id_from_xpath(a_input.service)
        params["id"] = svc_id
    if name in ["notify-approver", "timeout"]:
        ac_fmt = r"%H:%M %d.%m.%Y"
        spm_fmt = r"%Y-%m-%dT%H:%M:%S+00:00"
        with ncs.maapi.single_read_trans(uinfo.username, __name__) as t:
            svc = ncs.maagic.get_node(t, SERVICE_KPATH.format(svc_id))
            # expected format: 2021-08-19T23:07:01+00:00
            jeopardy = svc.service_progress_monitoring.trigger_status[
                f"nano-spm-{svc_id}"
            ].jeopardy_time
            violation = svc.service_progress_monitoring.trigger_status[
                f"nano-spm-{svc_id}"
            ].violation_time
            params["jeopardy_time"] = dt.datetime.strptime(jeopardy, spm_fmt).strftime(ac_fmt)
            params["violation_time"] = dt.datetime.strptime(violation, spm_fmt).strftime(ac_fmt)
            # other input params for timeout action: policy, service,
            # status, timeout, trigger
    # normalizing to str
    for k, v in params.items():
        if isinstance(v, ncs.maagic.Enum):
            params[k] = str(v)
    return params


class SendMsgAction(Action):
    """Send different types of messages via Webex bot."""

    @Action.action
    def cb_action(
        self,
        uinfo: ncs.UserInfo,
        name: str,
        kp: ncs.HKeypathRef,
        a_input: ncs.maagic.ActionParams,
        a_output: ncs.maagic.ActionParams,
        trans: ncs.maapi.Transaction,
    ) -> Any:  # pylint:disable=no-member
        """Execute the webex bot send action.

        Parameters
        ----------
        uinfo : ncs.UserInfo
            a UserInfo object
        name : str
            the tailf:action name
        kp : ncs.HKeypathRef
            the keypath of the action (HKeypathRef)
        a_input : ncs.maagic.ActionParams
            input node
        a_output : ncs.maagic.ActionParams
            output node
        trans : ncs.maapi.Transaction
            read only transaction, same as action transaction if
            executed with an action context.

        Returns
        -------
        Union[ncs.CONFD_OK, ncs.CONFD_ERR, None]

        Notes
        -----
        You may return a response via the a_output object.
        """
        self.log.info(f"Actionpoint invoked: {name}")
        self.log.info(
            f"{uinfo=}, {name=}, {type(name)=}, {kp=}, {str(kp)=}, {a_input=}, {str(a_input)=}, "
            f"{a_output=}, {str(a_output)=}, {trans=}",
        )

        self.log.debug(f"{tmpl_folder=}")
        md_tmpl = j2_env.get_template(f"{name}.md.j2")
        ac_tmpl = j2_env.get_template(f"{name}-ac.json.j2")

        params = get_input_dict(uinfo, name, kp, a_input)
        self.log.info(f"{params=}")
        msg_md = md_tmpl.render(params)
        msg_ac = ac_tmpl.render(params)
        self.log.debug(f"{msg_md=}")
        self.log.debug(f"{msg_ac=}")

        webex = webex_settings()
        self.log.debug(f"{webex['bot_token'][-10:]=}")
        self.log.debug(f"{webex['room_id'][-10:]=}")

        api = WebexTeamsAPI(access_token=webex["bot_token"])
        api.messages.create(
            roomId=webex["room_id"],
            markdown=f"{msg_md}",
            attachments=json.loads(msg_ac)["attachments"],
        )
        a_output.result = True
        a_output.msg = "OK"
        return ncs.CONFD_OK  # pylint:disable=no-member
