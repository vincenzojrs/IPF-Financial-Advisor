from CleanerScraper import CleanerScraper


def main():
    print("Hello from financial-advisor!")

    scraper = CleanerScraper("https://www.italiapersonalfinance.it")
    scraper.create_sitemap()
    results = scraper.scrape()

    print()
    print(results[0])
    print()
    print(results[0]["url"])
    print()
    print(results[0]["content"])


if __name__ == "__main__":
    main()
