from src.engine.orchestrator import Graph
from langgraph.types import Command

config = {
    "configurable": {
        "thread_id" : 1
    }
}

agent = Graph()
agent.invoke({"query": "Valutiamo insieme un mutuo"}, config=config)

payload = {
    "purchase_price" : 300000,
    "sqm" : 80,
    "condo_owner_fees_coeff" : 0.015,
    "notary_fees" : 3000,
    "payback_years" : 20,
    "years_occurring_renovation" : 10,
    "mortgage_interest_rate" : 0.035,
    "avg_invest_return" : 0.07,
    "buying_from_individual" : 'Privato',
    "tax_deduction" : 0.19
}

agent.compiled.invoke(Command(resume=payload), config=config)
    
agent.compiled.invoke(Command(resume='NAPOLI'), config=config)
result = agent.compiled.invoke(Command(resume='NAPOLI'), config=config)

print(result)