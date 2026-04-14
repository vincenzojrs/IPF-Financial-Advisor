# RAG IPF Wiki 
###### work in progress

At the moment we're writing, the scope of this exercise consists in developing an Agentic RAG who acts like a professional financial advisor. The Agent is able to retrieve pieces of information from the [subreddit](https://www.reddit.com/r/ItaliaPersonalFinance/) Italian Personal Finance [Wiki](https://www.italiapersonalfinance.it).
The aim is to deliver an industry-grade, production-ready piece of Python application, which follows all the best practices when it comes to software engineering, coding, data science, and GenAI, from following PEP-8 recomendation, to containeraizing software to ensure reproducibility and isolation, to properly clean data.

While we acknowledge there are much more direct solutions to implement some functionalities, such as using an already-built MCP to retrieve data, most of the features, as well as layers of abstractions and error handling, were included for learning purposes, coded *from scratch and entirely by a human*.

The project was broken down in several pieces:
- Web crawling using `TavilyMap` for sitemap creationg and `BeautifulSoup` for data scraping and cleaning;

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

- Naive semantic chunking using `Numpy`, vectorization using `OpenAI`, and storing in `MongoDB Atlas`;

<details>
<summary>Architectural choices about semantic chunking, embeddingd, and storage</summary>

## Background

Embedding a text consists in translating human language into something that the machine can elaborate. Embedding a piece of human-language information consists in creating numerical representations of words, sentences, or whole paragraphs. Such numerical representations are vectors, consisting in lists of numbers, where each number refers to some semantic features of the word, like genre, number, color, etc.
A common practice before embedding a document consists in dividing the whole text into smaller bits, called "chunks". Embedding sentences or paragraphs rather than individual words allows each vector to incorporate both word-level information and its broader context.
After chunking, the sentences are _translated_ into vectors via an embedding model and usually stored into a vector database.

## Semantic chunking - overkill solution
The Wiki was well organized, and its pages coincise, brief and direct. A semantic chunking approach was immediately recognized to be an overkill solution. However, it was still chosen and coded for educational purposes.
Semantic chunking consists of splitting the original text into chunks using punctuation or line breaks, assuming that each sentences, delimited by a strong punctuation or a line break, carries a complete meaning. The similarity between each a vector and its consecutive one is iteratively calculated, and once it exceeds a certain threshold, a new, bigger chunk is created by aggregation. The goal is therefore to obtain a smaller number of chunks containing mutually coherent information, in order to improve embedding performance.

- A dedicated class called SemanticChunker was created, which splits the corpus and the entire document based on punctuation marks, while preserving useful metadata such as the reference link for each chunk and their identification ID.
- Using an OpenAI embedding model, each chunk was vectorized and, leveraging the NumPy library, the cosine similarity was computed for each pair of consecutive chunks.
- Once the text chunks are created, newer embedding are created and stored in MongoDB Atlas.

</details>

- RAG enhancing: hybrid search using `BM25`, `RRF` for ensambling and reranking using `Cross Encoding`

<details>
<summary>Architectural choices about hybrid search, RRF, and reranking.</summary>

Several techniques were implemnted to improve RAG performance.

One of these involved adopting hybrid search, that is, _ensambling_ the advantages of vector search (VS) - the approach employed so far to retrieve relevant documents based on the semantic meaning encoded in embeddings - with full-text search (FTS), a retrieval method that deems a document relevant according to the occurrence of the query terms within it.

While VS scored relevancy based on cosine similarity, Best Match 25 (BM25) was implemented to calculate similarity scores for FTS. BM25 extends the features of the more popular Tf-IdF algorithm, that scores relevancy of a document based on the occurence of a word within documents in a corpus, and across the whole corpus. Like Tf-IdF, BM25 scores positevely documents where a word occurs most frequently, and scales down the score if the word occurs in many documents. BM25 introduces document length normalization, promoting smaller documents, and term frequency saturation, tweaking the influence of the term frequency in the similarity score.

The two search methods produces two rankings, so an _ensambled_ ranking is created using a Reciprocal Rank Fusion (RRF) algorithm, natively implemented via MongoDBAtlas. RRF combines rankings from two ranks, summing the reciprocals of the ranking for each search method, as well as using a constant. The higher the rank the document has acorss diferrent algorithms, the higher will be in the final ranking.

TOFIX:

Cross encoding is a technique used to return to the LLM only a subset of the most relevant document to enhance retrieval performance. The relevance of each pair of query-document is calculated via a specific

A subgroup of the most relevant documents.

Which are passed through an encoder, a big encoder that is queued to both the referring query and each document.

And queuing both the query and the chi allows us to grasp semantic nuances.

Which otherwise we wouldn't be able to. Through a specific model. We can establish. What are the most relevant N sources for our carpet.

</details>