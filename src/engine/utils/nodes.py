from statistics import mean

from langchain_openai import ChatOpenAI
from langgraph.types import interrupt

from src.engine.workflows.rag_tool import FinancialAdvisorRAG
from src.engine.workflows.RvB.WebSession import PlaywrightSession
from src.engine.workflows.rvb_tool import RvBTool

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

    return {"answer": result}


def human_input_node(state):

    user_inputs = {
        "purchase_price": interrupt(""),
        "sqm": interrupt(""),
        "condo_owner_fees_coeff": interrupt(""),
        "notary_fees": interrupt(""),
        "payback_years": interrupt(""),
        "years_occurring_renovation": interrupt(""),
        "mortgage_interest_rate": interrupt(""),
        "avg_invest_return": interrupt(""),
        "buying_from_individual": interrupt(""),
        "tax_deduction": interrupt(""),
    }

    return {"parameters": user_inputs}


def scraping_parameters(state):
    with PlaywrightSession() as page:
        choices = page.locator("//select[@id = 'pr']").all_inner_texts()[0].split("\n")
        province = interrupt("")  # <- ritorna alla UI la variabile choices

        page.select_option("//select[@id = 'pr']", label=province)
        page.click("//input[@id = 'bottone_invio']")

        choices = (
            page.locator("//select[@id = 'co' and @name = 'co']")
            .all_inner_texts()[0]
            .split("\n")
        )
        municipality = interrupt("")  # <- ritorna alla UI la variabile choices

        page.select_option("//select[@id = 'co' and @name = 'co']", label=municipality)
        page.click("//input[@id = 'bottone_invio']")

        # TODO: Enable block below once sent to frontend
        
        # choices = (
        #     page.locator(
        #         "//select[@id = 'linkzonastrada' and @name = 'linkzonastrada']"
        #     )
        #     .all_inner_texts()[0]
        #     .split("\n")
        # )
        # zone = interrupt("")

        page.select_option(
            "//select[@id = 'linkzonastrada' and @name = 'linkzonastrada']", index = 1
        )
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
            "municipality": municipality
            
            # TODO: Enable block below once sent to frontend
            # "zone": zone,
        }


def calculate(state):
    tool = RvBTool(**state["parameters"])
    return { "answer" : tool.analyze() }