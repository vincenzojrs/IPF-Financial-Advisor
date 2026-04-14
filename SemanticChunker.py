from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class SemanticChunker():
    def __init__(self, texts, metadata:str = None):
        self.docs = [
            Document(
                page_content = doc['content'],
                metadata = {metadata: doc[metadata]}
                )
                for doc in texts
                ]

    def _split_text(self):
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = 400,
            chunk_overlap = 0,
            separators= ["\n\n", "\n", "."],
            is_separator_regex= False
            )
        
        split_docs = splitter.split_documents(self.docs)

        for i, split_doc in enumerate(split_docs):
            split_doc.metadata["chunk_id"] = i

        return split_docs

    def _vectorize_and_store_splits(self, split_docs):
        embedding_model = OpenAIEmbeddings(
            openai_api_key = os.environ.get("OPENAI_API_KEY"),
            model = 'text-embedding-3-small'
            )

        mongo_client = MongoClient(os.getenv("MONGO_URI"))
        collection = mongo_client["Financial_Advisor"]["SplitPreSemChunking"]

        vector_store = MongoDBAtlasVectorSearch.from_documents(
            documents = split_docs,
            embedding = embedding_model,
            collection = collection,
            index_name = "vector_index"

        )

    def run(self, store = True):
        split_docs = self._split_text()

        if store:
            self._vectorize_and_store_splits(split_docs)

        return split_docs



        


        
