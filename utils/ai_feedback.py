from openai import OpenAI

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_feedback(user_skills, best_role):

    prompt = f"""
    You are a career coach.

    Analyze this candidate:

    Skills: {user_skills}
    Target Role: {best_role}

    Give:
    1. Short resume summary
    2. Strengths
    3. Weaknesses
    4. Suggestions to improve
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content