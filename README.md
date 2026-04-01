# RAG IPF Wiki 
###### work in progress

<details>
<summary>Architectural choices about web crawling</summary>

## CleanerScraper: a simple, yet powerful, data extraction and cleaning tool

The first task of the project consisted in creating a vector database containing all the information related to the Italia Personal Finance Wiki.
TavilyCrawl and TavilyExtract, while initially evaluated, were considered inadequate solutions for several reasons:
- Both tools could have consumed paid API tokens for a relatively simple site_map
- TavilyCrawl returned often a restricted number of links, even after adjusting prompt and parameters.
- TavilyExtract offered limited customization, capping at 20 URLs per batch on the free plan.

Ultimately, TavilyMap was used to generate a comprehensive sitemap, and mapped webpages were requested and scraped via the `requests` and `BeautifulSoup` modules.
By looking at the data, I found out the main content of the pages was enclosed in an HTML `<article>` tag, and within that, inside paragraph `<p>` and heading `<h#>` tags. BeautifulSoup was used to keep only relevant content considering the aforementioned criteria.
A `CleanerScraper` class was created, gathering data extraction and cleaning functionalities.

</details>