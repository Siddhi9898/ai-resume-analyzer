import streamlit as st
import pandas as pd

from utils.parser import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.matcher import get_role_scores
from utils.ai_feedback import generate_feedback

st.set_page_config(layout="wide")

st.title("🚀 AI Resume Analyzer Pro")

# Load dataset
df = pd.read_csv("data/jobs.csv")

# Extract all market skills
all_skills = []

for skills in df["skills"].dropna():
    skill_list = str(skills).replace("[","").replace("]","").replace("'","").split(",")
    for s in skill_list:
        all_skills.append(s.strip().lower())

market_skills = list(set(all_skills))

# Upload resume
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:

    # 🔹 Extract text
    text = extract_text_from_pdf(uploaded_file)
    user_skills = extract_skills(text, market_skills)

    if not user_skills:
        st.warning("No skills detected. Try another resume.")
        st.stop()

    # 🔹 Resume Insights
    st.subheader("📊 Resume Insights")
    st.write(f"Total Skills Found: {len(user_skills)}")

    if len(user_skills) < 5:
        st.warning("Your resume has very few detectable skills. Consider adding more.")

    # 🔹 Resume Score
    st.subheader("📈 Resume Score")

    score = min(len(user_skills) * 10, 100)

    st.progress(score)
    st.write(f"Your Resume Score: {score}/100")

    if score < 40:
        st.error("Weak resume - needs improvement")
    elif score < 70:
        st.warning("Average resume - can be improved")
    else:
        st.success("Strong resume")

    # 🔹 Layout (Skills + Matches)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧠 Extracted Skills")
        st.write(user_skills)

    with col2:
        st.subheader("💼 Top Job Matches")

        results = get_role_scores(df, user_skills)

        for role, score in results[:5]:
            st.write(f"{role} → {score}% Match")

    # 🔹 Chart
    roles = [r[0] for r in results[:5]]
    scores = [r[1] for r in results[:5]]

    chart_data = pd.DataFrame({
        "Match %": scores
    }, index=roles)

    st.bar_chart(chart_data)

    # 🔹 Career Suggestion
    st.subheader("🎯 Career Suggestion")

    best_role, best_score = results[0]

    st.write(f"You are best suited for: **{best_role}**")

    if best_score > 70:
        st.success("You are highly aligned with this role. Start applying!")
    elif best_score > 40:
        st.warning("You are partially ready. Improve missing skills.")
    else:
        st.error("You need significant improvement for this role.")

    # 🔹 Skills to Learn
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

    # 🔹 Skill Analysis
    st.subheader("🧠 Skill Analysis")

    common = list(set(user_skills) & set(role_skills))

    st.write("✅ Your Strengths:")
    for skill in common:
        st.write(f"✔ {skill}")

    st.write("❌ Areas to Improve:")

    if not missing:
        st.info("You match most skills, but you can still improve with advanced topics like:")
    
        extra_suggestions = ["system design", "data structures", "cloud", "docker"]

        for skill in extra_suggestions:
            st.write(f"➕ {skill}")

    # 🔹 AI Feedback Section
    # 🔹 AI Feedback Section
    st.subheader("🧠 AI Resume Feedback")

    if st.button("Generate AI Feedback"):
        with st.spinner("Analyzing your resume..."):
            feedback = generate_feedback(user_skills, best_role)
            st.write(feedback)