# mitmproxy-grpc

As of now, mitmproxy only supports raw deserialization of protobuf data. `mitmproxy_grpc.py` is an addon that adds descriptor-based gRPC support to mitmproxy. It allows for both serialization and deserialization of protobuf data. The addon uses a descriptor file to resolve gRPC services, methods, and message types.

## Usage
```
mitmproxy -s mitmproxy_grpc.py descriptorFile.proto
```

## Obtaining a descriptor file

You can use the [proto compiler](https://github.com/protocolbuffers/protobuf/releases) to compile a descriptor file out of your proto files. 

`protoc --descriptor_set_out=outputDir protoFiles`

## Viewing content
Once in the single flow view, switch to `google.protobuf` content view. The output will be a deserialized JSON of protobuf content.

## Editing content
Once in the single flow view, use the `:grpc request_body` or `:grpc response_body` to edit the content.

## Limitations
* Compressed protobuf content is not supported.

# License

```
MIT License

Copyright (c) 2021 Ahmed Arnaut

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```