import os
from flask import Flask, request, jsonify, render_template
from google.cloud import aiplatform
from flask import Flask, request, jsonify
app = Flask(__name__, template_folder='templates')

def get_env_var(var_name: str) -> str:
    """Gets an environment variable or raises an error if it's not set."""
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"Error: Environment variable {var_name} is not set.")
    return value

try:
    PROJECT_ID = get_env_var("PROJECT_ID")
    REGION = get_env_var("REGION")
    ENDPOINT_ID = get_env_var("ENDPOINT_ID")
    aiplatform.init(project=PROJECT_ID, location=REGION)
    endpoint = aiplatform.Endpoint(f"projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}")
except ValueError as e:
    print(f"Configuration error: {e}")
    endpoint = None


@app.get("/health")
def health():
    return jsonify({
        "message": "Term Deposit Prediction API is live",
        "status": "running",
        "usage": "POST /predict with JSON body"
    })

@app.get("/")
def home():
    """Renders the main user interface page."""
    return render_template("index.html")

@app.post("/predict")
def predict():
    """
    Prediction endpoint that accepts client data and returns a prediction.
    """
    try:
        # Get the JSON data from the request body
        instances = request.get_json()
        if not instances or not isinstance(instances, list):
            return (
                jsonify(
                    {
                        "error": "Invalid input: body must be a JSON list of instances."
                    }
                ),
                400,
            )

        if not endpoint:
            return jsonify({"error": "Server is not configured correctly. Check environment variables."}), 503

        # The AI Platform services require instance lists.
        response = endpoint.predict(instances=instances)

        # Parse the prediction results
        results = []
        for pred in response.predictions:
            # Zip classes and scores to maintain their association
            pairs = list(zip(pred.get("classes", []), pred.get("scores", [])))
            if not pairs:
                results.append({"error": "Malformed prediction response from model."})
                continue

            # Sort by score to find the top prediction
            pairs_sorted = sorted(pairs, key=lambda x: x[1], reverse=True)
            top_class, top_score = pairs_sorted[0]

            results.append({
                "prediction": top_class, 
                "probability": top_score
            })

        return jsonify(results)

    except Exception as e:
        # Log the exception for debugging
        print(f"An error occurred: {e}")
        return jsonify({"error": "An internal error occurred."}), 500


if __name__ == "__main__":
    # Run the app on port 8080, accessible from any IP
    app.run(host="0.0.0.0", port=8080, debug=True)