from datetime import datetime
from sqlalchemy import DateTime, Float, ForeignKey, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    role: Mapped[str] = mapped_column(String(32), default="candidate")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Resume(Base):
    __tablename__ = "resumes"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    candidate_name: Mapped[str] = mapped_column(String(255), default="Demo Candidate")
    filename: Mapped[str] = mapped_column(String(255))
    raw_text: Mapped[str] = mapped_column(Text)
    parsed: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    analyses: Mapped[list["Analysis"]] = relationship(back_populates="resume")


class Analysis(Base):
    __tablename__ = "analyses"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    resume_id: Mapped[str] = mapped_column(ForeignKey("resumes.id"), index=True)
    job_description: Mapped[str] = mapped_column(Text)
    ats_score: Mapped[float] = mapped_column(Float)
    semantic_match: Mapped[float] = mapped_column(Float)
    readability_score: Mapped[float] = mapped_column(Float)
    result: Mapped[dict] = mapped_column(JSON)
    resume: Mapped[Resume] = relationship(back_populates="analyses")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ResumeVersion(Base):
    __tablename__ = "resume_versions"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    resume_id: Mapped[str] = mapped_column(ForeignKey("resumes.id"), index=True)
    version_number: Mapped[int] = mapped_column()
    content: Mapped[str] = mapped_column(Text)
    ats_score: Mapped[float] = mapped_column(Float)
    diff: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Candidate(Base):
    __tablename__ = "candidates"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(255))
    match: Mapped[float] = mapped_column(Float)
    ats: Mapped[float] = mapped_column(Float)
    skills: Mapped[list[str]] = mapped_column(JSON, default=list)
    risk: Mapped[str] = mapped_column(String(32), default="Low")
