from dataclasses import dataclass
from uuid import UUID


@dataclass
class SearchResult:
    search_id: UUID
    knowledge_base_id: UUID
    document_id: UUID
    segment_id: UUID
    score: float
