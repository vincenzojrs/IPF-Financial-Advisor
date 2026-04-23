from src.config import METADATA_SEMANTIC_CHUNKING, WIKI_LINK
from src.tools.RAG.CleanerScraper import CleanerScraper
from src.tools.RAG.Generator import generate_answer
from src.tools.RAG.HybridRetrieval import HybridRetrieval
from src.tools.RAG.Indexing import create_indexes
from src.tools.RAG.SemanticChunker import SemanticChunker


class FinancialAdvisorRAG:
    def __init__(self, need_ingestion: bool = False):

        if need_ingestion:
            self.scraper = CleanerScraper(WIKI_LINK)
            self.scraper.create_sitemap()
            result = self.scraper.scrape()
            self.chunker = SemanticChunker(result, metadata=METADATA_SEMANTIC_CHUNKING)
            self.chunker.run()

            create_indexes()

        self.retrieval = HybridRetrieval()

    def ask(self, query):
        docs = self.retrieval.retrieve(query)
        return generate_answer(query, docs)
