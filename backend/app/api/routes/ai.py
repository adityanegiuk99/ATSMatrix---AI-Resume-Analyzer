from fastapi import APIRouter
from app.schemas.resume import RewriteRequest, RewriteResponse
from app.services.agents import GrammarAgent

router = APIRouter()


@router.post("/rewrite", response_model=RewriteResponse)
async def rewrite(request: RewriteRequest) -> RewriteResponse:
    return RewriteResponse(rewrites=GrammarAgent().rewrite(request.bullet, request.tone))
