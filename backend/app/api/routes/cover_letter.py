from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter()


class CoverLetterRequest(BaseModel):
    candidate_name: str
    company: str
    role: str
    highlights: list[str]


@router.post("/generate")
async def generate_cover_letter(request: CoverLetterRequest) -> dict[str, str]:
    evidence = "\n".join(f"- {item}" for item in request.highlights[:4])
    letter = f"""Dear {request.company} Hiring Team,

I am excited to apply for the {request.role} role at {request.company}. My background aligns with the role through concrete, measurable work:

{evidence}

I would bring strong product judgment, engineering rigor, and fast learning loops to your team.

Sincerely,
{request.candidate_name}
"""
    return {"format": "markdown", "cover_letter": letter}
