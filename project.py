import os
import json
import personas
import memory
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompt import build_prompt
from rich.console import Console
from CLI_design import print_text, mode_list, prompt_user, stream_response

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing in .env")

client = genai.Client(api_key=api_key)

console = Console()

CHAT_MODEL = "gemini-3.1-flash-lite-preview"
MODE_MODEL = "gemini-2.5-flash"

PERSONALITIES = personas.PERSONALITIES
BUILT_IN_MODES = {
    "Einstein": "Science and math explanations",
    "Socrates": "Philosophical discussion",
    "Programmer": "Debugging and coding help",
    "Therapist": "Emotional support",
    "Tutor": "Concept explanations",
    "Other": "You decide the personality",
    "Normal": "Friendly conversation"
}


class Persona:
    def __init__(self, mode="normal", prompt=None):
        self.mode = mode
        self.prompt = prompt


person = Persona()

# Used only on chat proper
def get_response_from_AI(contents, instruction, temp, max_token, retries=3):

    # Handling API Errors
    for attempt in range(retries):
        try:
            chat_response = client.models.generate_content_stream(
                model=CHAT_MODEL,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=instruction,
                    temperature=temp,
                    max_output_tokens=max_token
                )
            )

            return chat_response
        
        except Exception as e:
            console.print(f"[yellow]Chat model busy... retrying ({attempt + 1}/{retries})[/yellow]")
            time.sleep(2)
    
    console.print(
        "[red]Sorry, I couldn't get a response from the chat model right now.[/red]"
    )
    return None


# 1ST FUNCTION
def decide_mode(user_message: str, personalities: list[dict], current_mode, retries=3) -> dict:
    mode_ids = ", ".join(p["id"] for p in personalities)

    mode_prompt = f"""
You are deciding whether the assistant should change personality mode.

Available modes:
{mode_ids}

Current mode:
{current_mode}

Return JSON ONLY.

Valid JSON formats:

1. If the user explicitly requests a mode/personality change:
{{"action": "switch", "mode": "one_of_the_modes"}}

2. If the user does NOT explicitly request a change, but another mode would clearly help:
{{"action": "suggest", "mode": "one_of_the_modes", "reason": "short_reason"}}

3. If no mode change is needed:
{{"action": "stay"}}

User message:
{user_message}

Rules:
- Only use "switch" when the user clearly and directly asks to change mode or asks the assistant to act like a certain persona.
- Use "suggest" when the user did not explicitly ask to switch, but a specific mode would obviously improve the response.
- Use "stay" for normal conversation, follow-ups, greetings, short replies, thanks, and general-purpose requests.
- Do NOT switch modes automatically just because a message matches a topic.
- Prefer staying in the current mode unless there is a strong reason to suggest another one.

Mode guidance:
- programmer: coding, debugging, software design, technical implementation
- tutor: step-by-step teaching, guided learning, beginner-friendly explanation
- einstein: science or math explained intuitively with analogies and big-picture thinking
- socrates: philosophical reflection, deep reasoning, logic-heavy discussion
- therapist: emotional support, stress, sadness, frustration, personal struggles
- normal: casual conversation, general-purpose help, neutral assistance
- other: user wants a custom personality not covered above

Examples:

User: "switch to programmer mode"
{{"action": "switch", "mode": "programmer"}}

User: "act like Einstein"
{{"action": "switch", "mode": "einstein"}}

User: "be my therapist"
{{"action": "switch", "mode": "therapist"}}

User: "can you explain recursion step by step?"
{{"action": "suggest", "mode": "tutor", "reason": "The user wants guided step-by-step learning."}}

User: "why does gravity bend light?"
{{"action": "suggest", "mode": "einstein", "reason": "The topic fits intuitive science explanation."}}

User: "thanks, that helped"
{{"action": "stay"}}

User: "hello"
{{"action": "stay"}}
"""

    for i in range(retries):
        try:
            response = client.models.generate_content(
                model=MODE_MODEL,
                contents=mode_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.6,
                    response_mime_type="application/json"
                )
            )

            if not response or not response.text:
                continue

            data = json.loads(response.text)
            action = data.get("action")
            if action not in {"switch", "suggest", "stay"}:
                return {"action": "stay"}

            if action in {"switch", "suggest"} and "mode" not in data:
                return {"action": "stay"}
            return data
        
        # Handle API errors
        except Exception:
            console.print(f"[green]Model busy... retrying:[/green]")
            time.sleep(2)

    print()
    console.print("[red]Sorry, unable to change mode right now :<\n[bold red]Reason:[/bold red] Model busy[/red]")
    return {"switch": False}


