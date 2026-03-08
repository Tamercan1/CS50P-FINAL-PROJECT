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
MODE_MODEL = "gemini-2.5-flash-lite"

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
def get_response_from_AI(contents, instruction, temp, max_token):
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


# 1ST FUNCTION
def decide_mode(user_message: str, personalities: list[dict]) -> dict:
    mode_ids = ", ".join(p["id"] for p in personalities)

    mode_prompt = f"""
Choose the best personality mode for this user message.

Available modes:
{mode_ids}

Return JSON ONLY in this format:

If user explicitly requests a mode change:
{{"switch": true, "mode": "one_of_the_modes"}}

If user is NOT asking to change mode:
{{"switch": false}}

User message:
{user_message}

Guidelines:
- Use programmer for coding, debugging, software design, and technical implementation
- Use tutor for teaching concepts step-by-step
- Use einstein for science or math explained intuitively
- Use socrates for philosophical reflection or logic-heavy inquiry
- Use therapist for emotional support, stress, sadness, or personal struggles
- Use normal for casual conversation or general-purpose help
- Use other if user decide personality he wants to talk
- Only switch if the user clearly asks for a mode or personality
- Examples of switching:
  "switch to programmer mode"
  "act like Einstein"
  "be my therapist"
  "enter tutor mode"
- Normal questions should NOT trigger switching
"""
    
    for i in range(3):
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
            return data
        
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
    current_mode = mem.get("last_mode", "normal")

    print_text(
        text="mAI Friend bot automatically adopt mode, but you can choose from this list:",
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
        decision = decide_mode(user_input, PERSONALITIES)

        # validate mode
        if decision.get("switch"):
            new_mode = decision.get("mode", "normal")

            if new_mode != current_mode:
                current_mode = new_mode
                console.print(f"\n[green][Switching to {current_mode} mode...][/green]\n")

        # set mode to whatever the AI decided
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
        
        model_output = stream_response(chat_response, person.prompt['display_name'] + " Mode")
        print("\n")

        # append to memory.py every chat turn
        memory.append_trim(mem, "user", user_input)  
        memory.append_trim(mem, "model", model_output)
        memory.update_memory(mem)
        mem["last_mode"] = person.mode

        display_text = "Say anything"
        
        # save memory changes
        memory.save_memory(mem)

    console.print("[yellow]Nice Conversation, Nice to meet you![/yellow]")


if __name__ == "__main__":
    main()