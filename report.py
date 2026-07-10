from io import BytesIO

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


# =====================================================
# EXCEL REPORT
# =====================================================

def generate_excel(df):
    """
    Generate Excel report from DataFrame.
    Returns BytesIO object.
    """

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        export_df = df.copy()

        if "AI" in export_df.columns:
            export_df = export_df.drop(columns=["AI"])

        if "Resume Text" in export_df.columns:
            export_df = export_df.drop(columns=["Resume Text"])

        export_df.to_excel(
            writer,
            index=False,
            sheet_name="Resume Ranking"
        )

    output.seek(0)

    return output


# =====================================================
# PDF REPORT
# =====================================================

def generate_pdf(df):
    """
    Generate recruiter PDF report.
    Returns BytesIO object.
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "AI Resume Screening Report",
            styles["Heading1"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"Total Candidates : {len(df)}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 10))

    avg = round(
        df["Final Score"].mean(),
        2
    )

    story.append(
        Paragraph(
            f"Average ATS Score : {avg}%",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))

    table_data = [[

        "Resume",

        "ATS",

        "Experience",

        "Recommendation"

    ]]

    for _, row in df.iterrows():

        table_data.append([

            row["Resume"],

            row["Final Score"],

            row["Experience (Years)"],

            row["Recommendation"]

        ])

    table = Table(table_data)

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 12)

        ])

    )

    story.append(table)

    story.append(Spacer(1, 25))

    story.append(

        Paragraph(

            "Top Candidate",

            styles["Heading2"]

        )

    )

    best = df.iloc[0]

    story.append(

        Paragraph(

            f"Resume : {best['Resume']}",

            styles["Normal"]

        )

    )

    story.append(

        Paragraph(

            f"ATS Score : {best['Final Score']}%",

            styles["Normal"]

        )

    )

    story.append(

        Paragraph(

            f"Recommendation : {best['Recommendation']}",

            styles["Normal"]

        )

    )

    if "AI" in best.index:

        ai = best["AI"]

        summary = ai.get(
            "summary",
            "No AI summary available."
        )

        story.append(Spacer(1, 10))

        story.append(

            Paragraph(

                "AI Recruiter Summary",

                styles["Heading2"]

            )

        )

        story.append(

            Paragraph(

                summary,

                styles["BodyText"]

            )

        )

    doc.build(story)

    buffer.seek(0)

    return buffer