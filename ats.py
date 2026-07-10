import re

from config import ATS_WEIGHTS
from utils import (
    project_score,
    certification_score
)

# =====================================================
# EXPERIENCE
# =====================================================

def experience_years(text):

    text = text.lower()

    patterns = [

        r'(\d+)\+?\s*years',

        r'(\d+)\+?\s*year',

        r'(\d+)\+?\s*yrs',

        r'(\d+)\+?\s*yr'

    ]

    maximum = 0

    for pattern in patterns:

        matches = re.findall(pattern, text)

        for value in matches:

            maximum = max(

                maximum,

                int(value)

            )

    return maximum


# =====================================================
# EXPERIENCE SCORE
# =====================================================

def experience_score(years):

    if years >= 5:
        return 100

    elif years == 4:
        return 90

    elif years == 3:
        return 80

    elif years == 2:
        return 70

    elif years == 1:
        return 60

    return 40


# =====================================================
# EDUCATION SCORE
# =====================================================

def education_score(text):

    text = text.lower()

    if "phd" in text:

        return 100

    elif (
        "m.tech" in text or
        "master" in text or
        "mca" in text or
        "ms" in text
    ):

        return 90

    elif (
        "b.tech" in text or
        "btech" in text or
        "b.e" in text or
        "be" in text or
        "bachelor" in text
    ):

        return 80

    elif "diploma" in text:

        return 60

    return 40


# =====================================================
# FINAL ATS SCORE
# =====================================================

def calculate_ats_score(

    semantic_score,

    skill_score,

    resume_text

):

    years = experience_years(

        resume_text

    )

    exp_score = experience_score(

        years

    )

    edu_score = education_score(

        resume_text

    )

    proj_score = project_score(

        resume_text

    )

    cert_score = certification_score(

        resume_text

    )

    final = (

        semantic_score *

        ATS_WEIGHTS["semantic"]

        +

        skill_score *

        ATS_WEIGHTS["skills"]

        +

        exp_score *

        ATS_WEIGHTS["experience"]

        +

        edu_score *

        ATS_WEIGHTS["education"]

        +

        proj_score *

        ATS_WEIGHTS["projects"]

        +

        cert_score *

        ATS_WEIGHTS["certifications"]

    )

    return {

        "experience_years": years,

        "experience_score": round(

            exp_score,

            2

        ),

        "education_score": round(

            edu_score,

            2

        ),

        "project_score": round(

            proj_score,

            2

        ),

        "certification_score": round(

            cert_score,

            2

        ),

        "final_score": round(

            final,

            2

        )

    }