# Term Deposit Subscription Predictor

This project contains Python applications that interact with a deployed machine learning model on Google Cloud's Vertex AI to predict whether a bank client will subscribe to a term deposit. It includes both a command-line tool and a Flask-based REST API.

## Overview

This project demonstrates two ways to consume a deployed machine learning model as a service:

1.  A **command-line script** (`src/predict.py`) that sends client data from a local JSON file to a live Vertex AI model endpoint.
2.  A **Web Application** (`src/app.py`) built with Flask that provides:
    - A user-friendly web interface (`/`) to get predictions from a form.
    - A REST API endpoint (`/predict`) to receive prediction requests over HTTP.

These applications serve as a practical guide to MLOps and cloud engineering principles.

### Features

- **Vertex AI Integration:** Connects to a live Vertex AI Endpoint to get real-time predictions.
- **REST API:** A Flask-based web service to get predictions via HTTP POST requests.
- **Web Interface:** A simple HTML/JavaScript frontend for interactive predictions in the browser.
- **Dynamic Configuration:** Uses environment variables to configure the GCP `PROJECT_ID`, `REGION`, and `ENDPOINT_ID`, avoiding hard-coded values.
- **Data-driven:** Reads client data for prediction from an external `instances.json` file, allowing for easy testing with different inputs without modifying the code.
- **Clear & Parsed Output:** Parses the model's raw JSON response to provide a clean, human-readable prediction, confidence score, and a list of all class scores.

## Technology Stack

- **Language:** Python 3
- **Platform:** Google Cloud Platform (GCP)
- **Key Services:**
    - Vertex AI Endpoints for model serving
    - Cloud Shell for execution environment
- **Libraries:**
    - `google-cloud-aiplatform`: For interacting with Vertex AI.
    - `Flask`: For the web API server.
    - `gunicorn`: For running the Flask app in production.

## Prerequisites
Before running this script, ensure you have the following:

1.  A Google Cloud Project with the **Vertex AI API** enabled.
2.  A model successfully trained and deployed to a **Vertex AI Endpoint**.
3.  The `gcloud` command-line tool installed and authenticated (`gcloud auth application-default login`).
4.  Python 3 and the required Google Cloud SDK installed:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

1.  **Clone the repository (if applicable):**
    ```sh
    git clone https://github.com/your-username/term-deposit-predictor.git
    cd term-deposit-predictor
    ```

2.  **Set Environment Variables:**
    In your terminal, export the necessary environment variables. Replace the placeholder values with your actual GCP configuration.
    ```sh
    export PROJECT_ID="your-gcp-project-id"
    export REGION="your-model-region"
    export ENDPOINT_ID="your-endpoint-id"
    ```

3.  **Prepare Input Data (for `predict.py`):**
    Create a file named `instances.json` in the project's root directory. This file should contain a JSON list of client records to be predicted.
    
    *Example `instances.json` in project root:*
    ```json
    [
      {
        "Age": "45.0", "Job": "technician", "MaritalStatus": "married", "Education": "secondary", "Default": "no", "Balance": "800.0", "Housing": "yes", "Loan": "no", "Contact": "cellular", "Day": "16.0", "Month": "may", "Duration": "180.0", "Campaign": "1.0", "PDays": "-1.0", "Previous": "0.0", "POutcome": "unknown"
      }
    ]
    ```

### Option 1: Run the Command-Line Script

Execute the script from the project's root directory. You can optionally pass a path to an instances file as an argument.
```sh
python3 src/predict.py
```

#### Example CLI Output

A successful run will produce output similar to the following:
```
Accessing endpoint: projects/AMCAD/locations/us-central1/endpoints/3893818931389
Loading instances from: instances.json
Sending prediction request...
...prediction request complete.

--- Prediction Results ---

Instance #1:
  ✅ Predicted class: 1
  ✅ Confidence: 0.9805 (98.05%)
  All scores: [('1', 0.980525016784668), ('2', 0.01947491802275181)]

--- Raw Vertex AI Response ---
Raw Vertex AI response:
Prediction(predictions=[{'classes': ['1', '2'], 'scores': [0.980525016784668, 0.01947491802275181]}], deployed_model_id='401032022824321024', metadata=None, model_version_id='1', model_resource_name='projects/461746078421/locations/us-central1/models/7503514849175928832', explanations=None)
```
