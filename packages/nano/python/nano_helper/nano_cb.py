"""Nano service python callback."""
# pylint:disable=too-many-arguments
import ncs  # type: ignore
from ncs.application import NanoService  # type: ignore
from ncs.template import Template, Variables  # type: ignore


class TemplateCfg(NanoService):
    """Nano service class."""

    @NanoService.create
    def cb_nano_create(
        self,
        tctx: ncs.TransCtxRef,
        root: ncs.maagic.Root,
        service: ncs.maagic.ListElement,
        plan: ncs.maagic.Container,
        component: tuple,
        state: str,
        opaque: list[tuple[str, str]],
        compproplist: list[tuple[str, str]],
    ) -> None:
        """Fill variables into template.

        Parameters
        ----------
        tctx : ncs.TransCtxRef
            transaction context
        root : ncs.maagic.Node
            root node
        service : ncs.maagic.Node
            service node
        plan : ncs.maagic.Node
            Nano plan node
        component : tuple
            plan component active for this invocation
        state : str
            plan component state active for this invocation
        opaque : list[tuple[str, str]]
            properties
        compproplist : list[tuple[str, str]]
            component properties
        """
        self.log.info(
            f"Nano service callback invoked: {service=} {component[0]=} {component[1]=} {state=}"
        )
        self.log.info(
            f"{tctx=}, {root=}, {service=}, {plan=}, {component=}, {state=}, "
            f"{opaque=}, {compproplist=}"
        )
        status = service.plan.component[component].state[state].status.string
        self.log.info(f"State status: {status=}")

        name_server = service.name_server

        t_vars = Variables(
            (
                ("name-server", name_server),
                ("domain-list", "example.com"),
                ("domain-name", "example.com"),
                ("domain-name-lookup", "true"),
            )
        )

        name_server_tmpl = Template(service)
        name_server_tmpl.apply("nano-name-server", t_vars)
