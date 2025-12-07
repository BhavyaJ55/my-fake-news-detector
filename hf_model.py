from transformers import pipeline

# Updated version without deprecated parameter
classifier = pipeline(
    "text-classification", 
    model="distilbert-base-uncased-finetuned-sst-2-english",
    top_k=None  # Instead of return_all_scores=True
)

def predict_text(text):
    result = classifier(text[:1000])
    return result
