from langchain_openai import ChatOpenAI
from langgraph.types import interrupt
from statistics import mean
from src.tools.rag_tool import FinancialAdvisorRAG
from src.tools.rvb_tool import Comparator
from src.tools.RvB import WebSession

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
        "purchase_price" : interrupt(),
        "sqm" : interrupt(),
        "condo_owner_fees_coeff" : interrupt(),
        "notary_fees" : interrupt(),
        "payback_years" : interrupt(),
        "years_occurring_renovation" : interrupt(),
        "mortgage_interest_rate" : interrupt(),
        "avg_invest_return" : interrupt(),
        "buying_from_individual" : interrupt(),
        "tax_deduction" : interrupt()     
    }
    

    return {"parameters" : user_inputs}

def province_node(state):
    provinces = page.locator("//select[@id = 'pr']").all_inner_texts()[0].split("\n")
    choice = interrupt(provinces)

    page.select_option("//select[@id = 'pr']", label=choice)
    page.click("//input[@id = 'bottone_invio']")
    return {"province": choice}


def municipality_node(state):
    province = state["province"]
    municipalities = (
        page.locator("//select[@id = 'co' and @name = 'co']")
        .all_inner_texts()[0]
        .split("\n")
    )
    choice = interrupt(municipalities)

    page.select_option("//select[@id = 'co' and @name = 'co']", label=choice)
    page.click("//input[@id = 'bottone_invio']")
    return {"municipality": choice}


def zone_and_uses_node(state):
    zones = (
        page.locator("//select[@id = 'linkzonastrada' and @name = 'linkzonastrada']")
        .all_inner_texts()[0]
        .split("\n")
    )
    choice = interrupt(zones)

    page.select_option(
        "//select[@id = 'linkzonastrada' and @name = 'linkzonastrada']", label=choice
    )
    page.click("//input[@id = 'bottone_invio']")

    page.select_option(
        "//select[@id = 'utilizzo' and @name = 'utilizzo']", label="Residenziale"
    )
    page.click("//input[@id = 'bottone_invio']")

    return {"zone": choice}

def extract_parameters(state):
        row = page.locator("tr:has(td:text-is('Abitazioni civili'))").text_content()
        row = row.replace(",", ".").rsplit(" ", maxsplit=7)

        return {"parameters": {
             **state["parameters"],
             "avg_price_sqm": mean([float(row[2]),float(row[3])]),
             "price_to_rent_coeff": mean([float(row[5]),float(row[6])]) / mean([float(row[2]),float(row[3])])
             }
        }

def calculate(state):
        calculator = Comparator(**state["parameters"])
        calculator.calculate_purchasing_expenses()
        calculator.calculating_renting_expenses()

        return {"answer": {
             "Purchasing" : {
                  "purchase_price" : calculator.purchase_price,
                  "price_evaluation" : calculator.is_fair_price(),
                  "fair_price" : calculator.fair_price,
                  "mortgage_fee" : calculator.mortgage_fee,
                  "condo_owner_fee" : calculator.condo_owner_fees,
                  "renovation" : calculator.renovation,
                  "purchasing_expenses" : calculator.purchasing_expenses,
                  "investments_returns" : calculator.investments_returns,
                  "total_net_flow" : calculator.yearly_purchasing_expenses
             },
             "Renting" : {
                  "fair_rent" : calculator.fair_rent,
                  "yearly_fair_rent" : calculator.yearly_rent,
                  "tax_deduction": calculator.tax_deduction,
                  "investments_returns" : calculator.investments_returns,
                  "total_net_flow": calculator.yearly_renting_expenses
             },
             "Summary": {
                  "Convenience" : "purchasing" if calculator.yearly_renting_expenses > calculator.yearly_purchasing_expenses else "renting",
                  "Saving" : abs(calculator.yearly_purchasing_expenses - calculator.yearly_renting_expenses)
             }
        }
        }