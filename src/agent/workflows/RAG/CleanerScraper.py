import requests
from bs4 import BeautifulSoup
from langchain_tavily import TavilyMap

from src.config import (ALLOW_EXT_SITEMAP_SCRAPER, ARTICLE_TAG_CLEAN_PAGES,
                        INSTRUCTIONS_SITEMAP_SCRAPER,
                        MAX_DEPTH_SITEMAP_SCRAPER, TAGS_CLEAN_PAGES,
                        TAVILY_API_KEY)


class CleanerScraper:
    """
    The tool to scrape ItaliaPersonalFinance's Wiki.

    Attributes:
        url (str): The url of the website whose pages are to be scraped and cleaned. Defaults to None.
        sitemap (list[str]): If already available, a list of URLs to be scraped. Defaults to None.

    Methods:
        create_sitemap(max_depth, instructions, allow_external):
            Creates a sitemap by crawling the URL provided at instantiation using TavilyMap.
        scrape():
            Extracts and cleans HTML content from each webpage in the sitemap, to preserve relevant content.

    Example:
        scraper = CleanerScraper(url="https://www.italiapersonalfinance.it")
        scraper.create_sitemap(max_depth=3, allow_external=False)
        scraper.scrape()
    """

    def __init__(self, url=None, site_map=None):
        self.url = url
        self.site_map = site_map

    def create_sitemap(
        self,
        max_depth: int = MAX_DEPTH_SITEMAP_SCRAPER,
        instructions: str = INSTRUCTIONS_SITEMAP_SCRAPER,
        allow_external: bool = ALLOW_EXT_SITEMAP_SCRAPER,
    ) -> list[str]:
        """
        Creates a sitemap by crawling the URL provided at instantiation using TavilyMap
        The resulting sitemap is stored in self.site_map and returned
        For more details on TavilyMap, see: https://docs.tavily.com/documentation/api-reference/endpoint/map

        Args:
            max_depth (int): How many levels deep the crawler will follow links. Defaults to 3
            instructions (str) : Natural language instructions for the crawler. When specified, the cost increases to 2 API credits per 10 successful pages instead of 1 API credit per 10 pages. Default to "Find all blog articles, guides, and educational content pages"
            allow_external (bool): Whether to follow links pointing to external domains. Defaults to False

        Returns:
            list[str]: A list of URLs discovered during the crawl, stored in self.site_map

        Example:
            scraper = CleanerScraper(url="https://www.italiapersonalfinance.it")
            sitemap = scraper.create_sitemap(max_depth=3, allow_external=False)
            # sitemap -> ["https://...", "https://...", ...]
        """

        map = TavilyMap(
            max_depth=max_depth,
            instructions=instructions,
            allow_external=allow_external,
            tavily_api_key=TAVILY_API_KEY,
        )

        self.site_map = map.invoke({"url": self.url})["results"]
        return self.site_map

    def _extract_soup_pages(self):
        """
        Extract the HTML content from a list of urls

        Returns:
            list[dict]: A list of dictionaries, where each dictionary contains the HTML content under the "content" key, and the related url under the "url" keyu.

        Example:
            pages_soup = scraper._extract_soup_pages(["https://google.com", "https://repubblica.it"])
            # pages_soup -> [{"content" : "!doctype html><html ...", {"url": https;//google.com}]

        """

        pages_soup = []

        # Iterate over each link in the sitemap
        for url in self.site_map:
            # GET request to link
            page = requests.get(url)
            # Append HTML and related url to a list of soups
            pages_soup.append(
                {"content": BeautifulSoup(page.content, "html.parser"), "url": url}
            )

        return pages_soup

    def _return_cleaned_pages(self, pages_soup: list[dict]) -> list[dict]:
        """
        Clean articles removing unnecessary tags, links, header, and footer, only keeping body. The function works as below:
            - Withing the same page/url check if
                - Article exists, via <article> tag; filter out anything else.
                - In each article, whether paragraph <p> or headings e.g. <h1> tags exists; filter out anything else.
            - If so, store url and relative cleaned content into a dictionary

        It also handles error, in case no articles or tags are found.

        Args:
            pages_soup (list[dict]) : a list of dictionaries, where each dictionary contains a URL under the "url" key, and its related the HTML content under the "content" key.
        Returns:
            list[dict] : a list of dictionaries, where each dictionary contains a URL under the "url" key, and its related human-readble content under the "content" key.

        Example:
            website_clean = scraper._return_cleaned_pages(pages_soup)
            # website_clean -> [{"content" : "Search Images I'm feeling Lucky Google", {"url": https;//google.com}]

        """

        website_clean = []

        for page_soup in pages_soup:

            content = page_soup["content"]
            url = page_soup["url"]
            print(f"Cleaning {url}...")
            articles = content.find_all(ARTICLE_TAG_CLEAN_PAGES)

            if not articles:
                print(f"Skipping {url} because no <article> tag was found!")
                continue

            paragraph = []

            for article in articles:
                for tag in article.find_all(TAGS_CLEAN_PAGES):
                    text = tag.get_text(" ", strip=True)
                    if text:
                        paragraph.append(text)

            if not paragraph:
                print(f"Skipping {url} because no text was found.")
                continue

            website_clean.append({"url": url, "content": "\n\n".join(paragraph)})

        return website_clean

    def scrape(self):
        """
        Combine "_extract_soup_pages" and "_return_cleanded_pages"
        """
        pages_soup = self._extract_soup_pages()
        return self._return_cleaned_pages(pages_soup)