# 2ND FUNCTION
def build_contents(user_input: str, history: list) -> list:
    contents = history + [
            types.Content(role="user", parts=[types.Part(text=user_input)])
    ]

    return contents

# 3RD FUNCTION
def get_persona_prompt(mode: str, personalities: list[dict]):
    return next(
        (p["prompt"] for p in personalities if p["id"] == mode), None
    )


def main():

    mem = memory.load_memory()
    current_mode = "normal"

    print_text(
        text="mAI Friend bot automatically adapt mode, but you can choose from this list:",
        title="mAI Friend", border_color="blue"
    )
    mode_list(BUILT_IN_MODES)
    print()

    display_text = "Let me know what you need."

    while True:

        user_input = prompt_user(display_text)


        # Check if user wants to exit
        if user_input.lower() in ["exit", "quit"]:
            memory.save_memory(mem)
            console.print("[bold cyan]Goodbye![/bold cyan]")
            break
        
        # call decide mode every user input for dynamic mode
        decision = decide_mode(user_input, PERSONALITIES, current_mode)

        action = decision.get("action", "stay")

        if action == "switch":
            new_mode = decision.get("mode", current_mode)

            if new_mode != current_mode:
                current_mode = new_mode
                console.print(f"\n[green]Switching to {current_mode} mode...[/green]\n")

        elif action == "suggest":
            suggested_mode = decision.get("mode", current_mode)
            reason = decision.get("reason", "This mode may fit your request better.")

            if suggested_mode != current_mode:
                console.print(
                    f"\n[yellow]Suggestion:[/yellow] {suggested_mode.capitalize()} mode may help here.\n[dim]{reason}[/dim]\n"
                )
                suggest_dic = prompt_user("Want to switch? just say [green]'yes'[/green]")

                if suggest_dic.lower() in ["yes", "y", "okay", "ok"]:
                    current_mode = suggested_mode

        person.mode = current_mode
        person.prompt = get_persona_prompt(person.mode, PERSONALITIES)
        
        if person.prompt is None:
            console.print("[red]No matching personality found.[/red]")
            continue
        
        # build history from memory
        history = memory.build_history(mem)

        # PROMPT TO AI
        contents = build_contents(user_input=user_input, history=history)

        # SYSTEM_INSTRUCTION
        system_instruction = build_prompt(
            mode=person.mode,
            instructions=person.prompt["system_prompt"],
            personality=person.prompt["personality"],
            greeting=person.prompt["greeting"],
            style_rules=person.prompt["style_rules"]
        )

        with console.status("[bold cyan]mAI Friend is thinking...[/bold cyan]", spinner="dots"):
            time.sleep(0.3)
            chat_response = get_response_from_AI(
                contents=contents,
                instruction=system_instruction,
                temp=0.8, max_token=500
            )
        
        if chat_response is None:
            console.print(f"[red]Sorry, I'm having trouble responding right now. Please try again.[/red]\n")
            display_text = "Say anything"
            continue

        # Handle response when api is busy
        try:
            model_output = stream_response(resp=chat_response, mode=person.prompt['display_name'] + " Mode")
            print("\n") 
            if model_output is None:
                console.print("[red]Failed to stream response.[/red]")
                continue

        except Exception:
            console.print(f"[red]Sorry, something went wrong while streaming the response.[/red]\n")
            display_text = "Say anything"
            continue

        # append to memory.py every chat turn
        if model_output:
            memory.append_trim(mem, "user", user_input)  
            memory.append_trim(mem, "model", model_output)
            memory.update_memory(mem)
            mem["last_mode"] = person.mode            
            # save memory changes
            memory.save_memory(mem)

    console.print("[yellow]Nice Conversation, Nice to meet you![/yellow]")


if __name__ == "__main__":
    main()