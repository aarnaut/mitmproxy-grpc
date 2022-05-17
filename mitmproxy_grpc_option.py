import typing
import protobuf_modification

import mitmproxy

class GrpcOption:

    def __init__(self, protobuf_modifier: protobuf_modification.ProtobufModifier) -> None:
        self.protobuf_modifier = protobuf_modifier

    def load(self, loader):
        loader.add_option(
            name = "descriptor",
            typespec = typing.Optional[str],
            default = None,
            help = "Set the descriptor file used for serialiation and deserialization of protobuf content",
        )

    def configure(self, updates):
        if ("descriptor" in updates 
            and mitmproxy.ctx.options.__contains__("descriptor")
            and mitmproxy.ctx.options.descriptor is not None
        ):
            self.protobuf_modifier.set_descriptor(mitmproxy.ctx.options.descriptor)