"""Tests action module.

Note
----
Options to run tests to investigate:
1. Use `live-status` action to run. Results can be parsed with Genie
   parsers or NTC templates. Device credentials, connection settings are
   on NSO. This option is implemented in this example.
2. Use `scrapli` or another framework to connect to the devices
   directly. Need to pass required parameters, including decrypted
   passwords. Results can be parsed with `scrapli` embedded support for
   Genie parsers or NTC templates.
3. Run any external scripts you can imagine. Supply all required
   parameters as env variables or files. It could be pytest jobs, pyATS
   tasks, or even ansible playbook.

cisco-ios-cli-3.8 NED supports a limited number of commands. Newer
versions of IOS NED can run any commands:
>>> any_cmd = device.live_status.ios_stats__exec.any.get_input()
>>> any_cmd.args = ["show version"]
>>> cmd_output = device.live_status.ios_stats__exec.any(any_cmd).result
"""
# pylint:disable=too-many-arguments, protected-access

from typing import Any

import ncs  # type: ignore

# pylint:disable=no-name-in-module
from genie.libs.parser.iosxe import show_platform  # type: ignore
from ncs.dp import Action  # type: ignore

# pylint:enable=no-name-in-module


def check_cmd_result(output: ncs.maagic.ActionParams, cmd_output: str) -> ncs.maagic.ActionParams:
    """Check executed command output.

    Parameters
    ----------
    output : ncs.maagic.ActionParams
        output node
    cmd_output : str
        raw output of the command

    Returns
    -------
    ncs.maagic.ActionParams
        output params with updated status
    """
    if "NETSIM" in cmd_output:
        output.result = True
        output.msg = "Netsim device detected, It's OK, skipping checks."
        return output

    parser = show_platform.ShowVersion(show_platform.ShowVersionSchema)
    show_ver = parser.cli(output=cmd_output)
    if show_ver["version"]["curr_config_register"] == "0x2102":
        output.result = True
        output.msg = "Config register check: PASS"
        return output
    output.result = False
    output.msg = "Config register check: FAILED"
    return output


class PostTestAction(Action):
    """Run post-test."""

    @Action.action
    def cb_action(
        self,
        uinfo: ncs.UserInfo,
        name: str,
        kp: ncs.HKeypathRef,
        a_input: ncs.maagic.ActionParams,
        a_output: ncs.maagic.ActionParams,
        trans: ncs.maapi.Transaction,
    ) -> Any:
        """Execute an action.

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
        Optional[Union[ncs.CONFD_OK, ncs.CONFD_ERR]]
        """
        self.log.info(
            f"{uinfo=}, {name=}, {kp=}, {str(kp)=}, {a_input=}, {str(a_input)=}, "
            f"{a_output=}, {str(a_output)=}, {trans=}",
        )

        with ncs.maapi.single_read_trans("admin", "python") as t:
            root = ncs.maagic.get_root(t)
            print(f"{type(root)=}")
            request = ncs.maagic.get_node(t, kp)
            device = root.devices.device[request._parent.device]
            act_input = device.live_status.ios_stats__exec.show.get_input()
            act_input.args = ["version"]  # 'show version'
            cmd_output = device.live_status.ios_stats__exec.show(act_input).result

        self.log.info(f"{request=}, {str(request)=}")
        self.log.info(f"{request._parent.id=}, {request._parent.device=}")
        self.log.info(f"{cmd_output=}")

        a_output = check_cmd_result(a_output, cmd_output)
        if a_output.result:
            return ncs.CONFD_OK
        return ncs.CONFD_ERR


class PreTestAction(Action):
    """Run pre-test."""

    @Action.action
    def cb_action(
        self,
        uinfo: ncs.UserInfo,
        name: str,
        kp: ncs.HKeypathRef,
        a_input: ncs.maagic.ActionParams,
        a_output: ncs.maagic.ActionParams,
        trans: ncs.maapi.Transaction,
    ) -> Any:
        """Execute an action.

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
        Optional[Union[ncs.CONFD_OK, ncs.CONFD_ERR]]
        """
        self.log.info(
            f"{uinfo=}, {name=}, {kp=}, {str(kp)=}, {a_input=}, {str(a_input)=}, "
            f"{a_output=}, {str(a_output)=}, {trans=}",
        )

        with ncs.maapi.single_read_trans("admin", "python") as t:
            root = ncs.maagic.get_root(t)
            request = ncs.maagic.get_node(t, kp)
            device = root.devices.device[request._parent.device]
            act_input = device.live_status.ios_stats__exec.show.get_input()
            act_input.args = ["version"]  # 'show version'
            cmd_output = device.live_status.ios_stats__exec.show(act_input).result

        self.log.info(f"{request=}, {str(request)=}")
        self.log.info(f"{request._parent.id=}, {request._parent.device=}")
        self.log.info(f"{cmd_output=}")

        a_output = check_cmd_result(a_output, cmd_output)
        if a_output.result:
            return ncs.CONFD_OK
        return ncs.CONFD_ERR
