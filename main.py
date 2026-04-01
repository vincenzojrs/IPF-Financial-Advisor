from CleanerScraper import CleanerScraper

def main():
    print("Hello from financial-advisor!")

    scraper = CleanerScraper("https://www.italiapersonalfinance.it")
    scraper.create_sitemap()
    results = scraper.scrape()

if __name__ == "__main__":
    main()
