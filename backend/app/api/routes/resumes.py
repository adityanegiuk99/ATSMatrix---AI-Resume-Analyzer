from uuid import uuid4
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.rate_limit import limiter
from app.db.session import get_db
from app.models.entities import Analysis, Resume
from app.schemas.resume import AnalysisResult
from app.services.parser import parse_upload
from app.services.scoring import analyze

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResult)
@limiter.limit("20/minute")
async def analyze_resume(
    request: Request,
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    parsed = await parse_upload(resume)
    resume_id = f"res_{uuid4().hex[:12]}"
    result = analyze(parsed, job_description)
    db_resume = Resume(
        id=resume_id,
        filename=resume.filename or "resume",
        candidate_name=result["candidate_name"],
        raw_text=parsed.raw_text,
        parsed=parsed.as_dict(),
    )
    db_analysis = Analysis(
        id=f"ana_{uuid4().hex[:12]}",
        resume_id=resume_id,
        job_description=job_description,
        ats_score=result["ats_score"],
        semantic_match=result["semantic_match"],
        readability_score=result["readability_score"],
        result=result,
    )
    db.add_all([db_resume, db_analysis])
    await db.commit()
    return AnalysisResult(resume_id=resume_id, **result)
