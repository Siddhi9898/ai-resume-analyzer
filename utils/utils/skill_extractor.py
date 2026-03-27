import re

def extract_skills(text, skill_list):

    found_skills = []

    for skill in skill_list:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found_skills.append(skill)

    return list(set(found_skills))

import re

def extract_skills(text, skill_list):

    found_skills = []

    for skill in skill_list:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found_skills.append(skill)

    return list(set(found_skills))