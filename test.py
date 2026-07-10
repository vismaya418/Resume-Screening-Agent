from parser import extract_text
from scorer import calculate_score

# Read Job Description
with open("sample_data/job_description.txt", "r", encoding="utf-8") as f:
    jd = f.read()

# Read Resume
resume = extract_text("resumes/resume1.pdf")

# Calculate Similarity Score
score = calculate_score(jd, resume)

print("Resume Similarity Score:", score)