import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found. Please add it to your .env file."
    )

client = Groq(api_key=api_key)


def analyze_resume(job_description: str, resume_text: str):
    """
    Analyze a resume against a job description using Groq LLM.

    Returns a Python dictionary.
    """

    prompt = f"""
You are an experienced Technical HR Recruiter.

Compare the following Resume with the Job Description.

Return ONLY valid JSON.

Format:

{{
    "overall_match": 90,
    "strengths":[
        "...",
        "...",
        "..."
    ],
    "weaknesses":[
        "...",
        "..."
    ],
    "missing_skills":[
        "...",
        "..."
    ],
    "recommendation":"Highly Recommended",
    "summary":"A short recruiter summary."
}}

Job Description:

{job_description}

Resume:

{resume_text[:6000]}
"""

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            temperature=0.2,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            response_format={
                "type": "json_object"
            }

        )

        content = response.choices[0].message.content

        return json.loads(content)

    except Exception as e:

        return {

            "overall_match": 0,

            "strengths": [],

            "weaknesses": [],

            "missing_skills": [],

            "recommendation": "Error",

            "summary": str(e)

        }