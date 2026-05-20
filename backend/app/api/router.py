from fastapi import APIRouter
from app.api.routes import ai, cover_letter, interviews, recruiter, resumes

api_router = APIRouter()
api_router.include_router(resumes.router, prefix="/resumes", tags=["resumes"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(interviews.router, prefix="/interviews", tags=["interviews"])
api_router.include_router(cover_letter.router, prefix="/cover-letter", tags=["cover-letter"])
api_router.include_router(recruiter.router, prefix="/recruiter", tags=["recruiter"])
