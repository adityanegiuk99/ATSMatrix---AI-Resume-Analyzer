"use client";

import { useEffect, useState } from "react";
import { BarChart3, Filter, UsersRound } from "lucide-react";
import { getRecruiterRanking } from "@/lib/api";
import { CandidateRank } from "@/lib/types";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

const fallback: CandidateRank[] = [
  { id: "demo-1", name: "Aarav Mehta", role: "Full-stack AI Engineer", match: 92, ats: 88, skills: ["Next.js", "Python", "RAG"], risk: "Low" },
  { id: "demo-2", name: "Neha Rao", role: "Backend Engineer", match: 84, ats: 81, skills: ["FastAPI", "Postgres", "Redis"], risk: "Medium" },
  { id: "demo-3", name: "Kabir Shah", role: "Frontend Engineer", match: 78, ats: 74, skills: ["React", "TypeScript", "Charts"], risk: "Medium" }
];

export function RecruiterDashboard() {
  const [candidates, setCandidates] = useState<CandidateRank[]>(fallback);
  useEffect(() => {
    getRecruiterRanking().then(setCandidates).catch(() => setCandidates(fallback));
  }, []);

  return (
    <Card>
      <CardHeader className="flex-row items-start justify-between gap-4">
        <div>
          <CardTitle>Recruiter Command Center</CardTitle>
          <CardDescription>Bulk ranking, skill filters, comparison signals, and funnel analytics.</CardDescription>
        </div>
        <div className="flex gap-2 text-muted-foreground">
          <UsersRound className="h-5 w-5" />
          <Filter className="h-5 w-5" />
          <BarChart3 className="h-5 w-5" />
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {candidates.map((candidate, index) => (
          <div key={candidate.id} className="grid gap-4 rounded-lg border p-4 md:grid-cols-[40px_1fr_180px_100px] md:items-center">
            <div className="text-lg font-semibold text-primary">#{index + 1}</div>
            <div>
              <p className="font-medium">{candidate.name}</p>
              <p className="text-sm text-muted-foreground">{candidate.role}</p>
              <div className="mt-2 flex flex-wrap gap-2">
                {candidate.skills.map((skill) => (
                  <span key={skill} className="rounded-sm bg-secondary px-2 py-1 text-xs">{skill}</span>
                ))}
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between text-sm"><span>Match</span><span>{candidate.match}%</span></div>
              <Progress value={candidate.match} />
            </div>
            <div className="text-sm text-muted-foreground">Risk: {candidate.risk}</div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
