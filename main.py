from src.engine.orchestrator import Graph
from langgraph.types import Command

config = {
    "configurable": {
        "thread_id" : 1
    }
}

agent = Graph()
agent.invoke({"query": "Che cos'è un ETF?"}, config=config)

for value in [300000, 80, 0.015, 3000, 20, 10, 0.035, 0.07, True, 0.19]:
    agent.compiled.invoke(Command(resume=value), config=config)
    
agent.compiled.invoke(Command(resume='NAPOLI'), config=config)
result = agent.compiled.invoke(Command(resume='NAPOLI'), config=config)

print(result)