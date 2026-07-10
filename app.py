import os
import tempfile
import pandas as pd
import streamlit as st
from report import (
    generate_excel,
    generate_pdf
)
from parser import extract_text
from scorer import calculate_score
from utils import (
    extract_skills,
    skill_match_score,
    recommendation
)
from ats import (
    experience_years,
    education_score
)
from llm import analyze_resume
from charts import (
    score_bar_chart,
    recommendation_pie,
    experience_chart,
    skill_score_chart,
    semantic_score_chart,
    score_distribution,
    radar_chart,
    leaderboard
)
def load_css():
    with open("style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()
# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------

st.set_page_config(
    page_title="AI Resume Screening Agent",
    page_icon="📄",
    layout="wide"
)

# -----------------------------------------------------
# CUSTOM CSS
# -----------------------------------------------------

st.markdown("""
<style>

.main{
    padding:2rem;
}

.stButton>button{
    width:100%;
    height:3rem;
    font-size:18px;
    font-weight:bold;
}

.metric-card{
    background:#f5f5f5;
    padding:15px;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# SIDEBAR
# -----------------------------------------------------

with st.sidebar:

    st.title("🤖 Resume Screening Agent")

    st.markdown("---")

    st.info("""
Upload one Job Description and multiple resumes.

The system automatically:

• Parses resumes

• Calculates ATS Score

• Matches Skills

• Estimates Experience

• Performs Semantic Matching

• Generates AI Feedback

• Ranks Candidates
""")

    st.markdown("---")

    st.success("Powered by")

    st.write("• Streamlit")

    st.write("• Sentence Transformers")

    st.write("• Groq AI")

    st.write("• Plotly")

# -----------------------------------------------------
# TITLE
# -----------------------------------------------------

st.title("📄 AI Resume Screening Agent")

st.caption(
    "AI Powered Resume Ranking System"
)

st.divider()

# -----------------------------------------------------
# FILE UPLOADS
# -----------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    jd_file = st.file_uploader(
        "Upload Job Description",
        type=["txt"]
    )

with col2:

    resume_files = st.file_uploader(
        "Upload Resumes",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

st.divider()

# -----------------------------------------------------
# SESSION STATE
# -----------------------------------------------------

if "results" not in st.session_state:
    st.session_state.results = None

# -----------------------------------------------------
# ANALYZE BUTTON
# -----------------------------------------------------

analyze = st.button(
    "🚀 Analyze Resumes"
)

# -----------------------------------------------------
# START ANALYSIS
# -----------------------------------------------------

if analyze:

    if jd_file is None:

        st.warning(
            "Please upload a Job Description."
        )

        st.stop()

    if not resume_files:

        st.warning(
            "Please upload at least one Resume."
        )

        st.stop()

    job_description = jd_file.read().decode("utf-8")

    jd_skills = extract_skills(job_description)

    results = []

    progress = st.progress(0)

    status = st.empty()

    for index, resume in enumerate(resume_files):

        status.info(
            f"Processing {resume.name}"
        )

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=os.path.splitext(
                resume.name
            )[1]
        ) as tmp:

            tmp.write(
                resume.getbuffer()
            )

            temp_path = tmp.name

        try:

            resume_text = extract_text(
                temp_path
            )

        except Exception as e:

            st.error(
                f"Unable to read {resume.name}"
            )

            os.remove(temp_path)

            continue
                # -------------------------------------------------
        # SEMANTIC SCORE
        # -------------------------------------------------

        semantic_score = calculate_score(
            job_description,
            resume_text
        )

        # -------------------------------------------------
        # SKILLS
        # -------------------------------------------------

        resume_skills = extract_skills(
            resume_text
        )

        skill_score = skill_match_score(
            jd_skills,
            resume_skills
        )

        matched_skills = sorted(
            list(
                set(jd_skills).intersection(
                    set(resume_skills)
                )
            )
        )

        # -------------------------------------------------
        # EXPERIENCE
        # -------------------------------------------------

        years = experience_years(
            resume_text
        )

        experience_score = min(
            years * 20,
            100
        )

        # -------------------------------------------------
        # EDUCATION
        # -------------------------------------------------

        edu_score = education_score(
            resume_text
        )

        # -------------------------------------------------
        # FINAL ATS SCORE
        # -------------------------------------------------

        final_score = round(

            semantic_score * 0.50 +

            skill_score * 0.25 +

            experience_score * 0.15 +

            edu_score * 0.10,

            2

        )

        # -------------------------------------------------
        # AI ANALYSIS
        # -------------------------------------------------

        try:

            ai = analyze_resume(
                job_description,
                resume_text
            )

        except Exception:

            ai = {

                "overall_match": 0,

                "strengths": [],

                "weaknesses": [],

                "missing_skills": [],

                "recommendation": "Unavailable",

                "summary": "Unable to generate AI analysis."

            }

        # -------------------------------------------------
        # STORE RESULT
        # -------------------------------------------------

        results.append({

            "Resume": resume.name,

            "Semantic Score": semantic_score,

            "Skill Score": skill_score,

            "Experience (Years)": years,

            "Education Score": edu_score,

            "Matched Skills": ", ".join(matched_skills),

            "Final Score": final_score,

            "Recommendation": recommendation(
                final_score
            ),

            "AI": ai,

            "Resume Text": resume_text

        })

        progress.progress(
            (index + 1) / len(resume_files)
        )

        os.remove(temp_path)

    progress.empty()

    status.success(
        "Analysis Complete!"
    )

    # -------------------------------------------------
    # DATAFRAME
    # -------------------------------------------------

    df = pd.DataFrame(results)

    df = df.sort_values(
        by="Final Score",
        ascending=False
    ).reset_index(drop=True)

    df.index = df.index + 1

    st.session_state.results = df

# =====================================================
# DISPLAY RESULTS
# =====================================================

if st.session_state.results is not None:

    df = st.session_state.results

    st.divider()

    st.header("🏆 Candidate Ranking")

    st.dataframe(

        df[
            [

                "Resume",

                "Semantic Score",

                "Skill Score",

                "Experience (Years)",

                "Education Score",

                "Final Score",

                "Recommendation"

            ]

        ],

        use_container_width=True

    )

    st.download_button(

        "📥 Download CSV",

        df.drop(
            columns=[
                "AI",
                "Resume Text"
            ]
        ).to_csv(index=False),

        "resume_ranking.csv",

        "text/csv"

    )

    best = df.iloc[0]

    st.divider()

    st.header("🥇 Top Candidate")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Resume",
        best["Resume"]
    )

    c2.metric(
        "ATS Score",
        f"{best['Final Score']}%"
    )

    c3.metric(
        "Experience",
        f"{best['Experience (Years)']} Years"
    )

    c4.metric(
        "Recommendation",
        best["Recommendation"]
    )
    # =====================================================
# ANALYTICS DASHBOARD
# =====================================================

    st.divider()

    st.header("📊 Analytics Dashboard")

    chart1, chart2 = st.columns(2)

    with chart1:

        st.plotly_chart(
            score_bar_chart(df),
            use_container_width=True
        )

    with chart2:

        st.plotly_chart(
            recommendation_pie(df),
            use_container_width=True
        )

    st.plotly_chart(
        score_distribution(df),
        use_container_width=True
    )

    graph1, graph2 = st.columns(2)

    with graph1:

        st.plotly_chart(
            experience_chart(df),
            use_container_width=True
        )

    with graph2:

        st.plotly_chart(
            skill_score_chart(df),
            use_container_width=True
        )

    st.plotly_chart(
        semantic_score_chart(df),
        use_container_width=True
    )

# =====================================================
# LEADERBOARD
# =====================================================

if st.session_state.results is not None:

    df = st.session_state.results

    st.divider()

    st.header("🏆 Top Candidates")

    leaders = leaderboard(df)

    st.dataframe(
        leaders[
            [
                "Resume",
                "Final Score",
                "Recommendation"
            ]
        ],
        use_container_width=True
    )


    # =====================================================
    # DOWNLOAD REPORTS
    # =====================================================

    st.subheader("📥 Download Reports")

    csv = df.drop(
        columns=[
            "AI",
            "Resume Text"
        ],
        errors="ignore"
    ).to_csv(index=False)


    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="resume_report.csv",
        mime="text/csv"
    )

# =====================================================
# AI ANALYSIS
# =====================================================

    st.divider()

    st.header("🤖 AI Recruiter Feedback")

    for _, row in df.iterrows():

        with st.expander(

            f"📄 {row['Resume']}"

        ):

            ai = row["AI"]

            st.metric(

                "Overall Match",

                f"{ai.get('overall_match',0)}%"

            )

            st.subheader(

                "✅ Strengths"

            )

            strengths = ai.get(

                "strengths",

                []

            )

            if strengths:

                for item in strengths:

                    st.success(item)

            else:

                st.info("None")

            st.subheader(

                "⚠ Weaknesses"

            )

            weaknesses = ai.get(

                "weaknesses",

                []

            )

            if weaknesses:

                for item in weaknesses:

                    st.warning(item)

            else:

                st.info("None")

            st.subheader(

                "❌ Missing Skills"

            )

            missing = ai.get(

                "missing_skills",

                []

            )

            if missing:

                for item in missing:

                    st.error(item)

            else:

                st.success(

                    "No missing skills."

                )

            st.subheader(

                "📝 Recruiter Summary"

            )

            st.info(

                ai.get(

                    "summary",

                    ""

                )

            )

# =====================================================
# SCORE SUMMARY
# =====================================================

    st.divider()

    st.header("📈 Overall Summary")

    average = round(

        df["Final Score"].mean(),

        2

    )

    highest = round(

        df["Final Score"].max(),

        2

    )

    lowest = round(

        df["Final Score"].min(),

        2

    )

    total = len(df)

    m1, m2, m3, m4 = st.columns(4)

    m1.metric(

        "Total Candidates",

        total

    )

    m2.metric(

        "Average Score",

        f"{average}%"

    )

    m3.metric(

        "Highest Score",

        f"{highest}%"

    )

    m4.metric(

        "Lowest Score",

        f"{lowest}%"

    )