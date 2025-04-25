from app.resume_processing import (
    extract_candidate_details_llm,
    generate_experience_summary_llm,
)


def get_candidate_details(docs: list) -> dict:
    full_text = "\n".join(doc.page_content for doc in docs if doc.page_content)
    details = extract_candidate_details_llm(full_text)
    summary = generate_experience_summary_llm(full_text)
    details["summary"] = summary
    return details
