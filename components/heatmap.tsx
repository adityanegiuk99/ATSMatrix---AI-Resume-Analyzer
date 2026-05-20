import { HeatmapCell } from "@/lib/types";
import { cn } from "@/lib/utils";

const color = {
  strong: "bg-success",
  medium: "bg-warning",
  weak: "bg-coral"
};

export function Heatmap({ cells }: { cells: HeatmapCell[] }) {
  return (
    <div className="heatmap-grid">
      {cells.map((cell, index) => (
        <div
          key={`${cell.section}-${cell.label}-${index}`}
          title={`${cell.section}: ${cell.label}`}
          className={cn("h-10 rounded-sm opacity-90 transition-opacity hover:opacity-100", color[cell.signal])}
        />
      ))}
    </div>
  );
}
