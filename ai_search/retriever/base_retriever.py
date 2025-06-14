from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from llama_index.core.schema import Node

from ai_search.model.search_result import SearchResult


class Retriever(ABC):
    # @abstractmethod
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

    # @abstractmethod
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
        raise NotImplementedError()

    # @abstractmethod
    def index(self, document) -> List[Node]:
        raise NotImplementedError()
