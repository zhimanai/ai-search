from llama_index.core.llms import LLM

from ai_search.preprocessor.preprocessor import Preprocessor

class QueryRewritePreprocessor(Preprocessor):
    def __init__(self, completion_model: LLM):
        self.completion_model = completion_model

    def _get_prompt(self, query: str) -> str:
        return f"Rewrite the following query to be more specific and detailed: {query}"

    def preprocess(self, query: str) -> str:
        return self.completion_model.complete(self._get_prompt(query)).text

    async def apreprocess(self, query: str) -> str:
        return (await self.completion_model.acomplete(self._get_prompt(query))).text
