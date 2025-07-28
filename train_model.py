import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
import joblib
import os

# Load the dataset
df = pd.read_csv("review_dataset.csv")

# Features and targets
X = df["paper_text"]
y_clarity = df["clarity_score"]
y_novelty = df["novelty_score"]
y_citation = df["citation_strength"]

# Create a directory for models if it doesn't exist
os.makedirs("models", exist_ok=True)

# Function to train and save a model
def train_and_save_model(y, model_name):
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("regressor", LinearRegression())
    ])
    pipeline.fit(X, y)
    joblib.dump(pipeline, f"models/{model_name}.pkl")
    print(f"{model_name} model saved.")

# Train and save each model
train_and_save_model(y_clarity, "clarity_model")
train_and_save_model(y_novelty, "novelty_model")
train_and_save_model(y_citation, "citation_model")
