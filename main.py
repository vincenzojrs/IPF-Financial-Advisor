from CleanerScraper import CleanerScraper
from SemanticChunker import SemanticChunker

def main():
    print("Hello from financial-advisor!")

    scraper = CleanerScraper("https://www.italiapersonalfinance.it")
    scraper.create_sitemap()
    results = scraper.scrape()

    chunker = SemanticChunker(results, metadata = 'url')
    split_docs = chunker.run(store = False)

if __name__ == "__main__":
    main()
