from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

from config import OLLAMA_MODEL


class Citation(BaseModel):
    """
    Defining the citation structure
    Example:
        [1]
        CID: 839
        Source Url: https://finance.com/ETF
        Source Text: ...ETF or Exchange Traded Fund consists in financial...
    """

    id: str = Field(description="id of the citation; example: '[1]', '[2]'")
    chunk_id: str = Field(
        description="the id of the chunk the model retrieved information from; example: 'CID: 1'"
    )
    source_url: str = Field(
        description="the url associated to the chunk used in retrieval: found in the metadata of the document; example: 'Source Url: https://google.com'"
    )
    source_text: str = Field(
        description="a brief snippet of the chunk the information was retrieved from; example: 'Source Text: ...text snippet from the chunk..."
    )


class AnswerWithCitations(BaseModel):
    """
    Defining the structure of the answer with citations.
    Example:
        {answer : Exchange Traded Fund is a financial instrument commonly used in personal finance. [1] Bonds are financial instruments consisting in a loan of money. [2]}
        {citations: [1]
        CID: 839
        Source Url: https://finance.com/ETF
        Source Text: ...ETF or Exchange Traded Fund consists in financial...

        [2]
        CID: 213
        Source Url: https://finance.com/Bonds
        Source Text: ...a Bond is certificate issued by a government or a public company promising to repay borrowed money at a fixed rate of interest at a specified time...}
        {has_relevant_info: True}
    """

    answer: str = Field(
        description="provide an answer to the query in italian, using the inline citations in the format of '[1]'; example: The sky is blue [1]"
    )
    citations: list[Citation] = Field(
        description="provide a list citations using the citation output structure."
    )
    has_relevant_info: bool = Field(
        description="True, if you have retrieved relevant information; False if you haven't"
    )


def format_citations(retrieved_docs: list[Document]) -> str:
    retrived_cited_documents = []
    for idx, doc in enumerate(retrieved_docs, start=1):
        cid = doc.metadata.get("semantic_chunk_id", "N/A")
        url = doc.metadata.get("url", "N/A")
        retrived_cited_documents.append(f"""
        \n
        [{idx}]\n
        CID: {cid}\n
        Source Url: {url}\n
        Content: {doc.page_content}\n
        \n
        """)
    return "\n\n".join(retrived_cited_documents)


SYSTEM_PROMPT = """
                    Sei un consulente finanziario esperto che parla in italiano.

                    ISTRUZIONI:
                    - Rispondi solo usando i documenti forniti.
                    - Non inventare informazioni.
                    - Usa citazioni inline come [1], [2].
                    - Se le fonti non bastano, imposta has_relevant_info = false.
                    - Nella lista citations riporta solo le fonti effettivamente usate.
                    """.strip()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "DOMANDA : \n{query}\n\n CONTESTO: \n{cited_docs}"),
    ]
)

llm = ChatOllama(model=OLLAMA_MODEL, temperature=0.3)
citation_chain = prompt | llm.with_structured_output(AnswerWithCitations)

def generate_answer(query: str, docs: list[Document]) -> AnswerWithCitations:
    cited_docs = format_citations(docs)
    return citation_chain.invoke({"query": query, "cited_docs": cited_docs})
