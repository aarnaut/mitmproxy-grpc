# mitmproxy-grpc

As of now, mitmproxy only supports raw deserialization of protobuf data. `mitmproxy_grpc.py` is an addon that adds descriptor-based gRPC support to mitmproxy. It allows for both serialization and deserialization of protobuf data. The addon uses a descriptor file to resolve gRPC services, methods, and message types.

## Usage
```
mitmproxy -s mitmproxy_grpc.py --set descriptor_file=pathToDescriptorFile
```

## Obtaining a descriptor file
You can use the [proto compiler](https://github.com/protocolbuffers/protobuf/releases) to compile a descriptor file out of your proto files. See the `descriptor_set_out` option for more information.

## Viewing content
Once in the single flow view, switch to `google.protobuf` content view. The output will be a deserialized JSON of protobuf content.
Deserialization will only work if the gRPC and message definition are present in the descriptor file.

## Editing content
Once in the single flow view, use the `:grpc request_body` or `:grpc response_body` option to edit the content. Serialization will only work if the gRPC and message definition are present in the descriptor file.

## Limitations
* Compressed protobuf content is not supported.
