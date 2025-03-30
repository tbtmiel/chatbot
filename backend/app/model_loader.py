import joblib
import pandas as pd

model = joblib.load("./models/svm_model.pkl")
vectorizer = joblib.load("./models/tfidf_vectorizer.pkl")

print(f"{model.n_features_in_} features")
print(f"{len(vectorizer.get_feature_names_out())} features")

# Load answers from CSV
answer_df = pd.read_csv("./data/answer.csv")
qn_df = pd.read_csv("./data/question.csv")

