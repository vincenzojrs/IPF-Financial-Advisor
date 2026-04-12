from src.RAG.CleanerScraper import CleanerScraper
from config import METADATA_SEMANTIC_CHUNKING, WIKI_LINK
from src.RAG.Generator import generate_answer
from src.RAG.HybridRetrieval import HybridRetrieval
from src.RAG.Indexing import create_indexes
from src.RAG.SemanticChunker import SemanticChunker


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


if __name__ == "__main__":
    print("Ciao dal tuo financial advisor pignolazzo!")
    rag = FinancialAdvisorRAG(need_ingestion=False)
    query = "Che cos'è un ETF?"
    result = rag.ask(query)
    print(result)
