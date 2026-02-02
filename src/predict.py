from google.cloud import aiplatform
import os
import sys
import json

def main():
    """Main function to get predictions from a Vertex AI endpoint."""

    def get_env_var(var_name: str) -> str:
        """Gets an environment variable or exits if it's not set."""
        value = os.environ.get(var_name)
        if not value:
            sys.exit(f"Error: Environment variable {var_name} is not set.")
        return value

    project_id = get_env_var("PROJECT_ID")
    region = get_env_var("REGION")
    endpoint_id = get_env_var("ENDPOINT_ID")

    aiplatform.init(project=project_id, location=region)

    endpoint_name = f"projects/{project_id}/locations/{region}/endpoints/{endpoint_id}"
    print(f"Accessing endpoint: {endpoint_name}")
    endpoint = aiplatform.Endpoint(endpoint_name)

    # --- Robust Path Handling ---
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to the project root
    project_root = os.path.dirname(script_dir)
    # Read instances from a JSON file
    instances_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(project_root, "instances.json")
    print(f"Loading instances from: {instances_file}")
    try:
        with open(instances_file, "r") as f:
            instances = json.load(f)
    except FileNotFoundError:
        sys.exit(f"Error: Instance file not found at '{instances_file}'")
    except json.JSONDecodeError:
        sys.exit(f"Error: Could not decode JSON from '{instances_file}'")

    print("Sending prediction request...")
    response = endpoint.predict(instances=instances)
    print("...prediction request complete.")

    print("\n--- Prediction Results ---")
    for i, pred in enumerate(response.predictions):
        # Parse top class + confidence
        pairs = list(zip(pred.get("classes", []), pred.get("scores", [])))
        pairs_sorted = sorted(pairs, key=lambda x: x[1], reverse=True)

        top_class, top_score = pairs_sorted[0]
        print(f"\nInstance #{i+1}:")
        print(f"  ✅ Predicted class: {top_class}")
        print(f"  ✅ Confidence: {top_score:.4f} ({top_score*100:.2f}%)")
        print(f"  All scores: {pairs_sorted}")

    print("\n--- Raw Vertex AI Response ---")
    print("Raw Vertex AI response:")
    print(response)

if __name__ == "__main__":
    main()
