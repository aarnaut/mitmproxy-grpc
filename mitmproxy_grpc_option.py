import typing
import protobuf_modification

import mitmproxy

class GrpcProtobufOptionAddon:

    def __init__(self, protobuf_modifier: protobuf_modification.ProtobufModifier) -> None:
        self.protobuf_modifier = protobuf_modifier

    def load(self, loader):
        loader.add_option(
            name = "descriptor_path",
            typespec = typing.Optional[str],
            default = None,
            help = "Add a descriptor file for serialiation and deserialization of protobuf content",
        )

    def configure(self, updates):
        if ("descriptor_path" in updates and mitmproxy.ctx.options.descriptor_path != None):
            self.protobuf_modifier.set_descriptor_file_path(mitmproxy.ctx.options.descriptor_path)