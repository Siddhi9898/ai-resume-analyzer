from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_role_scores(df, user_skills):

    # Safety check
    if not user_skills:
        return []

    user_text = " ".join(user_skills)

    role_scores = {}

    for role in df["job_title"].unique():

        role_data = df[df["job_title"] == role]

        role_skills_list = []

        for skills in role_data["skills"].dropna():
            skill_list = str(skills).replace("[","").replace("]","").replace("'","").split(",")
            for s in skill_list:
                clean_skill = s.strip().lower()
                if clean_skill:
                    role_skills_list.append(clean_skill)

        # If no skills found → skip
        if not role_skills_list:
            continue

        role_text = " ".join(role_skills_list)

        try:
            vectorizer = TfidfVectorizer()

            vectors = vectorizer.fit_transform([user_text, role_text])

            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

            role_scores[role] = int(similarity * 100)

        except:
            # If TF-IDF fails → fallback to basic matching
            common = set(user_skills) & set(role_skills_list)
            score = int((len(common) / len(role_skills_list)) * 100) if role_skills_list else 0
            role_scores[role] = score

    return sorted(role_scores.items(), key=lambda x: x[1], reverse=True)