from app.schemas.resume import InterviewPack


class ATSAgent:
    name = "ats-agent"

    def explain(self, failures: list[str]) -> list[str]:
        return failures or ["Resume is likely parseable by mainstream ATS systems."]


class GrammarAgent:
    name = "grammar-agent"

    def rewrite(self, bullet: str, tone: str) -> list[str]:
        tone_prefix = {
            "fresher": "Built",
            "faang": "Engineered",
            "startup": "Shipped",
            "senior_engineer": "Led"
        }.get(tone, "Improved")
        base = bullet.rstrip(".")
        return [
            f"{tone_prefix} a measurable workflow from '{base}', improving delivery speed by 30% through clearer ownership and automation.",
            f"{tone_prefix} production-ready improvements for {base.lower()}, reducing operational friction and strengthening user-facing reliability.",
            f"{tone_prefix} cross-functional execution around {base.lower()}, translating ambiguous requirements into measurable product outcomes."
        ]


class InterviewAgent:
    name = "interview-agent"

    def generate(self, target_role: str) -> InterviewPack:
        return InterviewPack(
            hr=[
                f"Why are you targeting {target_role}, and what tradeoffs matter most to you?",
                "Tell me about a time you handled ambiguous requirements.",
                "What feedback have you received repeatedly, and how did you act on it?"
            ],
            technical=[
                "Design the resume analysis pipeline for 10,000 resumes per hour.",
                "How would you secure file uploads and background processing?",
                "Explain how you would evaluate embedding quality for job matching."
            ],
            dsa=[
                "Find the top K skills across N resumes with streaming updates.",
                "Merge overlapping employment intervals and compute total experience.",
                "Rank candidates by weighted signals with tie-breaking and pagination."
            ],
            resume_based=[
                "Walk through your highest-impact project and the metric you owned.",
                "Which technical decision on your resume would you change today?",
                "How did you validate that your optimization actually helped users?"
            ]
        )


class CareerCoachAgent:
    name = "career-coach-agent"

    def roadmap(self, missing_skills: list[str]) -> list[str]:
        focus = missing_skills[:4] or ["system design", "observability", "AI evaluation"]
        return [f"Build a two-week proof project around {skill} with a deployed demo and metrics." for skill in focus]


class RecruiterAgent:
    name = "recruiter-agent"

    def risk_label(self, ats: int, match: int) -> str:
        if ats >= 82 and match >= 82:
            return "Low"
        if ats >= 70 and match >= 70:
            return "Medium"
        return "High"
