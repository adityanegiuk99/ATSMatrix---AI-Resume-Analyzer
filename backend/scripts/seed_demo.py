import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings
from app.db.base import Base
from app.models.entities import Candidate, User


async def main() -> None:
    engine = create_async_engine(settings.database_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    Session = async_sessionmaker(engine, expire_on_commit=False)
    async with Session() as session:
        session.add_all([
            User(id="usr_demo_candidate", email="candidate@atsmatrix.dev", role="candidate"),
            User(id="usr_demo_recruiter", email="recruiter@atsmatrix.dev", role="recruiter"),
            Candidate(id="cand_001", name="Aarav Mehta", role="Full-stack AI Engineer", match=92, ats=88, skills=["Next.js", "Python", "RAG"], risk="Low"),
            Candidate(id="cand_002", name="Neha Rao", role="Backend Engineer", match=84, ats=81, skills=["FastAPI", "PostgreSQL", "Redis"], risk="Medium"),
            Candidate(id="cand_003", name="Kabir Shah", role="Frontend Engineer", match=78, ats=74, skills=["React", "TypeScript", "Charts"], risk="Medium"),
        ])
        await session.commit()
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
