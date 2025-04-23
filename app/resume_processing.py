import json

from langchain_openai import OpenAI


def extract_candidate_details_llm(full_text: str) -> dict:
    """
    Uses an LLM to extract candidate details from the resume text.
    Expected JSON format:
      {
        "position": "Candidate Position",
        "years_experience": "X years",
        "skills": ["skill1", "skill2", ...]
      }
    """
    prompt = f"""Analyze the following resume and respond _only_ with JSON.
    Include the fields:
      - position: candidate's job title
      - years_experience: number of years of experience
      - skills: list of key skills

    Resume:
    \"\"\"{full_text}\"\"\"

    Respond in this exact JSON format (no extra text):
    {{
      "position": "Position",
      "years_experience": "X",
      "skills": ["Skill1", "Skill2"]
    }}
    """
    llm = OpenAI(temperature=0)  # Deterministic output
    response = llm.invoke(prompt)
    try:
        details = json.loads(response)
    except json.JSONDecodeError:
        details = {
            "position": "Unknown",
            "years_experience": "Not specified",
            "skills": [],
        }
    return details


def generate_experience_summary_llm(full_text: str) -> str:
    """
    Uses an LLM to generate a brief summary
    of the candidate's professional experience,
    key skills, and achievements.
    """
    prompt = f"""Analyze the following resume and generate a brief summary
    of the candidate's professional experience,
    key skills, and achievements.
    The summary should be concise and well-structured.
    Resume:
    \"\"\"{full_text}\"\"\"
    Summary:
    """
    llm = OpenAI(temperature=0)
    summary = llm.invoke(prompt)
    return summary.strip()
