from statistics import mean

from langchain_openai import ChatOpenAI
from langgraph.types import interrupt

from src.engine.workflows.rag_flow import FinancialAdvisorRAG
from src.engine.workflows.RvB.WebSession import PlaywrightSession
from src.engine.workflows.rvb_flow import RvBTool

llm = ChatOpenAI(model="gpt-5.4-mini")


def router_node(state):
    query = state["query"]
    route = llm.invoke(f"""
        Decide whether this query requires:
        - RAG (Financial information)
        - MUTUO (Mortgage simulation)

        Query: {query}

        Return only RAG or MUTUO
        """).content.strip().lower()

    return {"route": route}


def rag_node(state):
    rag = FinancialAdvisorRAG()
    result = rag.ask(state["query"])

    return {"answer": result.answer}


def human_input_node(state):
    payload = interrupt({"step": "human_input"})

    return {"parameters": payload}


def scraping_parameters(state):
    with PlaywrightSession() as page:
        choices = page.locator("//select[@id = 'pr']").all_inner_texts()[0].split("\n")
        province = interrupt({"step": "provincia", "choices": choices})  # <- ritorna alla UI la variabile choices

        page.select_option("//select[@id = 'pr']", label=province)
        page.click("//input[@id = 'bottone_invio']")

        choices = (page.locator("//select[@id = 'co' and @name = 'co']").all_inner_texts()[0].split("\n"))
        municipality = interrupt({"step": "municipalità", "choices": choices})  # <- ritorna alla UI la variabile choices

        page.select_option("//select[@id = 'co' and @name = 'co']", label=municipality)
        page.click("//input[@id = 'bottone_invio']")
        
        choices = (page.locator("//select[@id = 'linkzonastrada' and @name = 'linkzonastrada']").all_inner_texts()[0].split("\n"))
        zone = interrupt({"step": "zona", "choices": choices})

        page.select_option("//select[@id = 'linkzonastrada' and @name = 'linkzonastrada']", label = zone)
        page.click("//input[@id = 'bottone_invio']")

        page.select_option(
            "//select[@id = 'utilizzo' and @name = 'utilizzo']", label="Residenziale"
        )
        page.click("//input[@id = 'bottone_invio']")

        values = page.get_by_role('row').filter(has = page.get_by_text('Abitazioni civili')).get_by_role('cell').all_inner_texts()
        values = [value.replace(",", ".") for value in values]

        return {
            "parameters": {
                **state["parameters"],
                "avg_price_sqm": mean([float(values[2]), float(values[3])]),
                "price_to_rent_coeff": mean([float(values[5]), float(values[6])])
                / mean([float(values[2]), float(values[3])]),
            },
            "province": province,
            "municipality": municipality,
            "zone": zone,
        }


def calculate(state):
    tool = RvBTool(**state["parameters"])
    return { "answer" : tool.analyze() }

def elaborate(state):
    raw_answer = state["answer"]
    refined_answer = llm.invoke(f"""
        You'll receive a dictionary containing recurring costs about purchasing and renting an house, as well as an assessment, whether which is is more convenient, and how much someone would save.
        Please, craft an effective summary, considering that you're a financial advisor.

        Query: {raw_answer}
        """
    )
    return {"answer": refined_answer.content}
    