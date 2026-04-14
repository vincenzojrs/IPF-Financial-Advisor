from CleanerScraper import CleanerScraper
from SemanticChunker import SemanticChunker


def main():
    print("Hello from financial-advisor!")

    scraper = CleanerScraper("https://www.italiapersonalfinance.it")
    print("\nCreating sitemap\n")
    scraper.create_sitemap()
    print("\nCrawling data\n")
    results = scraper.scrape()

    chunker = SemanticChunker(results, metadata="url")
    print("\nPerforming semantic chunking\n")
    sem_docs = chunker.run()

if __name__ == "__main__":
    main()
