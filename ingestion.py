import os

from dotenv import load_dotenv
from langchain.tools import tool
from langchain_core.documents import Document
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from langchain_tavily import TavilyExtract, TavilyMap
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymongo import MongoClient

load_dotenv()

url = "https://www.italiapersonalfinance.it"

tavily_map = TavilyMap(
    max_depth=3,
    instructions="Find all blog articles, guides, and educational content pages",
    allow_external=False,
)
site_map = tavily_map.invoke({"url": url})["results"]

tavily_extract = TavilyExtract(
    chunks_per_source=4, extract_depth="basic", include_images=False
)


def chunking(lista: list, n: int):
    for i in range(0, len(lista), n):
        yield lista[i : i + n]


all_docs = []

for batch in chunking(site_map, 20):
    urls = batch
    results = tavily_extract.invoke({"urls": urls})
    for result in results["results"]:
        all_docs.append(
            Document(
                page_content=result["raw_content"], metadata={"source": result["url"]}
            )
        )


text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(all_docs)

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

mongo_client = MongoClient(os.getenv("MONGO_URI"))
collection = mongo_client["FinancialAdvisor"]["chunks"]

vector_store = MongoDBAtlasVectorSearch.from_documents(
    documents=texts,
    collection=collection,
    embedding=embedding_model,
    index_name="vector_index",
)
