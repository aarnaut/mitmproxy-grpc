import typing
import protobuf_modification

import mitmproxy

class GrpcProtobufOptionAddon:

    def __init__(self, protobuf_modifier: protobuf_modification.ProtobufModifier) -> None:
        self.protobuf_modifier = protobuf_modifier

    def load(self, loader):
        loader.add_option(
            name = "descriptor_file",
            typespec = typing.Optional[str],
            default = None,
            help = "Set the descriptor file used for serialiation and deserialization of protobuf content",
        )

    def configure(self, updates):
        if ("descriptor_file" in updates and mitmproxy.ctx.options.descriptor_file != None):
            self.protobuf_modifier.set_descriptor_file_path(mitmproxy.ctx.options.descriptor_file)