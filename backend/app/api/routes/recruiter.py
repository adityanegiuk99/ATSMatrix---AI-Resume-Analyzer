from fastapi import APIRouter
from app.schemas.resume import CandidateRank

router = APIRouter()


@router.get("/rankings", response_model=list[CandidateRank])
async def rankings() -> list[CandidateRank]:
    return [
        CandidateRank(id="cand_001", name="Aarav Mehta", role="Full-stack AI Engineer", match=92, ats=88, skills=["Next.js", "Python", "RAG"], risk="Low"),
        CandidateRank(id="cand_002", name="Neha Rao", role="Backend Engineer", match=84, ats=81, skills=["FastAPI", "PostgreSQL", "Redis"], risk="Medium"),
        CandidateRank(id="cand_003", name="Kabir Shah", role="Frontend Engineer", match=78, ats=74, skills=["React", "TypeScript", "Charts"], risk="Medium"),
    ]
