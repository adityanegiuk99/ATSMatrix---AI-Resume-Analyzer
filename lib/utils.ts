import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function scoreColor(score: number) {
  if (score >= 82) return "text-success";
  if (score >= 65) return "text-warning";
  return "text-coral";
}

export function asPercent(value: number) {
  return `${Math.round(value)}%`;
}
