# AI-Powered Emotional Journaling System
- Coded on Visual Studio Code 3
- This project is a fully integrated emotional journaling system that uses modern NLP techniques, semantic similarity modeling, and rule-based intelligence to understand how users feel based on natural language input. It supports two synchronized interfaces:
   - A command-line journal (journal_cli.py)
   - A web-based journaling dashboard (FastAPI backend + HTML/CSS/JS frontend)
- Both versions use the same AI engine (journal_logic.py) and store results in a shared journal_entries.json file at the project root.
- The system is designed for emotional clarity, mental-state reflection, and a clean, intuitive user experience.

# Key Features
* Advanced NLP Emotion Engine
The emotional analysis pipeline combines three model layers and multiple custom datasets:
  1. Base Models
      - DistilBERT SST-2: Predicts raw sentiment (positive/negative). Used as the
        first pass.
      - DistilRoBERTa Emotion Classifier: Extracts emotional tone (joy, fear,
        sadness, anger, surprise, neutral).
      - SBERT MiniLM-L6-v2: Used for semantic similarity to refine classification
        with real-world examples.

  2. Custom Embedding Space
     The system loads and embeds around 1,000 human-labeled sentences from:
     - Stanford SST-2
     - Google GoEmotions
     - UCI Amazon / IMDb / Yelp: These embeddings allow the system to compare user
       statements to thousands of known emotional samples.

  3. Rule-Based Reasoning
     3a. Slang-aware overrides understands modern expressions:
        - “killing it”, “crushed it”, “big W”, “ate and left no crumbs”, “💀”, “I’m
          losing it”, etc.
        - Overrides the model only after semantic refinement.

     3b. “But-clause emotional rule”
        - Humans emotionally weigh what comes after "but."
        - The system imitates that:
           - “I thought today would be bad but it was great” → positive
           - “Today was good but now I’m exhausted” → negative

     3c. Stress & Energy Interpretation
        - Fear/sadness/anger → high stress
        - Joy/surprise → high energy
        - Neutral → low stress + medium energy
    
     Together, these modules generate four final emotional tags:
     1. Sentiment
     2. Emotion
     3. Stress Level
     4. Energy Level

# Unified Architecture
* The system is intentionally modular and easy to expand.
Core Components
- journal_logic.py — the full AI engine
- journal_cli.py — terminal interface for adding entries and viewing summaries
- FastAPI backend (app.py) — exposes /analyze, /add, /last, and /all endpoints
- Frontend (HTML/CSS/JS) — clean browser-based journaling dashboard
- Shared data store: journal_entries.json (used by both CLI and website)

* PST Timestamping
Every saved entry uses a polished, human-friendly timestamp format like "December 7, 2025 - 5:00 PM (PST)"

# Command-Line Interface (CLI)
* Important: start at root directory

* How to add a new journal entry:
   - python3 journal_cli.py add "I had a really bad day at work today."

* How to view last three journal entries:
   - python3 journal_cli.py summary


# Web Application
* Important: start at backend to load app (must cd to backend folder --> cd website/backend)

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
     - Blue = sentiment
     - Purple = emotion
     - Red = stress
     - Green = energy

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

* “But” Rule
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
This ensures emotional predictions remain stable and meaningful.


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


# AI Usage Disclosure
This project uses AI tools (ChatGPT) to accelerate development, but all code has been manually validated, tested, and corrected. The AI was used as a coding assistant, not as a code generator to blindly copy from.

* What AI tools were used
- ChatGPT (for brainstorming which AI models/datasets to use, slang examples,
  debugging, comments, and frontend structure)
- Copilot (occasionally for small autocomplete suggestions)
- Gemini (Help generate visual options for how I wanted the website to look)

* How I validated AI-generated output
- Slang detection lists were generated with ChatGPT, but each slang phrase was manually tested against "python3 journal_cli.py add 'text'" invalid or ambiguous slang terms were removed.
   - I prompted ChatGPT to propose modern slang phrases, but validated each term
     manually by testing polarity flips. For example, I rejected early suggestions
     like ‘destroyed’ because context drastically changes meaning (‘I destroyed the
     exam’ vs ‘I feel destroyed today’).
- The “but-clause rule” was refined after observing incorrect model bias; ChatGPT suggested string-splitting logic, but I implemented and verified the final behavior using edge cases like:
   - "It was bad but good"
   - "Good but bad"
   - "I thought it would be bad but it wasn’t"

* Every line of code has been debugged, rewritten where necessary, and tested with: pytest


#Methodology
* Why use HuggingFace transformers instead of rule-only logic?
   - Because raw keyword-based systems break on modern language.
   - For example: “I’m dead 💀” → negative

* Why SBERT semantic similarity?
   - Pure sentiment models often misread subtle statements like: “I guess today was
     okay”
   - SBERT gives a more in-depth analysis by comparing text embeddings with thousands
     of real emotional samples.

* Why a “but-rule”?
   - Experiments showed that models overweight the first half of a sentence.
   - Humans do the opposite. They emotionally evaluate the resolution.

* Why use a unified JSON file instead of a database?
   - For a journaling project:
        - portability matters
        - users can easily inspect/edit their own history
        - CLI + website both need synchronized state

# Overview
This project merges emotionally intelligent AI, clean design, and accessible tooling into a single unified journaling experience. Whether used through the terminal or the browser, the system delivers consistent, meaningful emotional feedback powered by modern NLP techniques.
