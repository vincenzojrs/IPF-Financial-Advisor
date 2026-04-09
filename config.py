import os
import yaml
from dotenv import load_dotenv

load_dotenv()

with open('config.yaml') as f:
    _cfg = yaml.safe_load(f)

# secrets, in .env
MONGO_URI = os.environ["MONGO_URI"]
TAVILY_API_KEY = os.environ["TAVILY_API_KEY"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

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
VECTOR_STORE_IDX_NAME = _cfg["semantic_chunker"]["vector_store"]["index_name"]






