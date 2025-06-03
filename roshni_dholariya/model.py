# # model.py
# from sentence_transformers import SentenceTransformer, util

# bert = SentenceTransformer('all-MiniLM-L6-v2')

# def compute_similarity(jd, resumes):
#     jd_embed = bert.encode(jd, convert_to_tensor=True)
#     res_embed = bert.encode(resumes, convert_to_tensor=True)
#     scores = util.cos_sim(jd_embed, res_embed)[0]
#     return scores.tolist()
# model.py
# import joblib
# import numpy as np
# from sentence_transformers import SentenceTransformer, util
# from sklearn.pipeline import Pipeline
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression

# # Load Sentence-BERT model
# bert_model = SentenceTransformer('all-MiniLM-L6-v2')

# def get_similarity_scores(jd_text, resumes):
#     jd_embedding = bert_model.encode(jd_text, convert_to_tensor=True)
#     resume_embeddings = bert_model.encode(resumes, convert_to_tensor=True)
#     similarities = util.cos_sim(jd_embedding, resume_embeddings)[0]
#     return similarities.cpu().numpy()

# def train_resume_classifier(df):
#     pipeline = Pipeline([
#         ('tfidf', TfidfVectorizer()),
#         ('clf', LogisticRegression(max_iter=200))
#     ])
#     pipeline.fit(df['resume'], df['category'])
#     joblib.dump(pipeline, 'resume_classifier.pkl')

# def load_classifier():
#     return joblib.load('resume_classifier.pkl')
# model.py
import joblib
from sentence_transformers import SentenceTransformer, util

bert_model = SentenceTransformer('all-MiniLM-L6-v2')

def get_similarity_scores(jd_text, resumes):
    jd_embedding = bert_model.encode(jd_text, convert_to_tensor=True)
    resume_embeddings = bert_model.encode(resumes, convert_to_tensor=True)
    similarities = util.cos_sim(jd_embedding, resume_embeddings)[0]
    return similarities.cpu().numpy()

def load_classifier():
    return joblib.load('resume_classifier.joblib')  # <-- Updated filename
