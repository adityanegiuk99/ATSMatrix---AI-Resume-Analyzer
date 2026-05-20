import { scoreColor } from "@/lib/utils";

export function ScoreRing({ score, label }: { score: number; label: string }) {
  const background = `conic-gradient(hsl(var(--primary)) ${score * 3.6}deg, hsl(var(--secondary)) 0deg)`;
  return (
    <div className="flex items-center gap-4">
      <div className="grid h-24 w-24 place-items-center rounded-full" style={{ background }}>
        <div className="grid h-20 w-20 place-items-center rounded-full bg-card">
          <span className={`text-2xl font-bold ${scoreColor(score)}`}>{score}</span>
        </div>
      </div>
      <div>
        <p className="text-sm text-muted-foreground">{label}</p>
        <p className="text-sm font-medium">Recruiter-grade signal score</p>
      </div>
    </div>
  );
}
