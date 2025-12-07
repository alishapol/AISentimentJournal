# Import the analyze_entry function so we can test its behavior
from journal_cli import analyze_entry


# Test that a neutral sentence is correctly labeled as neutral
def test_neutral_sentiment_detection():
    tags = analyze_entry("Today was fine. Nothing big happened.")
    assert tags["sentiment"] == "neutral"


# Test that positive slang like "killing it" is not misclassified as negative
def test_positive_slang_non_negative():
    tags = analyze_entry("I'm killing it today fr🔥")
    assert tags["sentiment"] in ["positive", "neutral"]


# Test that negative slang such as "I'm DONE" and the skull emoji are treated as negative
def test_negative_slang():
    tags = analyze_entry("bro I'm DONE with today 💀")
    assert tags["sentiment"] == "negative"


# Test that "crushing me" expresses negative emotion and should be labeled negative
def test_crushing_me_negative():
    tags = analyze_entry("The workload is crushing me and I cannot keep up.")
    assert tags["sentiment"] == "negative"


# Test that "crushing IT" is a positive slang phrase and should not be labeled negative
def test_crushing_it_not_negative():
    tags = analyze_entry("I'm CRUSHING IT at work today!")
    assert tags["sentiment"] in ["positive", "neutral"]


# Test that crying emoji and despairing language produce negative sentiment
def test_negative_emoji_sentence():
    tags = analyze_entry("😭😭 I can't do this anymore")
    assert tags["sentiment"] == "negative"


# Test that fear-related text results in a high stress classification
def test_high_stress_emotion():
    tags = analyze_entry("I'm scared and overwhelmed right now.")
    assert tags["stress"] == "high"


# Test that excitement (a high-energy emotion) results in high energy
def test_high_energy_joy():
    tags = analyze_entry("I'm so excited for this!!")
    assert tags["energy"] == "high"


# Test that analyze_entry always returns the correct set of output keys
def test_output_structure():
    tags = analyze_entry("I am feeling okay today.")
    assert set(tags.keys()) == {"sentiment", "emotion", "stress", "energy"}