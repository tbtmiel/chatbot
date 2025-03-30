import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import joblib
import os

# Absolute path to dir containing train.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Absolute path to CSV file
data_path = os.path.join(BASE_DIR, "data", "question.csv")

# Load data
qn_df = pd.read_csv(data_path)
X_train = qn_df["question_content"].values
y_train = qn_df["category_id"].values

# Train vectorizer
vectorizer = TfidfVectorizer(ngram_range=(1, 3), analyzer='char_wb')
X_train_tfidf = vectorizer.fit_transform(X_train)

# Train model
model = SVC(kernel='linear', probability=True, C=10)
model.fit(X_train_tfidf, y_train)

# Save files

svm_model_path = os.path.join(BASE_DIR, "models", "svm_model.pkl")
tfidf_path = os.path.join(BASE_DIR, "models", "tfidf_vectorizer.pkl")

joblib.dump(vectorizer, tfidf_path)
joblib.dump(model, svm_model_path)
print("✅ Model & Vectorizer đã được train và lưu!")
