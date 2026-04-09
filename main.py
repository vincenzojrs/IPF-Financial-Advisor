from config import WIKI_LINK, METADATA_SEMANTIC_CHUNKING
from CleanerScraper import CleanerScraper
from SemanticChunker import SemanticChunker


def main():
    print("Hello from financial-advisor!")

    scraper = CleanerScraper(WIKI_LINK)
    print("\nCreating sitemap\n")
    scraper.create_sitemap()
    print("\nCrawling data\n")
    results = scraper.scrape()

    chunker = SemanticChunker(results, metadata=METADATA_SEMANTIC_CHUNKING)
    print("\nPerforming semantic chunking\n")
    sem_docs = chunker.run()

if __name__ == "__main__":
    main()
