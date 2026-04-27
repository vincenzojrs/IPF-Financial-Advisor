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
    payload = interrupt({"step": "Parametri"})

    return {"parameters": payload}


def scraping_parameters(state):
    with PlaywrightSession() as page:
        choices = page.locator("//select[@id = 'pr']").all_inner_texts()[0].split("\n")
        province = interrupt({"step": "Provincia", "choices": choices})  # <- ritorna alla UI la variabile choices

        page.select_option("//select[@id = 'pr']", label=province)
        page.click("//input[@id = 'bottone_invio']")

        choices = (page.locator("//select[@id = 'co' and @name = 'co']").all_inner_texts()[0].split("\n"))
        municipality = interrupt({"step": "Municipalità", "choices": choices})  # <- ritorna alla UI la variabile choices

        page.select_option("//select[@id = 'co' and @name = 'co']", label=municipality)
        page.click("//input[@id = 'bottone_invio']")
        
        choices = (page.locator("//select[@id = 'linkzonastrada' and @name = 'linkzonastrada']").all_inner_texts()[0].split("\n"))
        zone = interrupt({"step": "Zona", "choices": choices})

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
        Sei un consulente finanziario che parla italiano.
        Riceverai un dizionario contenente:
            - Relativamente allo scenario di acquisto:
                - Costo di acquisto di una casa
                - Valutazione del prezzo, se è più alto, in linea o più basso rispetto al mercato
                - Quale sarebbe il fair price della casa considerando metri quadrati e altre condizioni
                - Rata annuale del mutuo, laddove presente
                - Costi di rinnovamento ammortizzati all'anno
                - Costi di acquisto, spalmati negli anni di mutuo o di rientro dalla spesa
                - Eventuali flussi di cassa positivi derivanti dagli investimenti, laddove presenti
                - Costo annuo netto (flussi positivi + flussi negativi) annui relativi all'acquisto
            - Relativamente allo scenario di affitto
                - Stima dell'affitto mensile di una casa che ha pari condizioni, come zona e metri quadrati
                - Stima dell'affitto annuo
                - Eventuali deduzioni fiscali laddove presenti
                - Eventuali flussi di cassa positivi derivanti dagli investimenti, laddove presenti
                - Costo annuo netto (flussi positivi + flussi negativi) annui relativi all'affitto
            - In sintesi:
                - Quale delle opzioni è più conveniente
                - Quanto si risparmia annualmente
        Crea una sintesi efficace e suggerisci all'utente cosa fare per risparmiare.
        Fornisci una risposta completa e non proporre scenari, calcoli, tabelle, informazioni aggiuntive e non chiedere nulla all'utente.
        Query: {raw_answer}
        """
    )
    return {"answer": refined_answer.content}
    