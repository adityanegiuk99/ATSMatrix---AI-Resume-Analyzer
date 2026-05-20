import math
import re
from collections import Counter
from app.schemas.resume import ExtractedResume, HeatmapCell, SectionFeedback
from app.services.parser import ParsedResume

STOPWORDS = {"and", "the", "with", "for", "you", "are", "that", "this", "from", "will", "have", "has"}


def analyze(parsed: ParsedResume, job_description: str) -> dict:
    jd_keywords = _keywords(job_description)
    resume_keywords = _keywords(parsed.raw_text)
    matched = sorted(jd_keywords & resume_keywords)
    missing = sorted((jd_keywords - resume_keywords))[:18]
    semantic_match = _cosine_score(parsed.raw_text, job_description)
    formatting_score = max(0, 100 - len(parsed.parsing_failures) * 12)
    section_score = _section_score(parsed)
    keyword_score = min(100, int((len(matched) / max(1, len(jd_keywords))) * 100))
    readability = _readability(parsed.raw_text)
    ats_score = round(keyword_score * 0.34 + formatting_score * 0.24 + section_score * 0.24 + readability * 0.18)
    feedback = _section_feedback(parsed, missing)
    return {
        "candidate_name": parsed.candidate_name,
        "ats_score": ats_score,
        "semantic_match": semantic_match,
        "readability_score": readability,
        "missing_keywords": missing,
        "matched_keywords": matched[:18],
        "parsing_failures": parsed.parsing_failures,
        "section_feedback": feedback,
        "heatmap": _heatmap(parsed, matched, missing),
        "extracted": ExtractedResume(
            skills=parsed.skills,
            education=parsed.education,
            experience=parsed.experience,
            projects=parsed.projects,
            links=parsed.links,
        ),
        "recommendations": _recommendations(parsed, missing),
    }


def _keywords(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z+#./-]{2,}", text.lower())
    counts = Counter(word for word in words if word not in STOPWORDS)
    return {word for word, count in counts.items() if count >= 1 and len(word) > 2}


def _cosine_score(a: str, b: str) -> int:
    ca, cb = Counter(_keywords(a)), Counter(_keywords(b))
    vocab = set(ca) | set(cb)
    dot = sum(ca[w] * cb[w] for w in vocab)
    na = math.sqrt(sum(ca[w] ** 2 for w in vocab))
    nb = math.sqrt(sum(cb[w] ** 2 for w in vocab))
    if not na or not nb:
        return 0
    return round((dot / (na * nb)) * 100)


def _readability(text: str) -> int:
    sentences = max(1, len(re.findall(r"[.!?]", text)))
    words = max(1, len(text.split()))
    avg_sentence = words / sentences
    penalty = max(0, avg_sentence - 22) * 1.8
    bullet_bonus = min(12, len(re.findall(r"(^|\n)[\-•]", text)) * 1.5)
    return max(35, min(98, round(86 - penalty + bullet_bonus)))


def _section_score(parsed: ParsedResume) -> int:
    present = sum(bool(getattr(parsed, section)) for section in ["skills", "education", "experience", "projects"])
    link_bonus = 10 if parsed.links else 0
    return min(100, present * 22 + link_bonus)


def _section_feedback(parsed: ParsedResume, missing: list[str]) -> list[SectionFeedback]:
    return [
        SectionFeedback(section="Skills", status="Strong" if len(parsed.skills) >= 7 else "Improve", feedback=f"{len(parsed.skills)} technical skills detected. Add missing role keywords: {', '.join(missing[:5]) or 'none'}."),
        SectionFeedback(section="Experience", status="Strong" if parsed.experience else "Missing", feedback="Use quantified bullets with action verbs, scope, metric, and business outcome."),
        SectionFeedback(section="Projects", status="Strong" if parsed.projects else "Improve", feedback="Include deployed links, architecture choices, user impact, and measurable results."),
        SectionFeedback(section="Formatting", status="Risk" if parsed.parsing_failures else "Clean", feedback="Avoid tables, icons, multi-column layouts, headers/footers, and image-only text."),
    ]


def _heatmap(parsed: ParsedResume, matched: list[str], missing: list[str]) -> list[HeatmapCell]:
    cells: list[HeatmapCell] = []
    for section in ["summary", "skills", "experience", "projects", "education", "links", "formatting", "keywords"]:
        signal = "strong"
        if section == "formatting" and parsed.parsing_failures:
            signal = "weak"
        elif section == "keywords" and len(missing) > len(matched):
            signal = "weak"
        elif not getattr(parsed, section, True) and section in {"skills", "experience", "projects", "education", "links"}:
            signal = "medium"
        for idx in range(4):
            cells.append(HeatmapCell(section=section, signal=signal, label=f"{section} signal {idx + 1}"))
    return cells


def _recommendations(parsed: ParsedResume, missing: list[str]) -> list[str]:
    recs = ["Move critical skills into a plain Skills section near the top.", "Rewrite bullets as: action verb + technical scope + metric + business outcome."]
    if missing:
        recs.append(f"Naturally include high-value missing keywords: {', '.join(missing[:8])}.")
    if parsed.parsing_failures:
        recs.append("Create an ATS-safe version using one column, standard bullets, and selectable text.")
    return recs
