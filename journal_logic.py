# journal_logic.py

import os
# Suppress noisy warnings/log messages from transformers and PyTorch
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["PYTORCH_MPS_LOG_LEVEL"] = "3"

import json
import pytz
from datetime import datetime

from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from datasets import load_dataset

# Models

# Standard sentiment classifier (positive/negative)
sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
)

# Emotion classifier that returns the strongest predicted emotion
emotion_model = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=1
)

# SBERT model used for semantic similarity checks
sbert_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# Datasets

# Load SST-2 dataset and split into positive and negative sample sentences
sst2 = load_dataset("sst2")
sst2_pos = [x["sentence"] for x in sst2["train"] if x["label"] == 1][:200]
sst2_neg = [x["sentence"] for x in sst2["train"] if x["label"] == 0][:200]

# Load GoEmotions dataset to extract extra positive/negative examples
goemo = load_dataset("google-research-datasets/go_emotions")
label_feature = goemo["train"].features["labels"].feature

# Define which emotions we consider positive or negative
positive_labels = {"admiration", "amusement", "joy"}
negative_labels = {"anger", "annoyance", "disappointment", "disgust", "fear", "sadness"}

go_pos, go_neg = [], []

# Go through each row and categorize based on emotion labels
for row in goemo["train"]:
    emotion_names = [label_feature.int2str(l) for l in row["labels"]]
    if any(e in positive_labels for e in emotion_names):
        go_pos.append(row["text"])
    if any(e in negative_labels for e in emotion_names):
        go_neg.append(row["text"])

# Limit dataset size to keep embeddings manageable
go_pos, go_neg = go_pos[:200], go_neg[:200]

# Load local sentiment files (Amazon/IMDB/Yelp) if they exist
def _load_local_sentiment_files(base_path="data"):
    files = ["amazon_cells_labelled.txt", "imdb_labelled.txt", "yelp_labelled.txt"]
    local_pos, local_neg = [], []

    for fname in files:
        path = os.path.join(base_path, fname)
        # Warn if optional dataset files are missing
        if not os.path.exists(path):
            print(f"WARNING: Missing local dataset file: {path}")
            continue

        # Read local dataset and separate by label (1 = positive)
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().rsplit("\t", 1)
                if len(parts) != 2:
                    continue
                sent, label = parts
                if label == "1":
                    local_pos.append(sent)
                else:
                    local_neg.append(sent)

    return local_pos, local_neg


local_pos, local_neg = _load_local_sentiment_files()

# Combine all datasets into unified positive/negative text lists
positive_texts = sst2_pos + go_pos + local_pos
negative_texts = sst2_neg + go_neg + local_neg

# Precompute embeddings for all positive and negative reference texts
positive_embeddings = sbert_model.encode(
    positive_texts, convert_to_tensor=True, normalize_embeddings=True
)

negative_embeddings = sbert_model.encode(
    negative_texts, convert_to_tensor=True, normalize_embeddings=True
)

# Use HuggingFace sentiment model
def _classify_sentiment(text):
    result = sentiment_model(text)[0]
    return result["label"].lower(), result["score"]

# Use HuggingFace emotion model (handles different return formats)
def _classify_emotion(text):
    raw = emotion_model(text)
    if isinstance(raw[0], list):
        raw = raw[0][0]
    else:
        raw = raw[0]
    return raw["label"].lower(), raw.get("score", 0.0)

# SBERT similarity check to adjust sentiment for more nuance
def _semantic_sentiment_refinement(text, sentiment):
    emb = sbert_model.encode(text, convert_to_tensor=True, normalize_embeddings=True)
    pos_sim = util.cos_sim(emb, positive_embeddings).max().item()
    neg_sim = util.cos_sim(emb, negative_embeddings).max().item()
    diff = abs(pos_sim - neg_sim)

    NEUTRAL_THRESHOLD = 0.04
    LOW_EMO = ["fine", "meh", "okay", "neutral", "alright"]

    # If similarities are too close or user expresses low emotion, classify as neutral
    if diff < NEUTRAL_THRESHOLD or any(w in text.lower() for w in LOW_EMO):
        return "neutral"

    # Otherwise whichever similarity is stronger becomes the sentiment
    return "positive" if pos_sim > neg_sim else "negative"

# Basic stress inference based on sentiment + emotion
def _infer_stress(sentiment, emotion):
    if emotion in ["fear", "sadness", "anger"]:
        return "high"
    if sentiment == "negative":
        return "medium"
    return "low"

# Basic energy inference based on emotional tone
def _infer_energy(emotion):
    if emotion in ["joy", "surprise"]:
        return "high"
    if emotion in ["fear", "sadness"]:
        return "low"
    return "medium"

def analyze_entry(text: str):
    cleaned = text.strip()
    # Reject empty input early
    if not cleaned:
        return {"error": "empty"}

    lowered = cleaned.lower()


    # If user writes a sentence with "but", we treat the clause after "but" as more important for the sentiment/emotion
    # Example: "I'm tired but I'm proud" → analyze "I'm proud"
    if " but " in lowered:
        after_but = cleaned.lower().split(" but ", 1)[1].strip()
        if after_but:
            cleaned = after_but
            lowered = cleaned.lower()

    # First pass classification using HF models
    sentiment_label, _ = _classify_sentiment(cleaned)
    emotion_label, _ = _classify_emotion(cleaned)

    # SBERT refinement step to account for subtle or ambiguous wording
    sentiment_label = _semantic_sentiment_refinement(cleaned, sentiment_label)

    # Slang lists override any earlier classification if matched
    slang_positive = [
        "killing it","killed it","kill it","crushing it","crushed it","crush it",
        "slay","slayed","slaying","fire","🔥","on fire","went crazy","go crazy",
        "going crazy","pop off","popped off","popping off","ate","ate that",
        "ate it up","ate and left no crumbs","slayed so hard","so proud of myself",
        "i did amazing","i’ll do amazing","i’m about to crush it","i’m about to kill it",
        "winning today","i won today","today was a win","feeling unstoppable",
        "feeling great","feeling good","good vibes","big w","major w","huge w",
    ]

    slang_negative = [
        "done with today","so done","i'm done","im done","i’m so done","over this",
        "over it","fed up","can’t do this","cant do this","💀","dead","i'm dead",
        "had me crying","i'm losing it","losing it","lost it today","i can't anymore",
        "cant anymore","i can't","i literally can't","bad vibes","today was an l",
        "took an l","taking an l","huge l","major l","burnt out","so stressed",
        "i hate today","today sucked","it sucked","this sucks","sucks so bad",
        "feels awful","feeling terrible","having a rough one","rough day",
        "today bodied me","i got wrecked today",
    ]

    # Check slang to override sentiment if needed
    if any(s in lowered for s in slang_positive):
        sentiment_label = "positive"
    elif any(s in lowered for s in slang_negative):
        sentiment_label = "negative"

    # Compute stress and energy based on final sentiment + emotion
    stress_level = _infer_stress(sentiment_label, emotion_label)
    energy_level = _infer_energy(emotion_label)

    # Final combined result for the API
    return {
        "sentiment": sentiment_label,
        "emotion": emotion_label,
        "stress": stress_level,
        "energy": energy_level,
    }