from pydantic import BaseModel, Field


class HeatmapCell(BaseModel):
    section: str
    signal: str
    label: str


class SectionFeedback(BaseModel):
    section: str
    status: str
    feedback: str


class ExtractedResume(BaseModel):
    skills: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    links: list[str] = Field(default_factory=list)


class AnalysisResult(BaseModel):
    resume_id: str
    candidate_name: str
    ats_score: int
    semantic_match: int
    readability_score: int
    missing_keywords: list[str]
    matched_keywords: list[str]
    parsing_failures: list[str]
    section_feedback: list[SectionFeedback]
    heatmap: list[HeatmapCell]
    extracted: ExtractedResume
    recommendations: list[str]


class RewriteRequest(BaseModel):
    bullet: str
    tone: str = "faang"


class RewriteResponse(BaseModel):
    rewrites: list[str]


class InterviewRequest(BaseModel):
    resume_id: str
    target_role: str


class InterviewPack(BaseModel):
    hr: list[str]
    technical: list[str]
    dsa: list[str]
    resume_based: list[str]


class CandidateRank(BaseModel):
    id: str
    name: str
    role: str
    match: int
    ats: int
    skills: list[str]
    risk: str
