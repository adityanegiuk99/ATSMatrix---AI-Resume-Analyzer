export type RewriteTone = "fresher" | "faang" | "startup" | "senior_engineer";

export type HeatmapCell = {
  section: string;
  signal: "strong" | "medium" | "weak";
  label: string;
};

export type AnalysisResult = {
  resume_id: string;
  candidate_name: string;
  ats_score: number;
  semantic_match: number;
  readability_score: number;
  missing_keywords: string[];
  matched_keywords: string[];
  parsing_failures: string[];
  section_feedback: { section: string; status: string; feedback: string }[];
  heatmap: HeatmapCell[];
  extracted: {
    skills: string[];
    education: string[];
    experience: string[];
    projects: string[];
    links: string[];
  };
  recommendations: string[];
};

export type CandidateRank = {
  id: string;
  name: string;
  role: string;
  match: number;
  ats: number;
  skills: string[];
  risk: string;
};

export type InterviewPack = {
  hr: string[];
  technical: string[];
  dsa: string[];
  resume_based: string[];
};
