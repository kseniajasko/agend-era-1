from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException

from app.resume_processing import (
    extract_candidate_details_llm,
    generate_experience_summary_llm,
)
from app.resume_queries import RESUME_DETAILS_QUERY
from app.schemas import CandidateLLMDetails
from app.utils import get_candidate_details
from app.vector_store import get_retriever

router = APIRouter()


@router.get("/candidate/{candidate_id}/llm_details", response_model=CandidateLLMDetails)
def get_candidate_llm_details(candidate_id: int, retriever=Depends(get_retriever)):
    """
    Retrieves candidate details for a given candidate_id from
    the vector database using the retriever, combines all document texts,
    and then uses LLM to extract structured candidate information:
      - Name
      - Position (job title)
      - Years of experience
      - List of skills
      - A short summary
    """
    docs = retriever.invoke(
        RESUME_DETAILS_QUERY, filter={"author_id": candidate_id}
    )
    if not docs:
        raise HTTPException(
            status_code=404, detail="No documents found for the given candidate_id."
        )
    return get_candidate_details(docs)


@router.get("/candidates/llm_details", response_model=List[CandidateLLMDetails])
def get_all_candidates_llm_details(retriever=Depends(get_retriever)):
    """
    Retrieves LLM-extracted candidate details for all candidates
    in the "resumes" collection using a single query.
    Process:
      - Retrieves all documents from the vector database via the retriever.
      - Groups documents by candidate (author) ID (from metadata).
      - For each candidate, concatenates document texts and uses LLM
        to extract candidate details and generate a summary.
    Returns a list of candidate detail objects.
    """
    retriever.search_kwargs = {"k": 200}
    docs = retriever.invoke(RESUME_DETAILS_QUERY)

    if not docs:
        raise HTTPException(
            status_code=404, detail="No documents found in the database."
        )

    candidates_docs: Dict[int, List] = {}
    for doc in docs:
        candidate_id = doc.metadata.get("author_id")
        if candidate_id is None:
            continue
        candidates_docs.setdefault(candidate_id, []).append(doc)

    candidate_details_list = []
    for doc_list in candidates_docs.values():
        candidate_details = get_candidate_details(doc_list)
        candidate_details_list.append(candidate_details)

    if not candidate_details_list:
        raise HTTPException(
            status_code=404, detail="No candidate details could be extracted."
        )

    return candidate_details_list
