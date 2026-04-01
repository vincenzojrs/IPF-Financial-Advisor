# RAG IPF Wiki 
###### work in progress

<details>
<summary>Architectural choices about web crawling<summary>

<h2>CleanerScraper: a simple, yet powerful, data extraction and cleaning tool</h2>
The first task of the project consisted in creating a vector database containing all the information related to the Italia Personal Finance Wiki.
TavilyCrawl and TavilyExtract, while initially evaluted, were considered inadequate solutions for several reasons:
- Both tools could have consumed paid API tokens for a relatively simple site_map
- TavilyCrawl returned often restricted number of link, even after adjusting prompt and parameters.
- TavilyExtract offered limited customization, capping at 20URL per batch on free plan.
Ultimetely, TavilyMap was used to generate a cohomprensive sitemap, and mapped webpages were requested and scraped via requests module and BeautifulSoup module.
By looking at the data I found out main content of the pages was enclosed in an HTML <article> tag, and within that, inside paragraph <p> and heading <h#> tags. BeautifulSoup was used to keep only relevant content considering aforementioned criteria.
A CleanerScraper class was created, everything gathering data extraction and cleaning funcitonalities.
</details>