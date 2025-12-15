from flask import Flask, request, jsonify
from models import MODEL_REGISTRY, run_model, USE_CASE_REGISTRY

app = Flask(__name__)

# Endpoint: /crane/run
@app.route("/crane/run", methods=["POST"])
def run():
    data = request.json
    model_id = data.get("model_id")
    user_input = data.get("input")
    options = data.get("options", {})

    if not model_id or not user_input:
        return jsonify({"error": "model_id and input are required"}), 400

    if model_id not in MODEL_REGISTRY:
        return jsonify({"error": "Unknown model_id"}), 400

    # Call the model inference function
    output, metadata = run_model(model_id, user_input, options)
    return jsonify({"output": output, "metadata": metadata})


# Endpoint: /crane/models
@app.route("/crane/models", methods=["GET"])
def list_models():
    models = [{"id": m["id"], "name": m["name"], "description": m["description"]} 
              for m in MODEL_REGISTRY.values()]
    return jsonify(models)


# Endpoint: /crane/use-cases
@app.route("/crane/use-cases", methods=["GET"])
def list_use_cases():
    # Static or DB-driven
    use_cases = [
        {"id": uc["id"], "category": uc["category"], "description": uc["description"], "prompt": uc["prompt"]}
        for uc in USE_CASE_REGISTRY
    ]
    return jsonify(use_cases)


# Endpoint: /crane/architecture
@app.route("/crane/architecture", methods=["GET"])
def architecture():
    # Return static architecture info
    return jsonify({
        "layers": [
            {"name": "Input Layer", "type": "text", "description": "Receives input text"},
            {"name": "Embedding Layer", "type": "vector", "description": "Transforms text into embeddings"},
            {"name": "Transformer Encoder", "type": "ML", "description": "Processes embeddings with attention layers"},
        ]
    })


# Endpoint: /crane/trust
@app.route("/crane/trust", methods=["GET"])
def trust():
    # Return static trust/governance info
    return jsonify({
        "data_locality": "EU",
        "hosting_region": "Frankfurt, Germany",
        "governance": "Complies with GDPR and ISO 27001"
    })


# Run Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
