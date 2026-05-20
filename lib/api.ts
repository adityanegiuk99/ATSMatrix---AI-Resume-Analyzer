import { AnalysisResult, CandidateRank, InterviewPack, RewriteTone } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      ...(init?.body instanceof FormData ? {} : { "Content-Type": "application/json" }),
      ...init?.headers
    },
    cache: "no-store"
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function analyzeResume(file: File, jobDescription: string): Promise<AnalysisResult> {
  const formData = new FormData();
  formData.append("resume", file);
  formData.append("job_description", jobDescription);
  return apiFetch<AnalysisResult>("/resumes/analyze", { method: "POST", body: formData });
}

export async function rewriteBullet(bullet: string, tone: RewriteTone) {
  return apiFetch<{ rewrites: string[] }>("/ai/rewrite", {
    method: "POST",
    body: JSON.stringify({ bullet, tone })
  });
}

export async function generateInterview(resumeId: string, role: string): Promise<InterviewPack> {
  return apiFetch<InterviewPack>("/interviews/generate", {
    method: "POST",
    body: JSON.stringify({ resume_id: resumeId, target_role: role })
  });
}

export async function getRecruiterRanking(): Promise<CandidateRank[]> {
  return apiFetch<CandidateRank[]>("/recruiter/rankings");
}
