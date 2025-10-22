import re

SECTION_KEYWORDS = {
    "experience": ["experience","work experience", "employment", "work history"],
    "education": ["education", "academic"],
    "skills": ["skills", "technical skills", "core skills"],
    "projects": ["projects"],
    "summary": ["summary", "profile"],
    "certifications": ["certifications", "licenses"],
}

def detect_sections(text: str):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    sections = {}
    current = "preamble"
    sections[current] = []
    for line in lines:
        low = line.lower()
        found = False
        for sec, kws in SECTION_KEYWORDS.items():
            for kw in kws:
                if low.startswith(kw):
                    current = sec
                    sections.setdefault(current, [])
                    found = True
                    break
            if found: break
        sections[current].append(line)
    return {k: "\n".join(v).strip() for k, v in sections.items()}
