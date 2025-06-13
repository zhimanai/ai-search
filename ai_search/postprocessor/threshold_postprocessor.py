from typing import List

from llama_index.core.schema import NodeWithScore

from ai_search.postprocessor.base_postprocessor import Postprocessor


class ThresholdPostprocessor(Postprocessor):
    """A postprocessor that filters nodes based on a minimum score threshold.

    This class filters out nodes whose scores fall below a specified threshold value,
    ensuring that only sufficiently relevant results are returned.

    Attributes:
        threshold (float): The minimum score required for a node to be included
            in the results. Nodes with scores <= threshold are filtered out.
    """

    def __init__(self, threshold: float):
        """Initialize the ThresholdPostprocessor with a score threshold.

        Args:
            threshold (float): The minimum score threshold. Only nodes with
                scores greater than this value will be retained.
        """
        self.threshold = threshold

    def postprocess(
        self, query: str, nodes: List[NodeWithScore], *args, **kwargs
    ) -> List[NodeWithScore]:
        """Filter nodes based on the score threshold.

        Args:
            query (str): The search query (not used in filtering, but required
                by the interface).
            nodes (List[NodeWithScore]): List of nodes with scores to be filtered.
            *args: Variable length argument list (unused).
            **kwargs: Arbitrary keyword arguments (unused).

        Returns:
            List[NodeWithScore]: Filtered list containing only nodes with scores
                greater than the threshold.
        """
        return [node for node in nodes if node.score > self.threshold]

    async def apostprocess(
        self, query: str, nodes: List[NodeWithScore], *args, **kwargs
    ) -> List[NodeWithScore]:
        """Asynchronously filter nodes based on the score threshold.

        Args:
            query (str): The search query (not used in filtering, but required
                by the interface).
            nodes (List[NodeWithScore]): List of nodes with scores to be filtered.
            *args: Variable length argument list (unused).
            **kwargs: Arbitrary keyword arguments (unused).

        Returns:
            List[NodeWithScore]: Filtered list containing only nodes with scores
                greater than the threshold.
        """
        return [node for node in nodes if node.score > self.threshold]
