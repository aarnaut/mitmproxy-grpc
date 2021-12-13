import typing

import mitmproxy
import mitmproxy.contentviews as contentviews

import protobuf_modification

class GrpcProtobufView(contentviews.base.View):

    name = "google.protobuf"
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
        return "gRPC Protobuf", contentviews.base.format_text(deserialized)

    def render_priority(self, data: bytes, *, content_type: typing.Optional[str] = None, **metadata) -> float:
        # Highest priority if the content type matches
        return float(content_type in self.supported_content_types)