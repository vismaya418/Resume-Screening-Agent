import plotly.express as px
import plotly.graph_objects as go


def score_bar_chart(df):
    """
    Horizontal bar chart showing ATS score for each candidate.
    """
    fig = px.bar(
        df,
        x="Final Score",
        y="Resume",
        orientation="h",
        text="Final Score",
        color="Final Score",
        color_continuous_scale="Viridis",
        title="🏆 ATS Score by Candidate"
    )

    fig.update_layout(
        height=500,
        xaxis_title="ATS Score",
        yaxis_title="Resume",
        yaxis=dict(autorange="reversed")
    )

    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")

    return fig


def recommendation_pie(df):
    """
    Pie chart of recommendation categories.
    """
    counts = (
        df["Recommendation"]
        .value_counts()
        .reset_index()
    )

    counts.columns = ["Recommendation", "Count"]

    fig = px.pie(
        counts,
        names="Recommendation",
        values="Count",
        title="📌 Recommendation Distribution",
        hole=0.45
    )

    return fig


def experience_chart(df):
    """
    Experience comparison chart.
    """
    fig = px.bar(
        df,
        x="Resume",
        y="Experience (Years)",
        color="Experience (Years)",
        text="Experience (Years)",
        title="💼 Candidate Experience"
    )

    fig.update_traces(textposition="outside")

    return fig


def skill_score_chart(df):
    """
    Skill score comparison.
    """
    fig = px.bar(
        df,
        x="Resume",
        y="Skill Score",
        color="Skill Score",
        text="Skill Score",
        title="🛠 Skill Match Score"
    )

    fig.update_traces(textposition="outside")

    return fig


def semantic_score_chart(df):
    """
    Semantic similarity comparison.
    """
    fig = px.bar(
        df,
        x="Resume",
        y="Semantic Score",
        color="Semantic Score",
        text="Semantic Score",
        title="🧠 Semantic Similarity"
    )

    fig.update_traces(textposition="outside")

    return fig


def score_distribution(df):
    """
    Histogram of ATS scores.
    """
    fig = px.histogram(
        df,
        x="Final Score",
        nbins=10,
        title="📊 ATS Score Distribution"
    )

    return fig


def radar_chart(candidate):
    """
    Radar chart for one candidate.
    """

    categories = [
        "Semantic",
        "Skills",
        "Experience",
        "Education"
    ]

    values = [
        candidate["Semantic Score"],
        candidate["Skill Score"],
        min(candidate["Experience (Years)"] * 20, 100),
        candidate["Education Score"]
    ]

    values.append(values[0])
    categories.append(categories[0])

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            name=candidate["Resume"]
        )
    )

    fig.update_layout(

        polar=dict(

            radialaxis=dict(

                visible=True,

                range=[0, 100]

            )

        ),

        title="🎯 Candidate Profile"

    )

    return fig


def leaderboard(df):
    """
    Return Top 10 candidates.
    """
    return df.sort_values(
        "Final Score",
        ascending=False
    ).head(10)