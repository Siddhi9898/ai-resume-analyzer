import streamlit as st
import pandas as pd
import io

from utils.parser import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.matcher import get_role_scores
from utils.ai_feedback import generate_feedback

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_page_config(layout="wide")

st.title("🚀 AI Resume Analyzer & Job Matcher")

# Load dataset
df = pd.read_csv("data/jobs.csv")

# Extract all market skills
all_skills = []

for skills in df["skills"].dropna():
    skill_list = str(skills).replace("[","").replace("]","").replace("'","").split(",")
    for s in skill_list:
        all_skills.append(s.strip().lower())

market_skills = list(set(all_skills))

# PDF generator
def generate_pdf(feedback):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    text = c.beginText(40, 750)
    text.setFont("Helvetica", 10)

    for line in feedback.split("\n"):
        text.textLine(line)

    c.drawText(text)
    c.save()

    buffer.seek(0)
    return buffer

# Upload resume
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:

    text = extract_text_from_pdf(uploaded_file)
    user_skills = extract_skills(text, market_skills)

    if not user_skills:
        st.warning("No skills detected. Try another resume.")
        st.stop()

    # Resume Insights
    st.subheader("📊 Resume Insights")
    st.write(f"Total Skills Found: {len(user_skills)}")

    if len(user_skills) < 5:
        st.warning("Your resume has very few detectable skills.")

    # Resume Score
    score = min(len(user_skills) * 10, 100)

    st.subheader("📈 Resume Score")
    st.progress(score)
    st.write(f"Score: {score}/100")

    # Layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💼 Extracted Skills")
        st.write(user_skills)

    with col2:
        st.subheader("🎯 Top Job Matches")

        results = get_role_scores(df, user_skills)

        # Best role
        best_role = results[0][0]
        st.success(f"Best Role for You: {best_role}")

        for role, score in results[:5]:

            role_data = df[df["job_title"] == role]

            role_skills = []
            for skills in role_data["skills"].dropna():
                skill_list = str(skills).replace("[","").replace("]","").replace("'","").split(",")
                for s in skill_list:
                    role_skills.append(s.strip().lower())

            role_skills = list(set(role_skills))

            match_percent = int((score / len(role_skills)) * 100) if len(role_skills) > 0 else 0

            st.write(f"{role} → {match_percent}% Match")

    # Chart
    roles = [r[0] for r in results[:5]]
    scores = [r[1] for r in results[:5]]

    chart_data = pd.DataFrame({
        "Match Score": scores
    }, index=roles)

    st.bar_chart(chart_data)

    # Missing skills
    st.subheader(f"🚀 Skills to Learn for {best_role}")

    role_data = df[df["job_title"] == best_role]

    role_skills = []
    for skills in role_data["skills"].dropna():
        skill_list = str(skills).replace("[","").replace("]","").replace("'","").split(",")
        for s in skill_list:
            role_skills.append(s.strip().lower())

    role_skills = list(set(role_skills))

    missing = [skill for skill in role_skills if skill not in user_skills]

    if missing:
        for skill in missing[:8]:
            st.write(f"👉 {skill}")
    else:
        st.success("You already match this role well!")

    # AI Feedback
    st.subheader("🤖 AI Resume Feedback")

    feedback = generate_feedback(user_skills, best_role)
    st.write(feedback)

    # Download PDF
    pdf = generate_pdf(feedback)

    st.download_button(
        label="📥 Download Feedback as PDF",
        data=pdf,
        file_name="resume_feedback.pdf",
        mime="application/pdf"
    )

    # Tip
    st.info("💡 Tip: Add more relevant skills to improve your job match chances.")