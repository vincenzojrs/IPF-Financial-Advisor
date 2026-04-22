from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_mongodb.retrievers import MongoDBAtlasHybridSearchRetriever
from langchain_openai import OpenAIEmbeddings
from pymongo import MongoClient

from src.config import (CO_API_KEY, COHERE_RERANK_MODEL, COLLECTION_NAME,
                        DATABASE_NAME, EMBEDDING_KEY, EMBEDDING_MODEL,
                        FULLTEXT_PENALTY, MONGO_URI, OPENAI_API_KEY,
                        RELEVANCE_SCORE_FN, SEARCH_INDEX_NAME, TEXT_KEY, TOP_K,
                        VECTOR_PENALTY, VECTOR_STORE_IDX_NAME)


class HybridRetrieval:
    def __init__(self):
        client = MongoClient(MONGO_URI)
        collection = client[DATABASE_NAME][COLLECTION_NAME]

        embeddings = OpenAIEmbeddings(
            openai_api_key=OPENAI_API_KEY, model=EMBEDDING_MODEL
        )

        vector_store = MongoDBAtlasVectorSearch(
            embedding=embeddings,
            collection=collection,
            index_name=VECTOR_STORE_IDX_NAME,
            embedding_key=EMBEDDING_KEY,
            text_key=TEXT_KEY,
            relevance_score_fn=RELEVANCE_SCORE_FN,
        )

        retriever = MongoDBAtlasHybridSearchRetriever(
            vectorstore=vector_store,
            search_index_name=SEARCH_INDEX_NAME,
            top_k=TOP_K,
            fulltext_penalty=FULLTEXT_PENALTY,
            vector_penalty=VECTOR_PENALTY,
        )

        reranker = CohereRerank(model=COHERE_RERANK_MODEL, cohere_api_key=CO_API_KEY)

        self.retriever = ContextualCompressionRetriever(
            base_compressor=reranker, base_retriever=retriever
        )

    def retrieve(self, query: str):
        return self.retriever.invoke(query)
