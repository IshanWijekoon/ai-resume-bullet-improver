import re

def calculate_ats_score(text):
    score = 0

    verbs = ["led", "built", "developed", "improved", "increased", "reduced"]
    if any(v in text.lower() for v in verbs):
        score += 30

    if re.search(r"\d+", text):
        score += 30

    if 10 <= len(text.split()) <= 25:
        score += 20

    if "," not in text:
        score += 20

    return min(score, 100)