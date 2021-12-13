import google.protobuf.reflection as protobuf_reflection
import google.protobuf.descriptor as protobuf_descriptor
import google.protobuf.json_format as protobuf_json
import google.protobuf.descriptor_pool as protobuf_descriptor_pool
import mitmproxy

class ProtobufModifier:

    def __init__(self, descriptor_pool: protobuf_descriptor_pool.DescriptorPool) -> None:
        self.descriptor_pool = descriptor_pool

    def __find_method_by_path(self, path: str) -> protobuf_descriptor.MethodDescriptor:
        # Drop the first '/' from the path and convert the rest to a fully qualified name space.
        method_path = path.replace('/', '.')[1:]
        return self.descriptor_pool.FindMethodByName(method_path)

    def deserialize(self, http_message: mitmproxy.http.Message, path: str, serialized_protobuf: bytes) -> str:
        grpc_method = self.__find_method_by_path(path)
        # Strip the length and compression prefix; 5 bytes in total. 
        # We don't compress the payload, so we completely ignore the compression bit.   
        data_without_prefix = serialized_protobuf[5:]

        if isinstance(http_message, mitmproxy.http.Request):
            # ParseMessage is deprecated, update to GetPrototype
            message = protobuf_reflection.ParseMessage(grpc_method.input_type, data_without_prefix)
        elif isinstance(http_message, mitmproxy.http.Response):
            message = protobuf_reflection.ParseMessage(grpc_method.output_type, data_without_prefix)
        else:
            raise Exception(f"Unexpected HTTP message type {http_message}")
        
        return protobuf_json.MessageToJson(message=message, descriptor_pool=self.descriptor_pool)

    def serialize(self, http_message: mitmproxy.http.Message, path: str, json: str) -> bytes:
        grpc_method = self.__find_method_by_path(path)

        if isinstance(http_message, mitmproxy.http.Request):
            # Create an empty message to populate
            empty_message = protobuf_reflection.ParseMessage(grpc_method.input_type, b"")
            populated_message = protobuf_json.Parse(
                text=json, 
                message=empty_message,
                ignore_unknown_fields=True, 
                descriptor_pool=self.descriptor_pool) 
        elif isinstance(http_message, mitmproxy.http.Response):
            empty_message = protobuf_reflection.ParseMessage(grpc_method.output_type, b"")
            populated_message = protobuf_json.Parse(  
                text=json, 
                message=empty_message,
                ignore_unknown_fields=True, 
                descriptor_pool=self.descriptor_pool)         
        else:
            raise Exception(f"Unexpected HTTP message type {http_message}")

        serializedMessage = populated_message.SerializeToString()
        # Prepend the length and compression prefix; 5 bytes in total with big endian byte order.
        # We don't support payload compression, so compression bit will always be 0.
        return len(serializedMessage).to_bytes(5, 'big') + serializedMessage