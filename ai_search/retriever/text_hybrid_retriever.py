import time
from typing import List, Optional
from uuid import UUID

from llama_index.core.schema import Node

from ai_search.logger import logger
from ai_search.model.search_result import SearchResult
from ai_search.retriever.base_retriever import Retriever
from ai_search.utils.get_index import get_text_index


class TextHybridRetriever(Retriever):
    def __init__(self, embedding_model, sparse_embedding_model, image_embedding_model):
        self.embedding_model = embedding_model
        self.sparse_embedding_model = sparse_embedding_model
        self.image_embedding_model = image_embedding_model

    def index(self, document) -> List[Node]:
        pass

    def retrieve(
        self,
        query: str,
        knowledge_base_id: UUID | str,
        top_k: int,
        threshold: Optional[float] = None,
        filters: Optional[dict] = None,
        *args,
        **kwargs,
    ) -> List[SearchResult]:
        raise NotImplementedError()

    async def aretrieve(
        self,
        query: str,
        knowledge_base_id: UUID | str,
        top_k: int,
        threshold: Optional[float] = None,
        filters: Optional[dict] = None,
        *args,
        **kwargs,
    ) -> List[SearchResult]:
        start_time = time.time()
        logger.info(f"Retrival start time: {start_time}")
        index = await get_text_index(
            knowledge_base_id,
            top_k,
            self.embedding_model,
            self.sparse_embedding_model,
        )

        retriever = index.as_retriever(filters=filters, similarity_top_k=top_k)

        retrieved_nodes = await retriever.aretrieve(query)

        retrival_time = time.time()

        end_time = time.time()
        logger.info(
            f"Retrival time: {retrival_time - start_time}, rerank time: {end_time - retrival_time}, total time taken: {end_time - start_time}"
        )

        return retrieved_nodes
