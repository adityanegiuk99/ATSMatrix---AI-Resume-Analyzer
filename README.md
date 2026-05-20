# ATSMatrix

ATSMatrix is a production-oriented AI Resume Analyzer and Career Intelligence Platform. It includes a Next.js 15 SaaS UI, FastAPI backend, PostgreSQL data model, Redis queue, Chroma vector store wiring, AI agent services, ATS parsing simulation, semantic job matching, recruiter ranking, and Docker deployment.

## Architecture

- `app/`, `components/`, `lib/`: Next.js 15, TypeScript, TailwindCSS, ShadCN-style primitives, Framer Motion, responsive dashboard.
- `backend/app/api`: API-first FastAPI routes for resume analysis, AI rewrite, interviews, cover letters, and recruiter workflows.
- `backend/app/services`: parser, scoring engine, vector store adapter, and multi-agent services.
- `backend/app/models`: SQLAlchemy entities for users, resumes, analyses, versions, and candidates.
- `backend/migrations`: Alembic schema migration.
- `docker-compose.yml`: frontend, API, worker, Postgres, Redis, and Chroma.

## Core Capabilities

- PDF/DOCX resume upload and structured parsing.
- Skill, education, project, experience, and link extraction.
- ATS score with keyword, section, readability, and formatting signals.
- ATS simulator for tables, columns, decorative bullets/icons, and short extraction failures.
- Semantic job matching using a deterministic local scorer, with ChromaDB adapter ready for embeddings/RAG.
- AI resume bullet rewriting across Fresher, FAANG, Startup, and Senior Engineer tones.
- Interview generation for HR, technical, DSA, and resume-based rounds.
- Cover letter generation endpoint.
- Recruiter dashboard with candidate ranking, skills, risk, and match scores.
- Resume history/versioning schema for before/after score diffs.
- Rate limiting, CORS, structured logging, Prometheus metrics, async DB access, and queue worker.

## Local Setup

1. Copy environment values:

```bash
cp .env.example .env
```

2. Start the full stack:

```bash
docker compose up --build
```

3. Seed demo records:

```bash
docker compose exec api python scripts/seed_demo.py
```

4. Open the app:

```text
http://localhost:3000
```

The API is available at `http://localhost:8000`, metrics at `http://localhost:8000/metrics`, and Chroma at `http://localhost:8001`.

## Development Without Docker

Frontend:

```bash
npm install
npm run dev
```

Backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL`: frontend API target.
- `DATABASE_URL`: async SQLAlchemy Postgres URL.
- `REDIS_URL`: queue and cache URL.
- `CHROMA_HOST`, `CHROMA_PORT`: vector database endpoint.
- `OPENAI_API_KEY`, `GEMINI_API_KEY`: optional AI provider keys for replacing deterministic local agents.
- `CLERK_SECRET_KEY`, `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`: auth integration keys.

## Production Notes

- Store uploads in S3/GCS with signed URLs and malware scanning before parsing.
- Move long resume processing to `resume-processing` RQ jobs and stream status over WebSockets or SSE.
- Replace the deterministic scorer with Sentence Transformers/OpenAI embeddings, persist vectors in Chroma/Pinecone, and add retrieval-grounded prompt templates.
- Enforce Clerk/Auth.js JWT verification on protected routes and RBAC for recruiter endpoints.
- Add OpenTelemetry traces and central log shipping for API, worker, and model calls.
