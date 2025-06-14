from typing import List

from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.schema import NodeWithScore

from ai_search.postprocessor.base_postprocessor import Postprocessor


class RerankPostprocessor(Postprocessor):
    """A postprocessor that reranks nodes using a specified reranking model.

    This class wraps a base reranking model to provide postprocessing functionality
    for search results. It delegates the actual reranking logic to the provided
    reranker instance.

    Attributes:
        default_reranker (BaseNodePostprocessor): The underlying reranking model
            used to reorder nodes based on relevance to the query.
    """

    def __init__(self, default_reranker: BaseNodePostprocessor):
        """Initialize the RerankPostprocessor with a reranking model.

        Args:
            default_reranker (BaseNodePostprocessor): The reranking model to use
                for postprocessing nodes.
        """
        self.default_reranker = default_reranker

    def postprocess(
        self, query: str, nodes: List[NodeWithScore], *args, **kwargs
    ) -> List[NodeWithScore]:
        """Rerank nodes based on their relevance to the query.

        Args:
            query (str): The search query used for reranking.
            nodes (List[NodeWithScore]): List of nodes with scores to be reranked.
            *args: Variable length argument list (passed to the reranker).
            **kwargs: Arbitrary keyword arguments (passed to the reranker).

        Returns:
            List[NodeWithScore]: The reranked list of nodes ordered by relevance.
        """
        return self.default_reranker.postprocess_nodes(nodes, query_str=query)

    async def apostprocess(
        self, query: str, nodes: List[NodeWithScore], *args, **kwargs
    ) -> List[NodeWithScore]:
        """Asynchronously rerank nodes based on their relevance to the query.

        Args:
            query (str): The search query used for reranking.
            nodes (List[NodeWithScore]): List of nodes with scores to be reranked.
            *args: Variable length argument list (passed to the reranker).
            **kwargs: Arbitrary keyword arguments (passed to the reranker).

        Returns:
            List[NodeWithScore]: The reranked list of nodes ordered by relevance.
        """
        return await self.default_reranker.apostprocess_nodes(nodes, query_str=query)
