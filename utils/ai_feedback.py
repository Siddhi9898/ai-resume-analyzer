import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_feedback(user_skills, best_role):

    feedback = f"🎯 Target Role: {best_role}\n\n"

    if len(user_skills) > 8:
        feedback += "✅ Strong resume with good skill coverage.\n\n"
    else:
        feedback += "⚠️ Your resume lacks sufficient skills.\n\n"

    feedback += "💪 Strengths:\n"
    for skill in user_skills[:5]:
        feedback += f"- {skill}\n"

    feedback += "\n📉 Areas to Improve:\n"
    feedback += "- Add more industry-relevant skills\n"
    feedback += "- Include projects and experience\n"
    feedback += "- Improve resume keywords\n"

    feedback += "\n🚀 Suggestions:\n"
    feedback += "- Work on real-world projects\n"
    feedback += "- Learn advanced tools in your domain\n"
    feedback += "- Tailor resume for each job\n"

    return feedback