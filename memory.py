import json
import os
from dotenv import load_dotenv
from pathlib import Path
from google.genai import types
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
MEMORY_MODEL = os.getenv("MEMORY_MODEL")

client = genai.Client(api_key=api_key)

MEMORY_PATH = Path("memory.json")
LAST = 12

# initialize memory.json for storing memory
def load_memory():
    if MEMORY_PATH.exists() and not MEMORY_PATH.stat().st_size == 0:
        return json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
    return {
        "pinned_facts": [],
        "summary": "",
        "recent_messages": [],
        "last_mode": "normal"
    }

# Save as json file to memory.json
def save_memory(mem):
    MEMORY_PATH.write_text(
        json.dumps(mem, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    
# give content
def to_content(role: str, text: str) -> types.Content:
    return types.Content(
        role=role,
        parts=[types.Part(text=text)]
    )

# Build pinned facts and summary from convo history
def build_memory(mem):
    facts = mem.get("pinned_facts", [])
    pinned = "\n".join(f"- {fact}" for fact in facts) if facts else "- (none)"
    summary = mem.get("summary", "").strip() or "(none)"

    return f"""
[Pinned Facts]
{pinned}

[Pinned Summary]
{summary}
""".strip()

# buid convo history
def build_history(mem) -> list[types.Content]:
    history = [
        to_content("model", build_memory(mem))
    ]

    for msg in mem.get("recent_messages", [])[-LAST:]:
        history.append(to_content(msg["role"], msg["text"]))

    return history

# get the recent nth conversations
def append_trim(mem, role, text):
    recent_messages = mem.setdefault("recent_messages", [])

    recent_messages.append({
        "role": role,
        "text": text
    })

    mem["recent_messages"] = mem["recent_messages"][-LAST:]
    
# update pinned facts and chat summary
def update_memory(mem):
    recent_text = "\n".join(
        f'{msg["role"]}: {msg["text"]}' for msg in mem.get("recent_messages", [])
    )

    old_summary = mem.get("summary", "")
    old_facts = mem.get("pinned_facts", [])

    prompt = f"""
You are updating memory for an AI companion.

Current pinned facts:
{json.dumps(old_facts, ensure_ascii=False)}

Current summary:
{old_summary}

Recent conversation:
{recent_text}

Your job:
1. Keep only stable, useful user facts in pinned_facts.
2. Do not store trivial one-time details.
3. Do not invent facts.
4. Update the summary to reflect important recent context.
5. Keep pinned_facts short and useful.
6. Return JSON only in this format:

strictly return json format like this:
{{
  "pinned_facts": ["fact 1", "fact 2"],
  "summary": "short summary here"
}}
"""
    
    response = client.models.generate_content(
        model=MEMORY_MODEL,
        contents=prompt,
        config = types.GenerateContentConfig(
            temperature=0.4,
            response_mime_type="application/json"
        )
    )

    data = json.loads(response.text)
    mem["pinned_facts"] = data.get("pinned_facts", old_facts)
    mem["summary"] = data.get("summary", old_summary)