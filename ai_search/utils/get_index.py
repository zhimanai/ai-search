from uuid import UUID

from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.indices import MultiModalVectorStoreIndex
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.vector_stores.milvus.utils import BaseSparseEmbeddingFunction

from ai_search.config import get_config


# This must be async even though there is no await in the function
# MilvusVectorStore creates an async client but anything that is not
# run in the main thread has no event loop and thus will cause error
async def get_text_store(
    knowledge_base_id: UUID | str,
    top_k: int,
    sparse_embedding_func: BaseSparseEmbeddingFunction,
):
    return MilvusVectorStore(
        uri=f"http://{get_config()['MILVUS_HOST']}:{get_config()['MILVUS_PORT']}",
        collection_name=f"kb_{str(knowledge_base_id).replace('-', '')}_text",
        dim=1024,
        overwrite=False,
        enable_sparse=True,
        hybrid_ranker="RRFRanker",
        hybrid_ranker_params={"k": top_k},
        sparse_embedding_function=sparse_embedding_func,
    )


async def get_text_index(
    knowledge_base_id,
    top_k,
    embedding_model,
    sparse_embedding_func,
):
    return VectorStoreIndex.from_vector_store(
        vector_store=await get_text_store(
            knowledge_base_id, top_k, sparse_embedding_func
        ),
        embed_model=embedding_model,
    )


async def get_image_store(knowledge_base_id, top_k):
    return MilvusVectorStore(
        uri=f"http://{get_config()['MILVUS_HOST']}:{get_config()['MILVUS_PORT']}",
        collection_name=f"kb_{str(knowledge_base_id).replace('-', '')}_image",
        dim=1536,
        overwrite=False,
        enable_sparse=False,
    )


async def get_image_index(knowledge_base_id, top_k, image_embedding_model):
    return VectorStoreIndex.from_vector_store(
        vector_store=await get_image_store(knowledge_base_id, top_k),
        embed_model=image_embedding_model,
    )


async def get_storage_context(
    knowledge_base_id: UUID, top_k: int, sparse_embedding_func
):
    storage_context = StorageContext.from_defaults(
        vector_store=await get_text_store(
            knowledge_base_id, top_k, sparse_embedding_func
        ),
        image_store=await get_image_store(knowledge_base_id, top_k),
    )

    return storage_context


async def get_multi_modal_index(
    knowledge_base_id,
    top_k,
    embedding_model,
    sparse_embedding_func,
    image_embedding_model,
):
    vector_store = await get_text_store(knowledge_base_id, top_k, sparse_embedding_func)

    image_vector_store = await get_image_store(knowledge_base_id, top_k)

    index = MultiModalVectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        image_vector_store=image_vector_store,
        embed_model=embedding_model,
        image_embed_model=image_embedding_model,
    )

    return index
