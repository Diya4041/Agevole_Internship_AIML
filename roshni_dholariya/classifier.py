# classifier.py
import joblib

clf = joblib.load('resume_classifier.joblib')

def predict_category(resume_text):
    return clf.predict([resume_text])[0]
