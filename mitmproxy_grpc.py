import mitmproxy

import mitmproxy_grpc_content_view as view
import mitmproxy_grpc_command_addon as addon
import protobuf_modification
import protobuf_download

import google.protobuf.descriptor_pool as protobuf_descriptor_pool
import google.protobuf.descriptor_pb2 as protobuf_descriptor_pb2

descriptor_pool = protobuf_download.load_proto_descriptor_pool()
protobuf_modifier = protobuf_modification.ProtobufModifier(descriptor_pool)
view = view.GrpcProtobufView(protobuf_modifier)
addon = addon.GrpcProtobufModifierAddon(protobuf_modifier)

def load(l):
    mitmproxy.contentviews.add(view)

def done():
    mitmproxy.contentviews.remove(view)

addons = [
    addon
]