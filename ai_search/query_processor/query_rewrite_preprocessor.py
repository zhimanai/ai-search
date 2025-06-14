from llama_index.core.llms import LLM

from ai_search.query_processor.base_query_processor import QueryProcessor


class QueryRewritePreprocessor(QueryProcessor):
    """A query_processor that rewrites queries to be more specific and detailed using an LLM.

    This class uses a language model to automatically enhance user queries by making them
    more specific and detailed, which can improve search results by providing better
    context and clarity.

    Attributes:
        completion_model (LLM): The language model used to rewrite queries.
    """

    def __init__(self, completion_model: LLM):
        """Initialize the QueryRewritePreprocessor with a language model.

        Args:
            completion_model (LLM): The language model instance that will be used
                to rewrite queries.
        """
        self.completion_model = completion_model

    def _get_prompt(self, query: str) -> str:
        """Generate the prompt for query rewriting.

        Args:
            query (str): The original user query to be rewritten.

        Returns:
            str: A formatted prompt instructing the LLM to rewrite the query.
        """
        return f"Rewrite the following query to be more specific and detailed: {query}"

    def preprocess(self, query: str) -> str:
        """Rewrite the query to be more specific and detailed.

        Uses the language model to enhance the original query by making it more
        specific and detailed, which can lead to better search results.

        Args:
            query (str): The original user query to be rewritten.

        Returns:
            str: The rewritten, more specific and detailed version of the query.
        """
        return self.completion_model.complete(self._get_prompt(query)).text

    async def apreprocess(self, query: str) -> str:
        """Asynchronously rewrite the query to be more specific and detailed.

        Uses the language model asynchronously to enhance the original query by
        making it more specific and detailed, which can lead to better search results.

        Args:
            query (str): The original user query to be rewritten.

        Returns:
            str: The rewritten, more specific and detailed version of the query.
        """
        return (await self.completion_model.acomplete(self._get_prompt(query))).text
