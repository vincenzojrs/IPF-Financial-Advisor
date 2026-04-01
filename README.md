# RAG IPF Wiki 
###### work in progress

At the moment we're writing, the scope of this exercise consists in an Agentic RAG who acts like a professional financial advisor. The Agent is able to retrieve pieces of information from the [subreddit](https://www.reddit.com/r/ItaliaPersonalFinance/) Italian Personal Finance [Wiki](https://www.italiapersonalfinance.it).
The aim is to deliver an industry-grade, production-ready piece of application, which follows all the best practices when it comes to software engineering, coding, data science, and GenAI, from following PEP-8 recomendation, to containeraizing software to ensure reproducibility and isolation, to properly clean data.

We acknowledge there are much more direct solutions to implement some functionalities, such as using an already-built MCP to retrieve data, most of the features (which also include functionalities not strictly necessary for the exercise's purposes, such as abstractions to work in other contexts and error handling) were written *from scratch and entirely by a human*, for learning purposes.

The project was broken down in several pieces:
- Web crawling and data cleaning

<details>
<summary>Architectural choices about web crawling and data cleaning</summary>

## CleanerScraper: a simple, yet powerful, data extraction and cleaning tool

The pipeline started with retriving data and cleaning data to optimize model performance.
TavilyCrawl and TavilyExtract, while initially evaluated, were considered inadequate solutions for several reasons:
- Both tools could have consumed paid API tokens for a relatively simple use case;
- TavilyCrawl returned often a restricted number of links, even after adjusting prompt and parameters;
- TavilyExtract offered limited customization, capping at 20 URLs per batch on the free plan.

Ultimately, TavilyMap was used only to generate a comprehensive sitemap, and the HTML content of the mapped webpages was requested and scraped via the `requests` and `BeautifulSoup` modules.
By looking at the data, I found out the main content of the pages was enclosed in an HTML `<article>` tag, and within that, inside paragraph `<p>` and heading `<h#>` tags. BeautifulSoup was used to keep only relevant content considering the aforementioned criteria.
A `CleanerScraper` class was created, gathering data extraction and cleaning functionalities.

</details>