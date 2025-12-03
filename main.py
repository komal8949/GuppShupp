from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import json

app = FastAPI()

# In-memory store
MEMORY_DB = []

# ---------------------------
# MEMORY EXTRACTION LOGIC
# ---------------------------
def extract_memories(messages: List[str]):
    preferences = []
    emotions = []
    facts = []

    for msg in messages:
        low = msg.lower()

        # Preferences
        if "i like" in low or "i prefer" in low or "i want" in low:
            preferences.append(msg)

        # Emotions
        if any(x in low for x in ["sad", "confused", "happy", "excited", "frustrated"]):
            emotions.append(msg)

        # Simple factual patterns
        if any(x in low for x in ["i am", "my name", "i work", "i study", "i applied"]):
            facts.append(msg)

    return {
        "preferences": preferences,
        "emotions": emotions,
        "facts": facts
    }

# ---------------------------
# PERSONALITY ENGINE
# ---------------------------
def apply_personality(text: str, tone: str):
    if tone == "calm_mentor":
        return (
            "Here’s a calm, step-by-step explanation:\n\n"
            + "1. " + text.replace(". ", "\n2. ")
        )
    elif tone == "witty_friend":
        return f"{text}\n\n😄 Anyway, that’s the gist — fun, right?"
    elif tone == "therapist":
        return (
            "I hear you, and it's completely okay to feel this way.\n\n"
            "Here's a gentle breakdown of what you shared:\n\n"
            + text
        )
    else:
        return text

# ---------------------------
# API ENDPOINTS
# ---------------------------
@app.post("/extract")
async def extract_api(messages: str = Form(...)):
    msgs = messages.split("\n")
    memories = extract_memories(msgs)
    MEMORY_DB.append(memories)
    return memories

@app.post("/respond")
async def respond_api(message: str = Form(...), tone: str = Form(...)):
    base_reply = f"You said: {message}. Here's what you can do..."
    transformed = apply_personality(base_reply, tone)
    return {"reply": transformed}

@app.get("/memories")
async def get_memories():
    return MEMORY_DB

# ---------------------------
# FRONTEND
# ---------------------------
@app.get("/", response_class=HTMLResponse)
async def home():
    html = """
    <h2>GUPPSHUPP Assignment Demo</h2>

    <form action="/extract" method="post">
        <textarea name="messages" rows="10" cols="50" placeholder="Paste 30 messages"></textarea><br>
        <button type="submit">Extract Memories</button>
    </form>

    <br><br>

    <form action="/respond" method="post">
        <input name="message" placeholder="User message" size="50"><br><br>

        <label>Choose Personality:</label><br>
        <select name="tone">
            <option value="calm_mentor">Calm Mentor</option>
            <option value="witty_friend">Witty Friend</option>
            <option value="therapist">Therapist Style</option>
        </select>

        <br><br>
        <button type="submit">Generate Response</button>
    </form>
    """
    return html
