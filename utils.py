import re
from config import SKILLS

# ==========================================
# Extract Skills
# ==========================================

def extract_skills(text: str):
    """
    Extract matching skills from resume/JD.
    """
    text = text.lower()

    found = []

    for skill in SKILLS:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found.append(skill)

    return sorted(list(set(found)))


# ==========================================
# Skill Match Score
# ==========================================

def skill_match_score(jd_skills, resume_skills):
    """
    Returns percentage of matched skills.
    """

    if len(jd_skills) == 0:
        return 0

    matched = set(jd_skills).intersection(
        set(resume_skills)
    )

    score = (
        len(matched) /
        len(jd_skills)
    ) * 100

    return round(score, 2)


# ==========================================
# Missing Skills
# ==========================================

def missing_skills(jd_skills, resume_skills):

    return sorted(

        list(

            set(jd_skills) -

            set(resume_skills)

        )

    )


# ==========================================
# Detect Projects
# ==========================================

PROJECT_KEYWORDS = [

    "project",

    "projects",

    "developed",

    "built",

    "implemented",

    "application",

    "system",

    "website",

    "android",

    "web app",

    "api"

]


def project_score(text):

    text = text.lower()

    count = 0

    for word in PROJECT_KEYWORDS:

        if word in text:

            count += 1

    return min(count * 15, 100)


# ==========================================
# Detect Certifications
# ==========================================

CERTIFICATION_KEYWORDS = [

    "certificate",

    "certification",

    "certified",

    "nptel",

    "coursera",

    "udemy",

    "infosys",

    "cisco",

    "google",

    "aws",

    "microsoft",

    "oracle",

    "ibm"

]


def certification_score(text):

    text = text.lower()

    count = 0

    for word in CERTIFICATION_KEYWORDS:

        if word in text:

            count += 1

    return min(count * 20, 100)


# ==========================================
# Recommendation
# ==========================================

def recommendation(score):

    if score >= 90:

        return "⭐⭐ Highly Recommended"

    elif score >= 75:

        return "⭐ Recommended"

    elif score >= 60:

        return "🟡 Consider"

    else:

        return "❌ Not Recommended"


# ==========================================
# Resume Summary
# ==========================================

def resume_summary(text):

    words = len(text.split())

    chars = len(text)

    lines = len(text.splitlines())

    return {

        "Words": words,

        "Characters": chars,

        "Lines": lines

    }


# ==========================================
# Match Details
# ==========================================

def match_details(jd_skills, resume_skills):

    matched = sorted(

        list(

            set(jd_skills).intersection(

                set(resume_skills)

            )

        )

    )

    missing = missing_skills(

        jd_skills,

        resume_skills

    )

    return {

        "matched": matched,

        "missing": missing

    }