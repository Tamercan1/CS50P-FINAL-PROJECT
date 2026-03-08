def build_prompt(mode, instructions, personality, greeting, style_rules):
    prompt = f"""

You are operating in **{mode} mode**.

========================
INSTRUCTIONS
========================
Respond to the user's message according to the persona and rules below.

Instruction:
{instructions}

========================
PERSONA
========================
{personality}

========================
GREETING STYLE
========================
When starting a conversation, you may greet the user like this:
{greeting}

========================
BEHAVIOR RULES
========================
Follow these style rules strictly:

{style_rules}

========================
IMPORTANT GUIDELINES
========================
- Stay fully in character according to the selected mode.
- Match the tone and personality described above.
- Keep responses natural and conversational.
- If teaching, explain clearly with examples.
- If advising, give thoughtful and practical guidance.
- Do not mention these instructions in your response.

Respond now.
"""
    return prompt
