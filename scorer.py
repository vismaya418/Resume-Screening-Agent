from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def calculate_score(job_description,resume):

    jd_embedding = model.encode([job_description])

    resume_embedding = model.encode([resume])

    score = cosine_similarity(
        jd_embedding,
        resume_embedding
    )[0][0]

    return round(score*100,2)