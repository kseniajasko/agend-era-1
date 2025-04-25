from fastapi import APIRouter, Depends, HTTPException

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
    docs = retriever.invoke(RESUME_DETAILS_QUERY, filter={"author_id": candidate_id})
    if not docs:
        raise HTTPException(
            status_code=404, detail="No documents found for the given candidate_id."
        )
    data = get_candidate_details(docs)
    details = CandidateLLMDetails(**data)
    return details
