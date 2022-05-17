from mitmproxy_grpc_command import GrpcCommand
import mitmproxy_grpc_content_view as view
from mitmproxy_grpc_option import GrpcOption
import protobuf_modification

import mitmproxy

protobuf_modifier = protobuf_modification.ProtobufModifier()
contentView = view.GrpcProtobufContentView(protobuf_modifier)

def load(loader):
    mitmproxy.contentviews.add(contentView)
   
def done():
    mitmproxy.contentviews.remove(contentView)

addons = [
    GrpcOption(protobuf_modifier),
    GrpcCommand(protobuf_modifier),
]