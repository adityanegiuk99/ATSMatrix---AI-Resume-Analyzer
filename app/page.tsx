"use client";

import { useState } from "react";
import { Activity, Bot, Layers3, ShieldCheck, type LucideIcon } from "lucide-react";
import { AnalysisResult } from "@/lib/types";
import { ThemeToggle } from "@/components/theme-toggle";
import { ResumeUploader } from "@/components/resume-uploader";
import { AnalysisDashboard } from "@/components/analysis-dashboard";
import { AiTools } from "@/components/ai-tools";
import { RecruiterDashboard } from "@/components/recruiter-dashboard";

export default function Home() {
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  return (
    <main className="min-h-screen">
      <header className="sticky top-0 z-20 border-b bg-background/85 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
          <div className="flex items-center gap-3">
            <div className="grid h-9 w-9 place-items-center rounded-md bg-primary text-primary-foreground">
              <Layers3 className="h-5 w-5" />
            </div>
            <div>
              <p className="font-semibold">ATSMatrix</p>
              <p className="text-xs text-muted-foreground">AI Resume Analyzer & Career Intelligence</p>
            </div>
          </div>
          <ThemeToggle />
        </div>
      </header>

      <section className="border-b bg-secondary/35">
        <div className="mx-auto grid max-w-7xl gap-8 px-4 py-10 lg:grid-cols-[0.95fr_1.05fr] lg:items-center">
          <div className="space-y-6">
            <div className="flex flex-wrap gap-2">
              {["ATS simulation", "Semantic matching", "Recruiter analytics"].map((item) => (
                <span key={item} className="rounded-sm border bg-background px-3 py-1 text-xs text-muted-foreground">{item}</span>
              ))}
            </div>
            <div className="space-y-4">
              <h1 className="max-w-3xl text-4xl font-semibold tracking-normal md:text-5xl">ATSMatrix</h1>
              <p className="max-w-2xl text-lg text-muted-foreground">
                Production-ready resume intelligence for candidates and hiring teams: parser diagnostics, AI rewriting, RAG career coaching, semantic job fit, and bulk candidate ranking.
              </p>
            </div>
            <div className="grid gap-3 sm:grid-cols-3">
              <Signal icon={ShieldCheck} label="Secure uploads" />
              <Signal icon={Bot} label="Multi-agent AI" />
              <Signal icon={Activity} label="Realtime pipeline" />
            </div>
          </div>
          <ResumeUploader onAnalysis={setAnalysis} />
        </div>
      </section>

      <div className="mx-auto max-w-7xl space-y-6 px-4 py-8">
        {analysis ? <AnalysisDashboard analysis={analysis} /> : <EmptyState />}
        <AiTools />
        <RecruiterDashboard />
      </div>
    </main>
  );
}

function Signal({ icon: Icon, label }: { icon: LucideIcon; label: string }) {
  return (
    <div className="flex items-center gap-2 rounded-lg border bg-background p-3 text-sm">
      <Icon className="h-4 w-4 text-primary" />
      {label}
    </div>
  );
}

function EmptyState() {
  return (
    <div className="grid min-h-64 place-items-center rounded-lg border border-dashed bg-secondary/25 p-8 text-center">
      <div className="max-w-md space-y-2">
        <p className="text-lg font-medium">Upload a resume to run the full intelligence workflow.</p>
        <p className="text-sm text-muted-foreground">The backend returns structured parsing, ATS score, missing skills, semantic match, heatmap cells, and section feedback.</p>
      </div>
    </div>
  );
}
