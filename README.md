<div align="center">

# 🤖 mAI Friend

### CLI-Based Adaptive AI Companion

An intelligent CLI assistant that **changes personality modes dynamically**
using **prompt engineering and Google's Gemini API**.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Gemini API](https://img.shields.io/badge/Gemini-AI-orange)
![Json](https://img.shields.io/badge/Json-{JSON}-yellow)
![Status](https://img.shields.io/badge/Status-Active-success)

</div>

---
# 🎥 Video Demo
####  URL: 
---
# 📖 Project Description

**mAI Friend – Adaptive AI Companion** is a CLI-based AI assistant built in Python that dynamically adapts its personality depending on the user's input. Instead of behaving like a generic chatbot, user has the freedom to choose appropriate personality mode they want to talk with such as a scientist, philosopher, programmer, tutor, or just a supportive companion.

The primary goal of this project is to demonstrate the practical application of **prompt engineering, AI API integration, and modular Python design**. The project utilizes Google's Gemini API to generate responses while a custom personality system controls the tone, reasoning style, and conversational behavior.

When a user enters a message, the program first analyzes the input to determine which personality mode best fits the request. For example, if the user asks a science-related question, mAI Friend may suggest to **Einstein Mode**, which focuses on explaining concepts scientifically and impersonate Albert Einstein. The user have the control to explicitly switch mode and accept suggested mode. mAI Friend AI **automatically detect** the best mode or personality.

Once the personality mode is selected, the program constructs a carefully engineered prompt containing *instructions, personality traits, style rules, and conversation context*. This prompt is then sent to the Gemini model to generate a response that reflects the selected persona.

To make the interaction more engaging, the project uses the **Rich Python library** to create a visually formatted command-line interface. Responses are displayed in styled panels and streamed gradually to simulate a real-time conversation.

Another important feature of the project is its **memory system**, which stores useful information about the conversation using a JSON file. This allows the assistant to remember certain preferences and conversation history between interactions. This is like a **simple version** of how certain LLM's store conversation contexts.

Overall, the project aims to demonstrate how AI assistants can be made more dynamic and interactive through **personality-based prompt engineering**.

---
# 📂 File Explanation

### `project.py`

This file contains the **main program logic** and serves as the entry point of the application. It handles user input, model output, program loop, determines when personality modes should change, and handles communication between the other modules.

### `personas.py`

This file defines the different **personality modes** available in the program. Each persona includes attributes such as display name, personality description, greeting message, style rules, and system instructions.

### `prompt.py`

The purpose of this module is to **build the system prompt** that is sent to the AI model. It combines the selected personality's traits, greeting, and behavioral rules into a single structured prompt. 

### `memory.py`

This module implements the **memory system** using JSON storage. It allows the program to save, retrieve, update, and add conversation-related data. 

### `CLI_design.py`

This file manages the **visual presentation of the command-line interface**. It uses the Rich library to display styled panels, status messages, streaming responses, modes list and others.

### `test_project.py`

This file contains **unit tests written with pytest**. These tests verify that important functions behave correctly, particularly those responsible for prompt building and personality selection.

### `memory.json`
This file acts as the **persistent storage for the assistant’s memory system**. It stores conversation-related data such as user preferences and recent interactions. The program reads from and writes to this file during execution.

### `.env.example`
This file is where other users should **store their API key** to ensure the model will work on their device.

---

# ✨ Features
### 1. Adaptive Personality System
mAi Friend Bot dynamically switches between personalities depending on the user's input.

| Modes | Purpose |
|-----|------|
| Einstein   | Science explanations |
| Socrates   | Philosophical reasoning |
| Programmer   | Debugging and coding help |
| Therapist   | Emotional support |
| Other   | User decides personality |
| Tutor   | Concept explanations |
| Normal   | Friendly conversation |


### 2. **AI Mode Detection**
  - Automatically detects the best mode from user's input.
  - Will suggest you mode and ask you first before switching.
  - You can explicitly command the model to change mode.

### 3. **Memory System**
  - Using JSON.
  - Stores users preferences based on recent conversation.
  - Stoes recent conversation history.

### 4. **Prompt Engineering**
  - Custom system prompts to control AI personality.

### 5. **Rich CLI Interface**
  - Beautiful command line UI using the `rich` library.

---

# 📸 Preview

Example CLI output:

```
(.venv) $ python project.py
╭───────────────────────────────────────────────────── mAI Friend ─────────────────────────────────────────────────────╮
│                                                                                                                      │
│  mAI Friend bot automatically adapt mode, but you can choose from this list:                                         │
│                                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
                          Available Modes                          
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Mode                 ┃ Purpose                                  ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Einstein             │ Science and math explanations            │
│ Socrates             │ Philosophical discussion                 │
│ Programmer           │ Debugging and coding help                │
│ Therapist            │ Emotional support                        │
│ Tutor                │ Concept explanations                     │
│ Other                │ You decide the personality               │
│ Normal               │ Friendly conversation                    │
└──────────────────────┴──────────────────────────────────────────┘

Let me know what you need.: lets talk about physics and math

Suggestion: Einstein mode may help here.
The user wants to discuss physics and math, which aligns with intuitive scientific explanations.

Want to switch? just say 'yes': yes
╭─────────────────────────────────────────────────── Einstein Mode ────────────────────────────────────────────────────╮
│                                                                                                                      │
│  A marvelous choice. Math is the language in which the universe writes its laws, and physics is the story that       │
│  those laws tell. Without the language, the story would...                                                           │
│                                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

Let me know what you need.: i need help debugging my code

Suggestion: Programmer mode may help here.
The user needs help with debugging code.

Want to switch? just say 'yes': yes
╭─────────────────────────────────────────────── Senior Programmer Mode ───────────────────────────────────────────────╮
│                                                                                                                      │
│  Alright, let's take a look. What are you building today?                                                            │
│                                                                                                                      │
│  I'm ready to pivot back into Programmer Mode. Sometimes the most elegant physical theories are easier to grasp      │
│  than a stubborn bug in a codebase!...                                                                               │
│                                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

Let me know what you need.: exit
Goodbye!
Nice Conversation, Nice to meet you!
```

---

# ⚙️ Installation

**Clone the repository:**

```bash
git clone https://github.com/Tamercan1/CS50P-FINAL-PROJECT.git
```

**Create virtual environment:**

```bash
python -m venv venv
```

**Activate it:**

*Windows*

```bash
venv\Scripts\activate
```

*Mac/Linux*

```bash
source venv/bin/activate
```

**Install dependencies:**

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create .env file
```bash
cp .env.example .env
```
Open the `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

You can get a free key from  
https://aistudio.google.com

To do that:
- Open the URL <https://aistudio.google.com>
- Sign in to your account
- Go to "Get API Key" located at the bottom left
- Click "Create API Key"
   - Create Key
   - Copy API Key
- Replace "your_api_key_here" with your real API key

---
# 🧠 How It Works

Program Flow:

```
User Input
   ↓
Mode Detection
   ↓
Prompt Builder
   ↓
AI Response Generation
   ↓
Memory Storage
   ↓
Formatted CLI Output
```


---
# ⚠️ Important Notes

### Gemini Model Availability

This project relies on Google's **Gemini API**, and the availability of models may change over time. If the model specified in the code becomes unavailable, you may need to update the model name in `project.py`.

For example, if the current model is unavailable:

### `project.py`
```python
CHAT_MODEL = "gemini-3.1-flash-lite-preview"
MODE_MODEL = "gemini-2.5-flash"
```
### `memory.py`
```python
MEMORY_MODEL = "gemini-3.1-flash-lite-preview"
```
> You can check other models at <https://ai.google.dev/gemini-api/docs/models> and use what's available
## Run test with pytest:

```bash
pytest test_project.py
```

---

## ✍️ Author

**Datu Tamer-Can Wawa**  
Computer Science Student   
Notre Dame University

Built as part of **Harvard CS50P – Introduction to Programming with Python**

---

## 📜 License

**MIT License**