from abc import ABC, abstractmethod


class Preprocessor(ABC):

    @abstractmethod
    def preprocess(self, query: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def apreprocess(self, query: str) -> str:
        raise NotImplementedError