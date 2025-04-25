from langchain_core.tools import tool
from langchain_openai import OpenAI
from langgraph.prebuilt import create_react_agent

from app.utils import get_candidate_details
from app.vector_store import get_retriever


@tool
def resume_retrieval(query: str) -> str:
    """Retrieve and summarize candidate resumes from the Postgres pgvector index."""
    retriever = get_retriever()
    docs = retriever.invoke(query)
    if not docs:
        return "No matching resumes found."
    details = get_candidate_details(docs)
    return f"""
    Position: {details['position']}\n
    Experience: {details['years_experience']}\n
    Skills: {', '.join(details['skills'])}\n
     Summary: {details['summary']}
    """


@tool
def general_knowledge(query: str) -> str:
    """Answer arbitrary general knowledge questions using LLM."""
    llm = OpenAI(temperature=0)
    return llm.invoke(query)


@tool
def calculator(expr: str) -> str:
    """Evaluate a simple arithmetic expression."""
    try:
        return str(eval(expr, {}, {}))
    except Exception:
        return "Error evaluating expression."


tools = [resume_retrieval, general_knowledge, calculator]
agent = create_react_agent(
    model="openai:gpt-3.5-turbo",
    tools=tools,
)
