# RAG IPF Wiki 
###### work in progress

At the moment we're writing, the scope of this exercise consists in developing an Agentic RAG who acts like a professional financial advisor. The Agent is able to retrieve pieces of information from the [subreddit](https://www.reddit.com/r/ItaliaPersonalFinance/) Italian Personal Finance [Wiki](https://www.italiapersonalfinance.it).
The aim is to deliver an industry-grade, production-ready piece of Python application, which follows all the best practices when it comes to software engineering, coding, data science, and GenAI, from following PEP-8 recomendation, to containeraizing software to ensure reproducibility and isolation, to properly clean data.

While we acknowledge there are much more direct solutions to implement some functionalities, such as using an already-built MCP to retrieve data, most of the features, as well as layers of abstractions and error handling, were included for learning purposes, coded *from scratch and entirely by a human*.

The project was broken down in several pieces:
- Web crawling using `TavilyMap` for sitemap creationg and `BeautifulSoup` for data scraping and cleaning;
- Naive semantic chunking using `Numpy`, vectorization using `OpenAI`, and storing in  `MongoDB Atlas`;


<details>
<summary>Architectural choices about web crawling and data cleaning</summary>

## CleanerScraper: a simple, yet powerful, data extraction and cleaning tool

The pipeline started with retriving data and cleaning data to optimize model performance.
`TavilyCrawl` and `TavilyExtract`, while initially evaluated, were considered inadequate solutions for several reasons:
- Both tools could have consumed paid API tokens for a relatively simple use case;
- `TavilyCrawl` returned often a restricted number of links, even after adjusting prompt and parameters;
- `TavilyExtract` offered limited customization, capping at 20 URLs per batch on the free plan.

Ultimately, `TavilyMap` was used only to generate a comprehensive sitemap, and the HTML content of the mapped webpages was requested and scraped via the `requests` and `BeautifulSoup` modules.
By looking at the data, I found out the main content of the pages was enclosed in an HTML `<article>` tag, and within that, inside paragraph `<p>` and heading `<h#>` tags. BeautifulSoup was used to keep only relevant content considering the aforementioned criteria.
A `CleanerScraper` class was created, gathering data extraction and cleaning functionalities.

</details>

<details>
<summary>Architectural choices about semantic chunking, embeddingd, and storage</summary>

## Naive semantic chunker

Embedding a text consists in translating human language into something that the machine can elaborate. Embedding a piece of human-language information consists in creating a numerical representation of words, sentences, or whole paragraphs. Such numerical representation is a vector, consisting in a list of numbers, each referring to some linguistic features of the word, like genre, number, color, etc.
A common practice before embedding a document consists in dividing the whole text into smaller bits, called "chunks". While it would be possible to embed single words, embedding whole sentences or paragraph allow incorporating in the numerical representation of a word, also information related to its context. 

The Wiki was well organized, and its pages coincise, brief and direct. A semantic chunking approach was immediately recognized to be an overkill solution. However, it was still chosen and coded for educational purposes.
A semantic chunking approach was chosen to create the Wiki chunks and subsequently vectorize them.
This was done exclusively for educational purposes: the Wiki was already well-organized and the language used was very concise and direct, to allow immediate understanding for those consulting it. Nevertheless, it was decided to implement the semantic chunking approach for study purposes.
Semantic chunking consists of splitting the original text into chunks using punctuation or line breaks, since it is assumed that each sentence delimited in this way carries a complete meaning. The similarity between each pair of consecutive chunks is then calculated, and a new chunk is created by aggregating consecutive ones whose similarity exceeds a certain threshold. The goal is therefore to obtain a smaller number of chunks containing mutually coherent information, in order to improve embedding performance.
For this reason, no existing library was used; instead, the functions were written from scratch. A dedicated class called SemanticChunker was created, which splits the corpus and the entire document based on punctuation marks, while preserving useful metadata such as the reference link for each chunk and their identification ID.
Using an OpenAI embedding model, each chunk was vectorized and, leveraging the NumPy library, the cosine similarity was computed for each pair of consecutive chunks. Whenever the similarity exceeded an empirically established threshold, the two chunks were merged into one.
The process is iterative: the aggregation of multiple chunks terminates when one of two conditions is met — either the maximum number of aggregated chunks is reached, or the similarity drops below the established threshold.
Also for computational optimization purposes, a dedicated vector collection was created on MongoDB Atlas, so that embeddings would not need to be recalculated every time. At the end of the semantic chunking process, the embeddings to be used for RAG purposes are recalculated.

</details>