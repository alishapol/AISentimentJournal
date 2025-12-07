# AI-Powered Emotional Journaling System
- A full-stack NLP project using transformers, semantic similarity, slang intelligence, and real-time emotional inference.
- This project is a fully integrated emotional journaling system powered by modern NLP models, custom semantic analysis, and a dual-interface design. Users can analyze their emotions and daily experiences through either a command-line interface or a web application, both of which share the same AI engine and write to a unified journal_entries.json file.
- The system focuses on emotional clarity, mental-state reflection, and intuitive user experience.

# Key Features
* Advanced NLP Emotion Engine
The emotional analysis pipeline combines multiple state-of-the-art models:
- DistilBERT SST-2 for baseline sentiment (positive, negative, neutral)
- DistilRoBERTa emotion classifier for emotions like joy, fear, sadness, anger, and surprise
- SBERT (SentenceTransformer MiniLM-L6-v2) for semantic similarity refinement
- Custom datasets (SST-2, GoEmotions, UCI Amazon/IMDb/Yelp) to build a 1000+ sample embedding space
- Slang-aware override system to interpret modern expressions like “killing it,” “slayed,” “big W,” “dead 💀,” “rough day,” etc.
- “But-clause emotional logic” → If a sentence contains "but," the system analyzes only the part after "but," reflecting human emotional weighting

This multi-layer approach produces four final tags per entry:
1. Sentiment
2. Emotion
3. Stress level
4. Energy level

# Unified Architecture
* The system is intentionally modular and easy to expand.
Core Components
- journal_logic.py — the full AI engine
- journal_cli.py — terminal interface for adding entries and viewing summaries
- FastAPI backend (app.py) — exposes /analyze, /add, /last, and /all endpoints
- Frontend (HTML/CSS/JS) — clean browser-based journaling dashboard
- Shared data store: journal_entries.json (used by both CLI and website)

* PST Timestamping
Every saved entry uses a polished, human-friendly timestamp format like "December 7, 2025 - 5:00 PM (PST)

# Command-Line Interface (CLI)
* Important: start at root directory

* How to add a new journal entry:
   - python3 journal_cli.py add "I had a really bad day at work today."

* How to view last three journal entries:
   - python3 journal_cli.py summary


# Web Application
* Important: start at backend to load app (must cd to backend folder)

* Step 1: How to load web app from VSCode terminal:
- uvicorn app:app --reload

* Step 2: How to open frontend:
- In VSCode, click on right click index.html file and select "Open With Live Server"

* Website Features:
- Analyze text without saving
- Save entries with emotional tags
- View last 3 entries
- View your entire journal history
- Color-coded emotional categories
- Clean UI designed for reflection and readability


# Intelligent Emotional Processing
* Semantic Refinement
- SBERT embeddings compare your text with thousands of positive and negative examples.
- This avoids misclassification of ambiguous phrases like:
   - “I guess I’m okay.” → Neutral
   - “I’m crushing it today!” → Positive
   - “I’m crushed.” → Negative

* Slang & Emoji Detection
- Modern emotional language often breaks traditional NLP models.
- This project corrects sentiment for:
   - Internet slang
   - TikTok-era phrasing
   - Dramatic exaggerations
   - Emojis that carry emotional meaning (🔥 💀 😭)

* “But” Emotional Rule
- Humans remember how events ended, not how they started.
   - “Today sucked, but it got better.” → Positive
   - “It was good, but now I’m overwhelmed.” → Negative

# Unit Tests
* The project includes tests that validate:
- Neutral emotion detection
- Slang interpretation
- Emoji sentiment
- Stress/energy inference
- Output structure integrity
* This ensures emotional predictions remain stable and meaningful.


# Purpose
* This journaling system is designed to help users reflect on their emotional lives through technology that understands nuance, human behavior, and expressive language. Its dual-interface design makes it accessible to developers, everyday users, and mental-health–focused applications.
* It also serves as a demonstration of:
- Transformer models
- SBERT semantic similarity
- Dataset engineering
- Algorithmic emotional inference
- Full-stack development
- API design
- Frontend UX for mental wellness tools


# Overview
This project merges emotionally intelligent AI, clean design, and accessible tooling into a single unified journaling experience. Whether used through the terminal or the browser, the system delivers consistent, meaningful emotional feedback powered by modern NLP techniques.
