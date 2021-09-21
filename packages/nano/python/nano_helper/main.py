"""Components init module."""
from ncs.application import Application  # type: ignore

from .nano_cb import TemplateCfg
from .spm import InitSPMAction
from .tests import PostTestAction, PreTestAction
from .webex import SendMsgAction


class Init(Application):
    """Manage components."""

    def setup(self):
        """Register callbacks."""
        self.log.info("Main RUNNING")
        self.register_action("send-msg-action", SendMsgAction)
        self.register_action("pre-test-action", PreTestAction)
        self.register_action("post-test-action", PostTestAction)
        self.register_action("init-spm-action", InitSPMAction)
        self.register_nano_service(
            "nano-svcpoint",
            "nano:cfg-com-type",
            "nano:name-server-cfg",
            TemplateCfg,
        )

    def teardown(self):
        """Teardown gracefully."""
        self.log.info("Main FINISHED")
