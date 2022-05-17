import typing

import protobuf_modification

import mitmproxy

class GrpcProtobufContentView(mitmproxy.contentviews.base.View):

    name = "gRPC/Protocol Buffer using protoc"

    supported_content_types = [
        "application/grpc"
    ]
    
    def __init__(self, protobuf_modifier: protobuf_modification.ProtobufModifier) -> None:
       self.protobuf_modifier = protobuf_modifier

    def __call__(
        self,
        data: bytes,
        *,
        content_type: typing.Optional[str] = None,
        flow: typing.Optional[mitmproxy.flow.Flow] = None,
        http_message: typing.Optional[mitmproxy.http.Message] = None,
        **unknown_metadata,
    ):
        deserialized = self.protobuf_modifier.deserialize(http_message, flow.request.path, data)
        return self.name, mitmproxy.contentviews.base.format_text(deserialized)

    def render_priority(self, data: bytes, *, content_type: typing.Optional[str] = None, **metadata) -> float:
        return float(content_type in self.supported_content_types)