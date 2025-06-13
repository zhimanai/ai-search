from abc import ABC, abstractmethod
from typing import List

from llama_index.core.schema import NodeWithScore


class Postprocessor(ABC):
    @abstractmethod
    def postprocess(
        self, query: str, nodes: List[NodeWithScore], *args, **kwargs
    ) -> List[NodeWithScore]:
        raise NotImplementedError()

    @abstractmethod
    async def apostprocess(
        self, query: str, nodes: List[NodeWithScore], *args, **kwargs
    ) -> List[NodeWithScore]:
        raise NotImplementedError()
