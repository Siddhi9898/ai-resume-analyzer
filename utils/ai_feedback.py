import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_feedback(user_skills, best_role):

    prompt = f"""
    You are a career coach.

    Skills: {user_skills}
    Target Role: {best_role}

    Give:
    1. Short summary
    2. Strengths
    3. Weaknesses
    4. Suggestions
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response["choices"][0]["message"]["content"]

    except Exception as e:
        return "⚠️ AI feedback is currently unavailable. Please try again later."