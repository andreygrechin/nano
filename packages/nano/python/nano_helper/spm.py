"""Service progress monitoring."""
# pylint:disable=too-many-arguments

from typing import Any

import ncs  # type: ignore
from ncs.dp import Action  # type: ignore

SPM_POLICY_NAME = "nano-sla-policy"


def update_kicker(root: ncs.maagic.Root) -> None:
    """Create or update a kicker to track timeouts changes.

    Parameters
    ----------
    root : ncs.maagic.Root
        Root object
    """
    kicker = root.kicker__kickers.data_kicker.create("nano-sla-timeouts-kicker")
    kicker.monitor = "/nano:nano/nano:sla/nano:timeouts"
    kicker.kick_node = "/nano:nano/nano:sla"
    kicker.action_name = "init-sla-policy"


def update_spm_policy(root: ncs.maagic.Root) -> None:
    """Create or update SPM policy.

    Parameters
    ----------
    root : ncs.maagic.Root
        Root object
    """
    if SPM_POLICY_NAME not in root.ncs__service_progress_monitoring.policy:
        policy = root.ncs__service_progress_monitoring.policy.create(SPM_POLICY_NAME)
    policy = root.ncs__service_progress_monitoring.policy[SPM_POLICY_NAME]
    # convert from minutes (model) to seconds (SPM policy)
    policy.jeopardy_timeout = root.nano__nano.sla.timeouts.jeopardy * 60
    policy.violation_timeout = root.nano__nano.sla.timeouts.violation * 60
    policy.action.always_call = True
    policy.action.action_path = "/nano:nano/nano:sla/nano:timeouts/nano:timeout"
    if "self-ready" not in policy.condition:
        policy.condition.create("self-ready")
    condition = policy.condition["self-ready"]
    if "self" not in condition.component_type:
        condition.component_type.create("self")
    condition.component_type["self"].status = "reached"
    condition.component_type["self"].plan_state = "ready"
    condition.component_type["self"].what = "all"


class InitSPMAction(Action):
    """Action to create or update SPM policy."""

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
        """Execute the actionpoint.

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
        Path: /nano/sla/init-sla-policy
        """
        self.log.info(f"Actionpoint invoked: {name}")
        with ncs.maapi.single_write_trans(uinfo.username, __name__) as t:
            root = ncs.maagic.get_root(t)
            update_spm_policy(root)
            update_kicker(root)
            t.apply()
        a_output.result = True
        a_output.msg = "OK"
        return ncs.CONFD_OK
