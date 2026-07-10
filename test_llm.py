from llm import analyze_resume

jd = """
Python Backend Developer

Skills Required

Python

FastAPI

SQL

Docker

Git

AWS
"""

resume = """
Python Developer

Skills

Python

Flask

SQL

Git

TensorFlow

Machine Learning
"""

result = analyze_resume(jd, resume)

print(result)