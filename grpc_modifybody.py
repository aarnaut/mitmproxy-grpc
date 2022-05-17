from encodings import utf_8
import re
import typing
from protobuf_modification import ProtobufModifier

from mitmproxy import ctx, exceptions
from mitmproxy.addons.modifyheaders import parse_modify_spec, ModifySpec


class GrpcModifyBody:

    def __init__(self, protobuf_modifier: ProtobufModifier):
        self.replacements: typing.List[ModifySpec] = []
        self.protobuf_modifier = protobuf_modifier

    def load(self, loader):
        loader.add_option(
            "grpc_modify_body", typing.Sequence[str], [],
            """
            Replacement pattern of the form "[/flow-filter]/regex/[@]replacement", where
            the separator can be any character. The @ allows to provide a file path that
            is used to read the replacement string.

            NOTE: regex part is ignored for now. All of content will be replaced.
            """
        )

    def configure(self, updated):
        if "grpc_modify_body" in updated:
            self.replacements = []
            for option in ctx.options.grpc_modify_body:
                try:
                    ctx.log.info(option)
                    spec = parse_modify_spec(option, True)
                except ValueError as e:
                    raise exceptions.OptionsError(f"Cannot parse grpc_modify_body option {option}: {e}") from e

                self.replacements.append(spec)
            
            ctx.log.info(self.replacements)

    def request(self, flow):
        if flow.response or flow.error or not flow.live:
            return
        self.__run(flow)

    def response(self, flow):
        if flow.error or not flow.live:
            return
        self.__run(flow)

    def __run(self, flow):
        for spec in self.replacements:
            if spec.matches(flow):
                try:
                    replacement = spec.read_replacement()
                    modified_replacement = self.__modify_replacement(flow, replacement)
                except OSError as e:
                    ctx.log.warn(f"Could not read replacement file: {e}")
                    continue
                if flow.response:
                    flow.response.content = modified_replacement
                else:
                    flow.request.content = modified_replacement

    def __modify_replacement(self, flow, replacement):
        if flow.response:
            return self.protobuf_modifier.serialize(flow.response, flow.request.path, replacement.decode("utf_8"))
        else:
            return self.protobuf_modifier.serialize(flow.request, flow.request.path, replacement.decode("utf_8"))
