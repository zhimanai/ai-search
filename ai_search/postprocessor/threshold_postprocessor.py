from typing import List

from llama_index.core.schema import NodeWithScore

from ai_search.postprocessor.postprocessor import Postprocessor


class ThresholdPostprocessor(Postprocessor):
    def __init__(self, threshold: float):
        self.threshold = threshold

    def postprocess(
        self, query: str, nodes: List[NodeWithScore], *args, **kwargs
    ) -> List[NodeWithScore]:
        return [node for node in nodes if node.score > self.threshold]

    async def apostprocess(
        self, query: str, nodes: List[NodeWithScore], *args, **kwargs
    ) -> List[NodeWithScore]:
        return [node for node in nodes if node.score > self.threshold]
