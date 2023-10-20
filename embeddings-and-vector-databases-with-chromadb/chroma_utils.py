import pathlib

import chromadb
from chromadb.utils import embedding_functions
from more_itertools import batched


def build_chroma_collection(
    chroma_path: pathlib.Path,
    collection_name: str,
    embbeding_func_name: str,
    ids: list[str],
    documents: list[str],
    metadatas: list[dict],
    distance_func_name: str = "cosine",
):
    """Create a ChromaDB collection"""

    chroma_client = chromadb.PersistentClient(chroma_path)

    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=embbeding_func_name
    )

    collection = chroma_client.create_collection(
        name=collection_name,
        embedding_function=embedding_func,
        metadata={"hnsw:space": distance_func_name},
    )

    document_indicies = list(range(len(documents)))

    for batch in batched(document_indicies, 166):
        start_idx = batch[0]
        end_idx = batch[-1]

        collection.add(
            ids=ids[start_idx:end_idx],
            documents=documents[start_idx:end_idx],
            metadatas=metadatas[start_idx:end_idx],
        )
