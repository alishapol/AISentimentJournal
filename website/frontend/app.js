// Base URL for all backend requests
const API_URL = "http://127.0.0.1:8000";


// Sends user text to the backend for AI analysis
async function analyzeEntry() {
    // Get text from the textarea and clean it
    const text = document.getElementById("entryText").value.trim();
    if (!text) return alert("Type something!");

    // Send text to the API for analysis
    const res = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ text })
    });

    // Parse the result and display it
    const data = await res.json();
    showAnalysis(data.analysis);
}


// Sends a new journal entry to be analyzed and saved
async function addEntry() {
    // Pull the text from input
    const text = document.getElementById("entryText").value.trim();
    if (!text) return alert("Write something first!");

    // Request to save the entry on the backend
    const res = await fetch(`${API_URL}/add`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ text })
    });

    // Show AI-generated tags for the newly saved entry
    const data = await res.json();
    showAnalysis(data.saved.tags);
}


// Displays sentiment, emotion, stress, and energy on the page
function showAnalysis(result) {
    const section = document.getElementById("analysisSection");
    const out = document.getElementById("analysisOutput");

    // Make analysis section visible
    section.classList.remove("hidden");

    // Inject formatted tag elements into the output box
    out.innerHTML = `
        <div class="tag tag-sentiment">Sentiment: ${result.sentiment}</div>
        <div class="tag tag-emotion">Emotion: ${result.emotion}</div>
        <div class="tag tag-stress">Stress: ${result.stress}</div>
        <div class="tag tag-energy">Energy: ${result.energy}</div>
    `;
}


// Loads the last 3 saved entries from the backend
async function loadLast3() {
    const res = await fetch(`${API_URL}/last`);
    showEntries("Last 3 Entries", (await res.json()).entries);
}


// Loads all saved entries
async function loadAllEntries() {
    const res = await fetch(`${API_URL}/all`);
    showEntries("All Entries", (await res.json()).entries);
}


// Renders entries onto the history page
function showEntries(title, entries) {
    const section = document.getElementById("entriesSection");
    const list = document.getElementById("entriesList");
    const titleEl = document.getElementById("entriesTitle");

    // Reveal the entries section
    section.classList.remove("hidden");

    // Update the section heading
    titleEl.innerText = title;

    // Handle the case where no entries exist
    if (!entries.length) {
        list.innerHTML = "<p>No journal entries found.</p>";
        return;
    }

    // Generate an HTML card for each entry
    list.innerHTML = entries.map(e => `
        <div class="entry">
            <h4>${e.timestamp}</h4>
            <p>${e.text}</p>

            <div class="tags">
                <span class="tag tag-sentiment">${e.tags.sentiment}</span>
                <span class="tag tag-emotion">${e.tags.emotion}</span>
                <span class="tag tag-stress">${e.tags.stress}</span>
                <span class="tag tag-energy">${e.tags.energy}</span>
            </div>
        </div>
    `).join("");
}