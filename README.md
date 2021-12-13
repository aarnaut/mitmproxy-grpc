# mitmproxy-grpc

As of now, mitmproxy only supports raw deserialization of protobuf content. `mitmproxy_grpc.py` is a small addon that adds descriptor-based gRPC support to mitmproxy. It allows for both serialization and deserialization of protobuf content. 

The addon requires a descriptor file as an input to resolve gRPC services and methods, as well as protobuf message types. Internally, it uses `google.protobuf` package to read the information out of the descriptor file.

## Setup

You will need:
* mitmproxy
* descriptor file of your proto files

## How do I obtain a descriptor file?

You can use the [proto compiler](https://github.com/protocolbuffers/protobuf/releases) to compile a descriptor file out of your proto files. 

`protoc --descriptor_set_out=outputDir --proto_path=pathToDependencies protoFile`

## Usage
---


```
mitmproxy -s mitmproxy_grpc.py descriptorFile
```

where `descriptorFile` points to your local descriptor file. 

## Deserializing protobuf
---
To view deserialized protobuf, switch to the `google.protobuf` content view, once you're viewing a single flow.


## Serializing protobuf
---
To edit and serialize a new protobuf message, intercept the request or response and enter the flow. Once in the flow, use the `grpc request_body` or `grpc response_body` to edit the corresponding body.

The protobuf content will be deserialized into JSON and opened in a text editor. Once you're done editing, the JSON is serialized back into protobuf.
