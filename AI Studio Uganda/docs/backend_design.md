# Backend Implementation Design

## 1. Reference Implementation

The backend is implemented as a Flask application, structured into two main modules:

*   **`backend/crane_api.py`**: The API Gateway / Controller. Handles request validation, routing, and response formatting.
*   **`backend/models.py`**: The Inference Engine. Managers the Model Registry and maps logical `model_id`s to actual Hugging Face pipelines.

## 2. Core Logic: `POST /crane/run`

The unifying controller that dispatches tasks to specific model pipelines.

### Implementation Reference (`backend/crane_api.py`)

```python
@app.route("/crane/run", methods=["POST"])
def run():
    data = request.json
    model_id = data.get("model_id")
    user_input = data.get("input")
    options = data.get("options", {})

    # Validation
    if not model_id or not user_input:
        return jsonify({"error": "model_id and input are required"}), 400

    # Dispatch to Inference Engine
    output, metadata = run_model(model_id, user_input, options)
    return jsonify({"output": output, "metadata": metadata})
```

## 3. Hugging Face Inference Mapping

We map our API models to Hugging Face models using a `MODEL_REGISTRY`.

### Registry Structure (`backend/models.py`)

```python
MODEL_REGISTRY = {
    "text-summarizer-v1": {
        "id": "text-summarizer-v1", 
        "hf_model": "facebook/bart-large-cnn", 
        "type": "summarization"
    },
    # ...
}
```

### Adapter Logic

The `run_model` function dynamically loads the correct pipeline:

1.  Checks if `model_id` exists in registry.
2.  Retrieves (or lazily loads) the corresponding Hugging Face pipeline.
3.  Maps `options` (like `max_tokens`) to HF specific kwargs (like `max_length`).
4.  Standardizes the output format (extracting text from list/dict results).

## 4. Rate Limits & Quotas

(Planned for Reference Architecture)

*   **Free Tier**: 60 requests/minute
*   **Pro Tier**: 600 requests/minute
*   **Implementation**: Can be added as a Flask `before_request` middleware using Redis.
