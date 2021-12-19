import mitmproxy_grpc_content_view as view
import mitmproxy_grpc_command_addon as addon
import mitmproxy_grpc_option as option
import protobuf_modification

import mitmproxy

protobuf_modifier = protobuf_modification.ProtobufModifier()
contentView = view.GrpcProtobufContentView(protobuf_modifier)

def load(loader):
    mitmproxy.contentviews.add(contentView)
   
def done():
    mitmproxy.contentviews.remove(contentView)

addons = [
    option.GrpcProtobufOptionAddon(protobuf_modifier),
    addon.GrpcProtobufModifierAddon(protobuf_modifier),
]