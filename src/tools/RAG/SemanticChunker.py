import numpy as np
from langchain_core.documents import Document
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymongo import MongoClient

from src.config import (CHUNK_OVLP_SPLITTER, CHUNK_SIZE_SPLITTER,
                        COLLECTION_NAME, DATABASE_NAME, EMBEDDING_MODEL,
                        IS_SEP_RGX_SPLITTER, MONGO_URI, OPENAI_API_KEY,
                        SEPARATORS_SPLITTER, VECTOR_STORE_IDX_NAME)


class SemanticChunker:
    """
    A naive tool to perform semantic chunking

    Attributes:
        texts (list[dict]): A list of dictionaries containing webpage content and relative url as [{"url": "https://google.com", "content": "Google I'm feeling luck gmail"}, {"url": "https://repubblica.it", "content": "..."}]
        metadata (str): A string containing the other key in the texts dictionaries, than "content". In this specific context, only one metadata key title can be passed and it's "string".

    Methods:

        _split_text(self):
            Split whole corpus into smaller chunks based on line breaks and strong puncutation. Add "chunk_id" metadata for tracing.

        _store_splits(self, chunks, embedding_model, collection_name):
            Open a MongoDB client, create a collection and store embeddings. It is invoked in the run method either before and after semantic chunking.

        _vectorize_splits():
            Extract chunks from Document and create embeddings.

        _cosine_similarity(self, v1, v2):
            Calculate cosine similarity between two vectors.

        _semantic_chunking(self, vectors, list_of_chunks, threshold, max_chunks):
            Perform aggregations among similar, consecutive chunks.

        _merge_semantic_chunks(self, sem_chunks):
            Convert back chunks intto LangChain Documents.

        run(self):
            Perform the above steps.
    """

    def __init__(self, texts: list[dict], metadata: str = None):
        """
        Initializes the SemanticChunker with raw text data and an embedding model.

        Args:
            texts (list[dict]): A list of dictionaries containing webpage content and metadata, e.g. [{"url": "https://google.com", "content": "..."}]. Each dict is converted into a LangChain Document object and stored in self.docs.
            metadata (str, optional): The key in each dict to use as document metadata, other than "content". Defaults to None.

        Attributes:
            docs (list[Document]): LangChain Documents built from texts, each carrying page_content and the specified metadata field.
            embedding_model (OpenAIEmbeddings): Embedding model used to vectorize chunks.

        """
        self.docs = [
            Document(page_content=doc["content"], metadata={metadata: doc[metadata]})
            for doc in texts
        ]
        self.embedding_model = OpenAIEmbeddings(
            openai_api_key=OPENAI_API_KEY,
            model=EMBEDDING_MODEL,
        )

    def _split_text(self) -> list[Document]:
        """
        Split text based using ReceuriveCharacterTextSplitter, based on strong punctuation and line breaks.
        Finally, enumerate the chunk created, and add the index as metadata in "chunk_id".

        Returns:
            list[Document]: A list of LangChain Documents, containing the split texts and their metadata like urls, and chunk_ids.

        Example:
            split_docs = self._split_text()
            # split_docs -> [
                                Document(metadata={'url': 'https://www.italiapersonalfinance.it/blog/assicurazioni',
                                                   'chunk_id': 0},
                                         page_content='...Strumenti assicurativi...'),
                                Document(metadata=...
                            ]
        """
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE_SPLITTER,
            chunk_overlap=CHUNK_OVLP_SPLITTER,
            separators=SEPARATORS_SPLITTER,
            is_separator_regex=IS_SEP_RGX_SPLITTER,
        )

        split_docs = splitter.split_documents(self.docs)

        for i, split_doc in enumerate(split_docs):
            split_doc.metadata["chunk_id"] = i

        return split_docs

    def _store_splits(
        self, chunks: list[Document], embedding_model, collection_name: str
    ):
        """
        Open a MongoDB Client, vectorize the chunks, and embedd their metadata and store them in a newly created collection.

        Args:
            chunks (list[Document]): list of LangChain Documents, containing the split texts and their metadata like urls, and chunk_ids.
            embedding_model (LangChain Embedding Object): refers to an embedding model object instantiation.
            collection_name (str): the name of the newly created collection.

        Example:
            self._store_split(chunks, OpenAIEmbeddings8), "new_collection")
        """

        mongo_client = MongoClient(MONGO_URI)
        collection = mongo_client[DATABASE_NAME][collection_name]

        vector_store = MongoDBAtlasVectorSearch.from_documents(
            documents=chunks,
            embedding=embedding_model,
            collection=collection,
            index_name=VECTOR_STORE_IDX_NAME,
        )

    def _vectorize_splits(self, split_docs: list[Document]):
        """
        Extract texts LangChain Documents and vectorize them.

        Args:
            split_docs (list[Document]): A list of LangChain Documents, containing the split texts and their metadata like urls, and chunk_ids.

        Returns:
            list[Document]: A list of LangChain Documents, containing the split texts and their metadata like urls, and chunk_ids.
            list[list[float]]: List of vectors, one for each text, containg 1536 linguistic features.

        Example:
            split_docs, vectors = self._vectorize_split(split_docs[:2])
            print(len(vectors)) -> # 2
            print(len(vectors[0])) -> # 1536
        """

        chunks = [doc.page_content for doc in split_docs]
        vectors = self.embedding_model.embed_documents(chunks)
        return split_docs, vectors

    def _cosine_similarity(self, v1: list[float], v2: list[float]) -> float:
        """
        Calculate cosine similarity between two vectors: please note that the two 1-D vectors should have the same length.

        Args:
            v1 (list) : The first vector.
            v2 (list) : The second vector.

        Returns:
            float: The cosine similarity between the vectors.

        Example:
            similarity = self._cosine_similarity([3, 2, 0, 5], [1, 0, 0, 0])
            # similarity -> 0.49
        """

        num = np.dot(v1, v2)
        denom = np.linalg.norm(v1) * np.linalg.norm(v2)
        if denom == 0:
            return 0.0
        return num / denom

    def _semantic_chunking(
        self,
        vectors: list[float],
        list_of_chunks: list[Document],
        threshold: float,
        max_chunks: int = 3,
    ):
        """
        Aggregate similar chunks based on relative vectors' similarity.

        Args:
            vectors (list[float]): vectors representing chunks; used to compute similarity between sentences;
            list_of_chunks (list[Document]): chunks - sentences - represented by vectors; aggregated into new, bigger chunks, if similarity exceed a certain threshold;
            threshold (float): used to establish if two chunks should be merged or not;
            max_chunks (int): maximum consecutive chunks to be aggregated.

        Returns:
            list[list[Document]] : contains new aggregated chunk based on semantic chunking.

        Example:
            list_of_chunks = [
                                'dog',
                                'ball',
                                'cat',
                                'lion'
                            ] # where each chunk is a LangChain Document

            vectors = [ [3, 4], [6, 7], [1, 2], [1, 1] ]
            semantic_chunks = self._semantic_chunking = [
                                                            ['dog'],
                                                            ['ball'],
                                                            ['cat', 'lion']
                                                        ]
        """

        chunks = []
        current_chunk = [list_of_chunks[0]]
        for i in range(len(vectors) - 1):
            sim = self._cosine_similarity(vectors[i], vectors[i + 1])
            if sim >= threshold and len(current_chunk) < max_chunks:
                current_chunk.append(list_of_chunks[i + 1])
            else:
                chunks.append(current_chunk)
                current_chunk = [list_of_chunks[i + 1]]
        chunks.append(current_chunk)
        return chunks

    def _merge_semantic_chunks(
        self, sem_chunks: list[list[Document]]
    ) -> list[Document]:

        # TODO: Enable store multiple urls when aggregating different vectors.

        """
        Merges groups of semantically similar Documents into single Documents.

        Each group produced by _semantic_chunking is joined into one Document,
        preserving the URL from the first chunk in the group and assigning a
        new semantic_chunk_id.

        Args:
            sem_chunks (list[list[Document]]): A list of groups, where each group is a list of semantically similar Documents to be merged.
                e.g. [
                    [
                        Document(page_content="Google I'm feeling lucky", metadata={"url": "https://google.com", "chunk_id": 0}),
                        Document(page_content="Gmail inbox outbox spam drafts.", metadata={"url": "https://gmail.com", "chunk_id": 1})
                    ],
                    [
                        Document(page_content="Reddit subreddit Italia Personal Finance Karma", metadata={"url": "https://reddit.com", "chunk_id": 2})
                    ]
                ]

        Returns:
            list[Document]: A flat list of merged Documents, one per group.
                e.g. [
                    Document(
                        page_content="Google I'm feeling lucky Gmail inbox outbox spam drafts",
                        metadata={"semantic_chunk_id": 0, "url": "https://gmail.com"}
                    ),
                    Document(
                        page_content="Reddit subreddit Italia Personal Finance Karma",
                        metadata={"semantic_chunk_id": 1, "url": "https://reddit.com"}
                    )
                ]
        """
        merged = []
        for i, group in enumerate(sem_chunks):
            merged.append(
                Document(
                    page_content=" ".join(doc.page_content for doc in group),
                    metadata={
                        "semantic_chunk_id": i,
                        "url": group[0].metadata.get("url", ""),
                    },
                )
            )
        return merged

    def run(self):
        split_docs = self._split_text()
        self._store_splits(split_docs, self.embedding_model, "PreSemChunking")
        split_docs, vectors = self._vectorize_splits(split_docs)
        sem_chunks = self._semantic_chunking(vectors, split_docs, 0.7)
        sem_docs = self._merge_semantic_chunks(sem_chunks)
        self._store_splits(sem_docs, self.embedding_model, COLLECTION_NAME)
        return sem_docs
