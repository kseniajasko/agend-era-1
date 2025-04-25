from typing import Any, Dict

from fastapi import APIRouter

from app.react_agent import agent

router = APIRouter()


@router.post("/agent/query")
def run_agent_endpoint(query: str) -> Dict[str, Any]:
    """
    Endpoint that routes user query into the ReAct agent.
    Supports resume_retrieval, calculator, general_knowledge based on prefixes.
    """
    state = {"messages": [{"role": "user", "content": query}]}
    result = agent.invoke(state)
    messages = result.get("messages", [])
    content = messages[-1].content if messages else ""
    return {"response": content}
