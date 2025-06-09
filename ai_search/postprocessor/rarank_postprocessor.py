from typing import List

from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.schema import NodeWithScore

from ai_search.postprocessor.postprocessor import Postprocessor


class RerankPostprocessor(Postprocessor):
    def __init__(self, default_reranker: BaseNodePostprocessor):
        self.default_reranker = default_reranker

    def postprocess(
        self, query: str, nodes: List[NodeWithScore], *args, **kwargs
    ) -> List[NodeWithScore]:
        return self.default_reranker.postprocess_nodes(nodes, query_str=query)

    async def apostprocess(
        self, query: str, nodes: List[NodeWithScore], *args, **kwargs
    ) -> List[NodeWithScore]:
        return await self.default_reranker.apostprocess_nodes(nodes, query_str=query)
