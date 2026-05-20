"use client";

import { useState, useTransition } from "react";
import { useDropzone } from "react-dropzone";
import { FileText, Loader2, UploadCloud } from "lucide-react";
import { analyzeResume } from "@/lib/api";
import { AnalysisResult } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";

const defaultJd = "Senior full-stack engineer with React, Next.js, TypeScript, Python, PostgreSQL, Redis, AI product experience, system design, CI/CD, and strong product ownership.";

export function ResumeUploader({ onAnalysis }: { onAnalysis: (analysis: AnalysisResult) => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState(defaultJd);
  const [error, setError] = useState("");
  const [isPending, startTransition] = useTransition();
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    maxFiles: 1,
    accept: {
      "application/pdf": [".pdf"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"]
    },
    onDrop: (files) => {
      setError("");
      setFile(files[0] ?? null);
    }
  });

  function submit() {
    if (!file) {
      setError("Upload a PDF or DOCX resume first.");
      return;
    }
    startTransition(async () => {
      try {
        onAnalysis(await analyzeResume(file, jobDescription));
      } catch (err) {
        setError(err instanceof Error ? err.message : "Analysis failed");
      }
    });
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Resume Intelligence Intake</CardTitle>
        <CardDescription>PDF/DOCX parsing, ATS simulation, semantic matching, and AI feedback in one pipeline.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div
          {...getRootProps()}
          className="grid min-h-40 cursor-pointer place-items-center rounded-lg border border-dashed bg-secondary/45 p-6 text-center transition-colors hover:bg-secondary"
        >
          <input {...getInputProps()} />
          <div className="space-y-3">
            {file ? <FileText className="mx-auto h-10 w-10 text-primary" /> : <UploadCloud className="mx-auto h-10 w-10 text-primary" />}
            <div>
              <p className="font-medium">{file ? file.name : isDragActive ? "Drop the resume here" : "Upload resume"}</p>
              <p className="text-sm text-muted-foreground">PDF or DOCX, up to 10 MB</p>
            </div>
          </div>
        </div>
        <Textarea value={jobDescription} onChange={(event) => setJobDescription(event.target.value)} aria-label="Job description" />
        {error ? <p className="text-sm text-destructive">{error}</p> : null}
        <Button onClick={submit} disabled={isPending} className="w-full">
          {isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <UploadCloud className="h-4 w-4" />}
          Analyze Resume
        </Button>
      </CardContent>
    </Card>
  );
}
