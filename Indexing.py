from pymongo import MongoClient
from pymongo.operations import SearchIndexModel

from config import (COLLECTION_NAME, DATABASE_NAME, FTS_INDEX_NAME,
                    FTS_INDEX_TYPE, MONGO_URI, VECTOR_INDEX_NAME,
                    VECTOR_INDEX_NDIM, VECTOR_INDEX_PATH, VECTOR_INDEX_SIM,
                    VECTOR_INDEX_TYPE, VECTOR_INDEX_TYPE_A)


def create_indexes() -> list[SearchIndexModel]:
    """
    A one-off function which creates 2 indexes, a full-text search one, BM25-based, and a vector search one.
    """
    mongo_client = MongoClient(MONGO_URI)
    collection = mongo_client[DATABASE_NAME][COLLECTION_NAME]

    fulltext_index = SearchIndexModel(
        definition={
            "mappings": {
                "dynamic": False,
                "fields": {
                    "text": {"type": "string"},
                    "url": {"type": "string"},
                    "semantic_chunk_id": {"type": "number"},
                },
            }
        },
        name=FTS_INDEX_NAME,
        type=FTS_INDEX_TYPE,
    )

    vector_index = SearchIndexModel(
        definition={
            "fields": [
                {
                    "type": VECTOR_INDEX_TYPE,
                    "path": VECTOR_INDEX_PATH,
                    "numDimensions": VECTOR_INDEX_NDIM,
                    "similarity": VECTOR_INDEX_SIM,
                }
            ]
        },
        name=VECTOR_INDEX_NAME,
        type=VECTOR_INDEX_TYPE_A,
    )

    return collection.create_search_indexes([fulltext_index, vector_index])
