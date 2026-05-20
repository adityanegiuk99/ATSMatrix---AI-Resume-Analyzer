from fastapi import APIRouter
from app.schemas.resume import InterviewPack, InterviewRequest
from app.services.agents import InterviewAgent

router = APIRouter()


@router.post("/generate", response_model=InterviewPack)
async def generate_interview(request: InterviewRequest) -> InterviewPack:
    return InterviewAgent().generate(request.target_role)
