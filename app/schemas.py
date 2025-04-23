from dataclasses import dataclass
from typing import List


@dataclass
class CandidateLLMDetails:
    position: str
    years_experience: str
    skills: List[str]
    summary: str
