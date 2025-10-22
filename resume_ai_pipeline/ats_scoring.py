import re
from sklearn.feature_extraction.text import CountVectorizer

def normalize(text):
    return re.sub(r'[^a-z0-9+ ]', ' ', text.lower())

def ats_score(resume_text: str, job_description: str):
    """
    Calculates overlap between resume and JD keywords.
    Returns: (score %, matched keywords, missing keywords)
    """
    resume = normalize(resume_text)
    jd = normalize(job_description)

    # build vocabulary from JD
    vectorizer = CountVectorizer(stop_words='english')
    jd_vec = vectorizer.fit_transform([jd])
    resume_vec = vectorizer.transform([resume])

    jd_terms = vectorizer.get_feature_names_out()
    jd_counts = jd_vec.toarray()[0]
    resume_counts = resume_vec.toarray()[0]

    matched, missing = [], []
    for term, cnt in zip(jd_terms, jd_counts):
        if cnt == 0: continue
        if resume_counts[list(jd_terms).index(term)] > 0:
            matched.append(term)
        else:
            missing.append(term)

    score = (len(matched) / max(len(matched) + len(missing), 1)) * 100
    return round(score, 2), matched, missing

# quick test
if __name__ == "__main__":
    resume = "Skilled in Python, machine learning, SQL, and AWS cloud."
    jd = "We need expertise in Python, ML, data analysis, Azure."
    score, matched, missing = ats_score(resume, jd)
    print("ATS Score:", score)
    print("Matched:", matched)
    print("Missing:", missing)
