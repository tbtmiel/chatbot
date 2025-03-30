from flask import Blueprint, request, jsonify
from app.model_loader import model, vectorizer, answer_df
import json
import numpy as np


routes = Blueprint("routes", __name__)

def preprocess_input(text):
    return text.lower()

@routes.route("/")
def home():
    return "Flask is running"

@routes.route("/classify", methods=["POST"])
def classify_message():
    try:
        # Log raw data for debugging
        print("Raw request data:", request.data)

        # Parse JSON request
        try:
            data = request.get_json(force=True)
        except Exception as json_error:
            print("Flask JSON parsing failed:", str(json_error))
            if not request.data:
                return jsonify({"error": "No data provided"}), 400
            data = json.loads(request.data.decode("utf-8"))

        print("Parsed data:", data)

        if not data or "message" not in data:
            return jsonify({"error": "No message provided"}), 400

        user_input = data["message"]
        processed_input = preprocess_input(user_input)

        print("Processed input:", processed_input)

        # Vectorize input
        input_vectorized = vectorizer.transform([processed_input])
        print("Vectorized input shape:", input_vectorized.shape)

        # Check feature mismatch
        if input_vectorized.shape[1] != model.n_features_in_:
            return jsonify({"error": f"Feature mismatch: Model expects {model.n_features_in_} features, but got {input_vectorized.shape[1]}"}), 400

        # Predict label
        label = model.predict(input_vectorized)[0]
        print("Predicted label:", label)
        probabilities = model.predict_proba(input_vectorized)
        confidence = np.max(probabilities) * 100  # % percentage

        
        if confidence > 4:
            # Find answer
            response = (
                answer_df[answer_df["label"] == label]["answer"].iloc[0]
                if label in answer_df["label"].values
                else "Sorry, I don’t understand."
            )
        else:
            response = "Tôi không hiểu câu hỏi, vui lòng hỏi lại."

        # # Find answer
        # response = (
        #     answer_df[answer_df["label"] == label]["answer"].iloc[0]
        #     if label in answer_df["label"].values
        #     else "Sorry, I don’t understand."
        # )

        print("Bot response:", response)
        return jsonify({"response": str(response)})

    except ValueError as e:
        print("JSON parsing error:", str(e))
        return jsonify({"error": f"Invalid JSON: {str(e)}"}), 400
    except Exception as e:
        print("General error:", str(e))
        return jsonify({"error": str(e)}), 500
