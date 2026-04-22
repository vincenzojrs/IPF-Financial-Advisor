# RAG IPF Wiki
 
###### work in progress
 
At the moment we're writing, the scope of this exercise consists in developing a full-stack application in Python, consisting of an Agentic RAG acting like a professional financial advisor. The Agent will be able to retrieve pieces of information from the [subreddit](https://www.reddit.com/r/ItaliaPersonalFinance/) Italian Personal Finance's [Wiki](https://www.italiapersonalfinance.it).
 
The aim is to deliver an industry-grade, production-ready piece of Python application, which follows all the best practices for software engineering, coding, data science, and GenAI — from following PEP-8 recommendations, to containerizing software to ensure reproducibility and isolation, to properly cleaning data.
 
While we acknowledge there are much more direct solutions to implement some functionalities, such as using an already-built MCP to retrieve data, most of the features, as well as layers of abstraction and error handling, were included for learning purposes, coded *from scratch and entirely by a human*, both front-end and back-end.
 
The project was broken down in several pieces:
 
- Data ingestion and cleaning: in the `LangChain` environemnt, web crawling using `TavilyMap` for sitemap creation and `BeautifulSoup` for HTML data scraping;
- RAG implementation: naive semantic chunking using `NumPy`, vectorization using `OpenAI`, and storing in `MongoDB Atlas`;
- RAG enhancing: hybrid search using `BM25`, `RRF` for ensembling and reranking using Cross-Encoding;
- Developing Agentic feature in `LangGraph`: *Rent vs. Buy* using `Selenium` for web page interactions;
- Building a front-end in `Streamlit`, allowing chat history storage between reruns for each user session, as well as citations rendering;
- Local containerization using `Docker`;
- Web hosting using `Google Cloud Platform` and its tools: `Artifact Registry`, `Secret Manager`, and `Google Cloud Run`.
 
 
# Architectural choices about web crawling and data cleaning
 
The pipeline started with retrieving and cleaning data to optimize model performance.
 
`TavilyCrawl` and `TavilyExtract`, while initially evaluated, were considered inadequate solutions for several reasons:
 
- Both tools could have consumed paid API tokens for a relatively simple use case;
- `TavilyCrawl` often returned a restricted number of links, even after adjusting prompt and parameters;
- `TavilyExtract` offered limited customization, capping at 20 URLs per batch on the free plan.
 
Ultimately, `TavilyMap` was used only to generate a comprehensive sitemap, and the HTML content of the mapped webpages was requested and scraped via the `requests` and `BeautifulSoup` modules.
 
By looking at the data, we found that the main content of the pages was enclosed in an HTML `<article>` tag, and within that, inside `<p>` and `<h#>` tags. `BeautifulSoup` was used to keep only relevant content based on the aforementioned criteria.
 
A `CleanerScraper` class was created, gathering data extraction and cleaning functionalities.
 
 
# Architectural choices about semantic chunking, embeddings, and storage
 
Embedding a text consists in translating human language into something that the machine can elaborate. Embedding a piece of human-language information consists in creating numerical representations of words, sentences, or whole paragraphs. Such numerical representations are vectors — lists of numbers where each number refers to some semantic feature of the word, like genre, number, color, etc.
 
A common practice before embedding a document consists in dividing — or *chunking* — the whole text, sometimes referred to as the *corpus*, into smaller bits called *chunks*. Embedding sentences or paragraphs rather than individual words allows each vector to incorporate both word-level information and its broader context.
 
After chunking, the sentences are *translated* into vectors via an embedding model and usually stored in a vector database.
 
## Semantic chunking
 
The Wiki was well organized, and its pages concise, brief and direct. A semantic chunking approach was immediately recognized to be an overkill solution. However, it was still chosen and coded for educational purposes.
 
Semantic chunking consists of splitting the original text into chunks using punctuation or line breaks, assuming that each sentence — delimited by strong punctuation or a line break — carries a complete meaning. The similarity between each vector and its consecutive one was iteratively calculated, and once it exceeded a certain threshold, a new, larger chunk was created by aggregation. The goal was to obtain a smaller number of chunks containing mutually coherent information, in order to improve embedding performance.
 
- A dedicated `SemanticChunker` class was created, which splits the corpus based on punctuation marks while preserving useful metadata such as the reference link for each chunk and their identification ID. The splitter used was a `RecursiveTextSplitter` from `LangChain`.
- Using an `OpenAI` embedding model, each chunk was vectorized and, leveraging the `NumPy` library, the cosine similarity was computed for each pair of consecutive chunks.
- Once the text chunks are created, new embeddings are created and stored in `MongoDB Atlas`.
 
 
# Architectural choices about hybrid search, RRF, and Re-Ranking
 
Several layers of improving RAG performance were implemented: hybrid search, RRF, and reranking.
 
## Hybrid Search using BM25
 
Hybrid search consists of an ensembling method that combines the advantages of vector search (VS) — the approach implemented to find similar vectors using cosine similarity — with full-text search (FTS), a retrieval method that deems a document relevant according to the occurrence of the query terms within it.
 
While VS scores relevancy based on cosine similarity, `Best Match 25` (`BM25`) was implemented to calculate similarity scores for FTS. `BM25` extends the features of the more traditional Tf-IDF algorithm, which scores the relevancy of documents for a query of words based on their occurrence in the corpus. Like `Tf-IDF`, `BM25` positively scores documents where a word occurs most frequently, and scales down the score if the word occurs in many documents. `BM25` introduces document length normalization, promoting smaller documents, and term frequency saturation, tweaking the influence of term frequency in the similarity score.
 
The two search methods produce two rankings, so an ensembled ranking is created using a `Reciprocal Rank Fusion` (`RRF`) algorithm, natively implemented via `MongoDB Atlas`. `RRF` combines rankings from two sources by summing the reciprocals of each document's rank across both methods, weighted by a constant. The higher a document is ranked by different scoring algorithms, the higher it will appear in the final ranking.
 
## Cross-Encoding for Re-Ranking
 
Cross-encoding is a technique used to allow the LLM to retrieve only a subset of the most relevant documents to enhance generation performance. Compared to Bi-Encoder, where query and document vectors are encoded separately and their embeddings compared, cross-encoding encodes both the query and the document within the same transformer, resulting in a similarity score between them. The `Cohere Rerank API` was used to perform this step.
 
# Architectural choices about the first tool realized: *Rent vs. Buy*

In the Italian media, it is common to see people wondering whether to buy a home or pay rent. Here, whilst buying a home usually represents a significant and long-term financial commitment, renting is seen as a waste of money, especially when the rent is higher than a potential mortgage payment.
The tool calculates whether buying a home is more cost-effective than renting, considering several variables:
- Full price paid in cash vs. mortgage;
- Considering alternative investment opportunities;
- Costs of periodic renovation;
- Differences in tax treatment depending on certain typical scenarios recognised under Italian law – such as purchasing from private sellers or from developers.

Additionally, by interacting with the Italian Tax Agency’s website, it is possible to determine whether the property’s price is in line with the market for the same area and what a competitive rent would be for a similar property.

The website interaction was implemented using `Selenium`: a Python library that enables interaction with web pages by identifying their components via their XPATHs, and performing actions such as scrolling, clicking, and selecting from a drop-down menu.

# Architectural choices about LangGraph to orchestrate agentic features:
_TO DO_
 
# Architectural choices about the front-end
 
`Streamlit` was used as the front-end framework, given its simplicity and native chat elements: `chat_message`, which renders a container storing chat history messages, and `chat_input`, which renders a widget handling input prompting.
 
Crucial was the `session_state` functionality in Streamlit: variables that store user-specific data, allowing persistence across reruns for every user session. Each user–system pair of messages was stored in a `session_state` variable that rendered the whole chat history — this solution solved the disappearance of previous chat messages when a new message was prompted.
 
It was one of our first uses of the walrus operator `:=`, as commonly seen in the `Streamlit` documentation, which assigns a value to a variable — in our specific case, the input to the prompt variable — and checks if it is not `None`.
 
The citations, whenever present, were rendered into an `expander` container to increase both credibility and readability.
 
 
# Architectural choices about local deployment in Docker
 
The first local release of the project was packaged using `Docker`. The usage of a local model like `qwen3` would have required the creation and orchestration of multiple containers. However, for the first deployment, we switched to `OpenAI GPT`, cloud-based.
 
A `Dockerfile` created an image from a lightweight Python base with the `uv` package manager installed. The `Dockerfile` exposed port 8080 to reach `Streamlit`, instead of the default 8501, as per the `Google Cloud Run` docs, to make one image compatible with the web hosting environment as well.
 
 
# Architectural choices about web deployment in GCP
 
While possibly subject to changes for future deployments, it was decided to build an image locally and push it to the web.
 
The main steps for web deployment consisted in:
 
- Temporarily allowing web traffic to the `MongoDB Atlas` server so that `Google Cloud Run` can reach it for RAG:
 
```
go to https://cloud.mongodb.com
Security -> Database & Network Access -> Network Access -> IP Access List -> ADD IP ADDRESS (0.0.0.0/0)
```
 
- Storing secrets, like API keys, following the Google documentation about [creating a secret](https://docs.cloud.google.com/secret-manager/docs/creating-and-accessing-secrets#gcloud_1) and [adding a value to a secret](https://docs.cloud.google.com/secret-manager/docs/add-secret-version). Given the small number of secrets, those were entered manually;
- Allowing the developer account to access secrets, following the Google [documentation](https://docs.cloud.google.com/secret-manager/docs/manage-access-to-secrets);
- Pushing the Docker image to `Artifact Registry` following the Google [documentation](https://docs.cloud.google.com/artifact-registry/docs/docker/store-docker-container-images#create);
- Running the container in `Cloud Run`, following this [tutorial](https://medium.com/@ntepp.marcus/deploy-your-side-project-in-minutes-a-beginners-guide-to-google-cloud-run-artifact-registry-f5475240595f).