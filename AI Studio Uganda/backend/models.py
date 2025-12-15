from transformers import pipeline

# Example registry of models
# Expanded to include 'id', 'name', 'description' fields used by the API
MODEL_REGISTRY = {
    "text-summarizer-v1": {
        "id": "text-summarizer-v1",
        "name": "Text Summarizer",
        "description": "Summarizes long articles into short summaries",
        "type": "summarization",
        "hf_model": "facebook/bart-large-cnn"
    },
    "sentiment-analyzer-v2": {
        "id": "sentiment-analyzer-v2",
        "name": "Sentiment Analyzer",
        "description": "Analyzes sentiment of text",
        "type": "sentiment-analysis",
        "hf_model": "distilbert-base-uncased-finetuned-sst-2-english"
    }
}

# Use Case Registry (added to match API usage)
USE_CASE_REGISTRY = [
    {
        "id": "agriculture-summary",
        "category": "Agriculture",
        "description": "Summarize crop reports",
        "prompt": "Summarize this crop report data..."
    }
]

# Pre-load HF pipelines
# Note: In a real production env, lazy loading or separate inference servers would be used.
HF_PIPELINES = {}
try:
    for k, v in MODEL_REGISTRY.items():
        HF_PIPELINES[k] = pipeline(v["type"], model=v["hf_model"])
except Exception as e:
    print(f"Warning: Could not load local HF pipelines. Ensure transformers/torch are installed. Error: {e}")


def run_model(model_id, input_text, options):
    if model_id not in HF_PIPELINES:
         # Fallback for when libraries aren't installed or model load failed
         return f"Simulated output for {input_text[:20]}...", {"model_version": "simulated"}

    hf_pipeline = HF_PIPELINES[model_id]
    
    # Pass options like max_length, temperature if supported by the specific pipeline
    # Be careful filtering relevant kwargs for specific pipelines
    gen_kwargs = {}
    if "max_tokens" in options:
        gen_kwargs["max_length"] = options["max_tokens"]
    
    try:
        result = hf_pipeline(input_text, **gen_kwargs)
        
        # Output parsing depends on task type
        output = ""
        if model_id.startswith("text-summarizer"):
            output = result[0]["summary_text"] 
        elif "sentiment" in model_id:
             output = str(result[0])
        else:
            output = str(result)
            
        metadata = {"model_version": MODEL_REGISTRY[model_id]["hf_model"]}
        return output, metadata
    except Exception as e:
        return f"Error running model: {str(e)}", {"error": True}
