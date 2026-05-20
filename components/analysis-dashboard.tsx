"use client";

import { AnimatePresence, motion } from "framer-motion";
import { AlertTriangle, CheckCircle2, FileSearch, Sparkles, Target, type LucideIcon } from "lucide-react";
import { AnalysisResult } from "@/lib/types";
import { asPercent } from "@/lib/utils";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { ScoreRing } from "@/components/score-ring";
import { Heatmap } from "@/components/heatmap";

export function AnalysisDashboard({ analysis }: { analysis: AnalysisResult }) {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={analysis.resume_id}
        initial={{ opacity: 0, y: 14 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -14 }}
        className="grid gap-5 xl:grid-cols-[1.25fr_0.75fr]"
      >
        <Card>
          <CardHeader>
            <CardTitle>{analysis.candidate_name}</CardTitle>
            <CardDescription>ATS score, semantic fit, parsing confidence, and reviewer recommendations.</CardDescription>
          </CardHeader>
          <CardContent className="grid gap-6 md:grid-cols-3">
            <ScoreRing score={analysis.ats_score} label="ATS Score" />
            <Metric icon={Target} label="Semantic Match" value={asPercent(analysis.semantic_match)} progress={analysis.semantic_match} />
            <Metric icon={Sparkles} label="Readability" value={asPercent(analysis.readability_score)} progress={analysis.readability_score} />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Resume Heatmap</CardTitle>
            <CardDescription>Section risk visualization from parser, keyword, and formatting signals.</CardDescription>
          </CardHeader>
          <CardContent>
            <Heatmap cells={analysis.heatmap} />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Section Feedback</CardTitle>
            <CardDescription>Actionable analysis by resume section.</CardDescription>
          </CardHeader>
          <CardContent className="grid gap-3 md:grid-cols-2">
            {analysis.section_feedback.map((item) => (
              <div key={item.section} className="rounded-lg border p-4">
                <div className="mb-2 flex items-center justify-between">
                  <p className="font-medium">{item.section}</p>
                  <span className="text-xs text-muted-foreground">{item.status}</span>
                </div>
                <p className="text-sm text-muted-foreground">{item.feedback}</p>
              </div>
            ))}
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>ATS Simulator</CardTitle>
            <CardDescription>Real-world parsing and formatting risks detected.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {analysis.parsing_failures.length ? (
              analysis.parsing_failures.map((failure) => (
                <div key={failure} className="flex gap-3 rounded-lg border border-warning/30 bg-warning/10 p-3 text-sm">
                  <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-warning" />
                  <span>{failure}</span>
                </div>
              ))
            ) : (
              <div className="flex gap-3 rounded-lg border border-success/30 bg-success/10 p-3 text-sm">
                <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-success" />
                <span>No major parser blockers detected.</span>
              </div>
            )}
            <KeywordList title="Matched" words={analysis.matched_keywords} />
            <KeywordList title="Missing" words={analysis.missing_keywords} />
          </CardContent>
        </Card>
        <Card className="xl:col-span-2">
          <CardHeader>
            <CardTitle>Extracted Resume Knowledge</CardTitle>
            <CardDescription>Structured profile produced by the parsing and NLP pipeline.</CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4 md:grid-cols-5">
            {Object.entries(analysis.extracted).map(([section, values]) => (
              <div key={section} className="rounded-lg border p-4">
                <div className="mb-3 flex items-center gap-2 font-medium capitalize">
                  <FileSearch className="h-4 w-4 text-primary" />
                  {section}
                </div>
                <div className="space-y-2 text-sm text-muted-foreground">
                  {values.slice(0, 5).map((value) => (
                    <p key={value}>{value}</p>
                  ))}
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </motion.div>
    </AnimatePresence>
  );
}

function Metric({ icon: Icon, label, value, progress }: { icon: LucideIcon; label: string; value: string; progress: number }) {
  return (
    <div className="space-y-3 rounded-lg border p-4">
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <Icon className="h-4 w-4 text-primary" />
        {label}
      </div>
      <p className="text-3xl font-semibold">{value}</p>
      <Progress value={progress} />
    </div>
  );
}

function KeywordList({ title, words }: { title: string; words: string[] }) {
  return (
    <div>
      <p className="mb-2 text-sm font-medium">{title} keywords</p>
      <div className="flex flex-wrap gap-2">
        {words.slice(0, 12).map((word) => (
          <span key={word} className="rounded-sm bg-secondary px-2 py-1 text-xs">
            {word}
          </span>
        ))}
      </div>
    </div>
  );
}
