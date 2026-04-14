import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

with open("config.yaml") as f:
    _cfg = yaml.safe_load(f)

# secrets, in .env
MONGO_URI = os.environ["MONGO_URI"]
TAVILY_API_KEY = os.environ["TAVILY_API_KEY"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
CO_API_KEY = os.environ["CO_API_KEY"]

# enviromental variables, in config.yaml
## main.py
WIKI_LINK = _cfg["main"]["wiki_link"]
METADATA_SEMANTIC_CHUNKING = _cfg["main"]["metadata_semantic_chunking"]

## CleanerScraper.py
MAX_DEPTH_SITEMAP_SCRAPER = _cfg["cleaner_scraper"]["create_sitemap"]["max_depth"]
INSTRUCTIONS_SITEMAP_SCRAPER = _cfg["cleaner_scraper"]["create_sitemap"]["instructions"]
ALLOW_EXT_SITEMAP_SCRAPER = _cfg["cleaner_scraper"]["create_sitemap"]["allow_external"]

ARTICLE_TAG_CLEAN_PAGES = _cfg["cleaner_scraper"]["return_cleaned_pages"]["article_tag"]
TAGS_CLEAN_PAGES = _cfg["cleaner_scraper"]["return_cleaned_pages"]["tags"]

## SemanticChunker.py
EMBEDDING_MODEL = _cfg["semantic_chunker"]["embedding_model"]
CHUNK_SIZE_SPLITTER = _cfg["semantic_chunker"]["splitter"]["chunk_size"]
CHUNK_OVLP_SPLITTER = _cfg["semantic_chunker"]["splitter"]["chunk_overlap"]
SEPARATORS_SPLITTER = _cfg["semantic_chunker"]["splitter"]["separators"]
IS_SEP_RGX_SPLITTER = _cfg["semantic_chunker"]["splitter"]["is_separator_regex"]
DATABASE_NAME = _cfg["semantic_chunker"]["database_name"]
COLLECTION_NAME = _cfg["semantic_chunker"]["collection_name"]
VECTOR_STORE_IDX_NAME = _cfg["semantic_chunker"]["vector_store"]["index_name"]
EMBEDDING_KEY = _cfg["semantic_chunker"]["vector_store"]["embedding_key"]
TEXT_KEY = _cfg["semantic_chunker"]["vector_store"]["text_key"]
RELEVANCE_SCORE_FN = _cfg["semantic_chunker"]["vector_store"]["relevance_score_fn"]

## HybridRetrieval.py
COHERE_RERANK_MODEL = _cfg["hybrid_retrieval"]["reranker"]["model"]
SEARCH_INDEX_NAME = _cfg["hybrid_retrieval"]["retriever"]["search_index_name"]
TOP_K = _cfg["hybrid_retrieval"]["retriever"]["top_k"]
FULLTEXT_PENALTY = _cfg["hybrid_retrieval"]["retriever"]["fulltext_penalty"]
VECTOR_PENALTY = _cfg["hybrid_retrieval"]["retriever"]["vector_penalty"]

## Indexing.py
VECTOR_INDEX_TYPE = _cfg["indexing"]["vector_index"]["type"]
VECTOR_INDEX_PATH = _cfg["indexing"]["vector_index"]["path"]
VECTOR_INDEX_NDIM = _cfg["indexing"]["vector_index"]["numDimensions"]
VECTOR_INDEX_SIM = _cfg["indexing"]["vector_index"]["similarity"]
VECTOR_INDEX_NAME = _cfg["indexing"]["vector_index"]["name"]
VECTOR_INDEX_TYPE_A = _cfg["indexing"]["vector_index"]["type_A"]

FTS_INDEX_NAME = _cfg["indexing"]["fulltext_index"]["name"]
FTS_INDEX_TYPE = _cfg["indexing"]["fulltext_index"]["type"]

## Generator.py
# OLLAMA_MODEL = _cfg["generator"]["ollama_model"]
OPENAI_GEN_MODEL = _cfg["generator"]["openai_gen_model"]
