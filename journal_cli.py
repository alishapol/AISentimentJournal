# Handles command-line arguments and input text
import argparse
# Used for reading/writing JSON journal data
import json
# Allows file path resolution and file existence checks
import os
# Provides timezone control for timestamps
import pytz
# Used for generating timestamps
from datetime import datetime

# Suppresses recurring LibreSSL warnings on some systems
import warnings
warnings.filterwarnings("ignore", message=".*LibreSSL.*", category=Warning)

# Base directory where the script lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Path to the shared journal JSON file
JOURNAL_PATH = os.path.join(BASE_DIR, "journal_entries.json")

# Imports the AI text analysis logic from the other module
from journal_logic import analyze_entry

# Produces a PST timestamp string for saved entries
def get_pst_timestamp():
    pst = pytz.timezone("America/Los_Angeles")
    now = datetime.now(pst)
    return now.strftime("%B %d, %Y — %-I:%M %p (PST)")

# Loads all saved journal entries from disk
def load_entries():
    if not os.path.exists(JOURNAL_PATH):
        return []
    with open(JOURNAL_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Saves the updated list of entries back into the JSON file
def save_entries(entries):
    with open(JOURNAL_PATH, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)

# Runs AI analysis on input text and stores the entry
def add_new_entry(text: str):
    tags = analyze_entry(text)
    # Handles empty text or invalid input cases
    if "error" in tags:
        return tags

    # Creates the structured journal entry object
    entry = {
        "timestamp": get_pst_timestamp(),
        "text": text,
        "tags": tags,
    }

    # Append new entry to the existing journal list
    entries = load_entries()
    entries.append(entry)
    save_entries(entries)
    return tags

# Returns the most recent n entries
def get_last_entries(n=3):
    entries = load_entries()
    return entries[-n:]

# Provides a command-line interface for adding entries or viewing a summary
def main():
    parser = argparse.ArgumentParser(description="AI-Powered Journal CLI")
    # User chooses between adding a new entry or viewing a summary
    parser.add_argument("command", choices=["add", "summary"])
    # Optional text argument for the "add" command
    parser.add_argument("text", nargs="?", help="Journal text for 'add'")

    args = parser.parse_args()

    # Handles: `python journal.py add "my thoughts"`
    if args.command == "add":
        if not args.text:
            print("Error: No entry text provided.")
            return

        # Run analysis + save entry
        tags = add_new_entry(args.text)

        # Display results from the AI model
        print("\nSaved entry with tags:")
        print(f"  Sentiment : {tags['sentiment']}")
        print(f"  Emotion   : {tags['emotion']}")
        print(f"  Stress    : {tags['stress']}")
        print(f"  Energy    : {tags['energy']}\n")

    # Handles: `python journal.py summary`
    elif args.command == "summary":
        entries = get_last_entries()

        # Handle empty journal
        if not entries:
            print("No entries available.")
            return

        # Print the most recent entries and their AI metadata
        print("\nLast Journal Entries:\n")
        for entry in entries:
            print(f"- {entry['timestamp']}")
            print(f"  Text     : {entry['text']}")
            print(f"  Sentiment: {entry['tags']['sentiment']}")
            print(f"  Emotion  : {entry['tags']['emotion']}")
            print(f"  Stress   : {entry['tags']['stress']}")
            print(f"  Energy   : {entry['tags']['energy']}\n")

# Runs the CLI when the script is executed directly
if __name__ == "__main__":
    main()