import typing 
import protobuf_modification

import mitmproxy

class GrpcCommand:

    def __init__(self, protobuf_modifier: protobuf_modification.ProtobufModifier) -> None:
        self.protobuf_modifier = protobuf_modifier
    
    @mitmproxy.command.command("grpc.options")
    def edit_focus_options(self) -> typing.Sequence[str]:
        focus_options = [
            "request-body",
            "response-body",
        ]

        return focus_options

    @mitmproxy.command.command("grpc")
    @mitmproxy.command.argument("flow_part", type=mitmproxy.types.Choice("grpc.options"))
    def edit_focus(self, flow_part: str) -> None:    
        request = mitmproxy.ctx.master.view.focus.flow.request
        response = mitmproxy.ctx.master.view.focus.flow.response
        path = request.path

        if flow_part == "request-body":
            content = request.get_content(strict=False) or b""
            http_message = request
        elif flow_part == "response-body":
            content = response.get_content(strict=False) or b""
            http_message = response
        else:
            mitmproxy.ctx.log(f"Unknown option {flow_part}")
            return 

        deserialized_content = self.protobuf_modifier.deserialize(http_message, path, content)
        modifiedContent = mitmproxy.ctx.master.spawn_editor(deserialized_content)

        # Many editors make it hard to save a file without a terminating
        # newline on the last line. When editing message bodies, this can
        # cause problems.
        if mitmproxy.ctx.master.options.console_strip_trailing_newlines:
            modifiedContent = modifiedContent.rstrip(b"\n")

        http_message.content = self.protobuf_modifier.serialize(http_message, path, modifiedContent)