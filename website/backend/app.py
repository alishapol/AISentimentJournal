# FastAPI framework for building the backend API
from fastapi import FastAPI
# Middleware to allow frontend JavaScript to call the API
from fastapi.middleware.cors import CORSMiddleware
# OS utilities for file paths and directories
import os
import json
import pytz
from datetime import datetime

# Add the project root folder to Python’s import path
import sys
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

# Import the AI analysis function used by the frontend and CLI
from journal_logic import analyze_entry

# Path to the shared journal JSON file used across the project
JOURNAL_PATH = os.path.join(ROOT_DIR, "journal_entries.json")

# Creates a PST timestamp string for saved entries
def get_pst_timestamp():
    pst = pytz.timezone("America/Los_Angeles")
    now = datetime.now(pst)
    return now.strftime("%B %d, %Y — %-I:%M %p (PST)")

# Reads previously saved journal entries
def load_entries():
    if not os.path.exists(JOURNAL_PATH):
        return []
    with open(JOURNAL_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Saves updated entries back to disk
def save_entries(entries):
    with open(JOURNAL_PATH, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)

# Create the FastAPI application instance
app = FastAPI()

# Allow all origins so the local frontend can request data freely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint that analyzes text and returns sentiment/emotion/stress/energy
@app.post("/analyze")
async def analyze(payload: dict):
    text = payload.get("text", "").strip()
    result = analyze_entry(text)
    return {"analysis": result}

# Endpoint that analyzes text, saves it, and returns the stored entry
@app.post("/add")
async def add(payload: dict):
    text = payload.get("text", "").strip()
    result = analyze_entry(text)

    # Build the entry object with timestamp + AI tags
    entry = {
        "timestamp": get_pst_timestamp(),
        "text": text,
        "tags": result,
    }

    # Save entry to journal file
    entries = load_entries()
    entries.append(entry)
    save_entries(entries)

    return {"saved": entry}

# Endpoint that returns the last three journal entries
@app.get("/last")
async def last():
    entries = load_entries()
    return {"entries": entries[-3:]}

# Endpoint that returns all journal entries
@app.get("/all")
async def all_entries():
    return {"entries": load_entries()}