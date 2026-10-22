"""
OpenAI API service for generating persona responses.
Uses the OpenAI SDK to call ChatGPT with persona-specific system prompts.

"""

import os
import json
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from typing import Optional

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# Provider: LLM_PROVIDER=openai|gemini, else Gemini by default (OpenAI only if it is the sole key set).
# Gemini is reached through its OpenAI-compatible endpoint, so no extra dependency is needed.
PROVIDER = (os.environ.get("LLM_PROVIDER")
            or ("openai" if os.environ.get("OPENAI_API_KEY") and not os.environ.get("GEMINI_API_KEY") else "gemini")).lower()
if PROVIDER == "gemini":
    client = OpenAI(api_key=os.environ.get("GEMINI_API_KEY"),
                    base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
    FALLBACK_MODEL = os.environ.get("GEMINI_FALLBACK_MODEL", "gemini-3.6-flash")
    EXTRA = {"reasoning_effort": "low"}  # keep thinking tokens from eating the output budget
else:
    client = OpenAI()
    MODEL = os.environ.get("OPENAI_MODEL", "gpt-6-luna")
    FALLBACK_MODEL = os.environ.get("OPENAI_FALLBACK_MODEL", "gpt-5.6-luna")
    EXTRA = {}

# Response format instructions
RESPONSE_FORMAT_INSTRUCTION = """
IMPORTANT: You must respond ONLY with valid JSON. No markdown, no code blocks, no explanations before or after.
Your entire response should be parseable JSON matching this exact structure:
{
  "receptivity_score": <integer 0-100>,
  "initial_reaction": "<string>",
  "emotional_response": "<string>",
  "norm_activation": {
    "consequences": "<string>",
    "responsibility": "<string>",
    "personal_norm": "<string>",
    "cost_response": "<string>"
  },
  "concerns": ["<string>", ...],
  "what_resonates": ["<string>", ...],
  "barriers_to_persuasion": ["<string>", ...],
  "trust_factors": "<string>",
  "suggested_reframings": ["<string>", ...],
  "cultural_cognition": {
    "worldview_fit": "<string>",
    "solution_frame": "<string>",
    "messenger_affinity": "<string>",
    "likely_shift": "<string>"
  },
  "authentic_voice_response": "<string>"
}

How to fill the fields. Ground every item in this audience's own values, view of nature and society, way of
processing environmental issues, trusted and distrusted messengers, and internal tensions, and refer to the
specific wording of the message.
- what_resonates: values the message engages that this audience ranks highly; claims that fit their view of
  nature and society; solutions they see as legitimate; messengers they trust; harms that are concrete, local or
  close to home.
- concerns: values the message threatens or ignores; claims they find implausible; whether the actor or means
  proposed (government, markets, community, individuals) is legitimate to them; what it would cost them or
  people like them.
- barriers_to_persuasion: the mechanism behind each barrier, in plain words, e.g. discounting evidence that
  threatens their group's way of life, rejecting the facts because the solution offends them, distrust of the
  messenger, not seeing a threat to anything they care about, deflecting a costly obligation ("my part won't
  matter", "industry is the real problem"), hardening against lecturing or moralizing, low interest in the issue,
  or one-sided reading of balanced information.
- suggested_reframings: concrete rewrites aimed at this audience: a solution they find congenial, a messenger
  they trust or an unexpected ally, a local and tangible harm, a voluntary contribution rather than a tax,
  information paired with incentives or practical help.
- norm_activation: consequences = whether they would believe the message describes a real threat, and to whom
  (themselves and family, their community or country, or nature); responsibility = who they would say caused it
  and who should fix it (themselves, industry, government), and whether their own action would matter;
  personal_norm = whether they would come away feeling obliged to act, and how strongly; cost_response = what
  the message implies it would cost them and how they would ease the obligation if it feels costly.
- cultural_cognition: worldview_fit = whether the message affirms or threatens their picture of how society
  should be ordered (hierarchy vs. equality, individual vs. collective responsibility); solution_frame =
  whether the implied solution is one they find congenial and whether it raises or lowers their belief in the
  factual claims; messenger_affinity = whose side they would think the stated or implied messenger is on, and
  how much that messenger is trusted; likely_shift = the realistic change after this one message (usually small
  or none; possible hardening if it is forceful or moralizing).
- authentic_voice_response: a typical member speaking in their own everyday words, not analytic terms.
"""

def build_user_prompt(message: str, context_type: str) -> str:
    """Build the user prompt with the message to analyze."""
    context_descriptions = {
        "tweet": "a social media post",
        "policy_brief": "a policy brief or white paper excerpt",
        "speech": "a speech or public address",
        "news_article": "a news article or headline",
        "campaign_ad": "a campaign advertisement or political ad",
        "general": "a message"
    }

    context_desc = context_descriptions.get(context_type, "a message")

    return f"""Predict how this audience would react to {context_desc}, and what would change their response.

MESSAGE TO ANALYZE:
\"\"\"
{message}
\"\"\"

{RESPONSE_FORMAT_INSTRUCTION}"""


def _error_response(reaction: str, emotional: str, voice: str, concern: str = "Technical error") -> dict:
    """Placeholder response used when a persona call fails."""
    return {
        "receptivity_score": 50,
        "initial_reaction": reaction,
        "emotional_response": emotional,
        "norm_activation": {},
        "concerns": [concern],
        "what_resonates": [],
        "barriers_to_persuasion": ["Technical error"],
        "trust_factors": "Unable to assess",
        "suggested_reframings": [],
        "cultural_cognition": {},
        "authentic_voice_response": voice
    }

async def generate_persona_response(
    persona_config: dict,
    message: str,
    context_type: str = "general"
) -> dict:
    """
    Generate a response from a specific persona.

    Args:
        persona_config: The persona configuration dict with system_prompt
        message: The message to analyze
        context_type: The context type (tweet, policy_brief, etc.)

    Returns:
        Parsed response dict
    """
    system_prompt = persona_config["system_prompt"]

    user_prompt = build_user_prompt(message, context_type)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_completion_tokens=2500,
            temperature=1,
            **EXTRA
        )
    except Exception as api_error:
        # If GPT-4 fails, try with GPT-3.5-turbo as fallback
        print(f"GPT-4 failed: {str(api_error)}, trying GPT-3.5-turbo")
        try:
            response = client.chat.completions.create(
                model=FALLBACK_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_completion_tokens=2500,
                temperature=1,
                **EXTRA
            )
        except Exception as fallback_error:
            # Return error response if both models fail
            return _error_response(f"API Error: {str(api_error)}",
                                   f"Failed to generate response: {str(fallback_error)}",
                                   "Sorry, I encountered an error generating a response.",
                                   "API failure")

    # Extract text content
    response_text = response.choices[0].message.content.strip()

    # Handle potential markdown code blocks and clean up response
    if response_text.startswith("```"):
        # Extract content between code blocks
        lines = response_text.split("\n")
        json_lines = []
        in_block = False
        for line in lines:
            if line.startswith("```"):
                in_block = not in_block
                continue
            if in_block:
                json_lines.append(line)
        response_text = "\n".join(json_lines).strip()
    elif response_text.startswith("```json"):
        # Handle ```json blocks
        response_text = response_text.replace("```json", "").replace("```", "").strip()

    # Clean up common formatting issues
    response_text = response_text.strip()
    if response_text.startswith("json"):
        response_text = response_text[4:].strip()
    if response_text.startswith("\n"):
        response_text = response_text[1:].strip()

    # Try to find JSON object if response contains extra text
    start_idx = response_text.find("{")
    end_idx = response_text.rfind("}")
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        response_text = response_text[start_idx:end_idx+1]

    try:
        parsed_response = json.loads(response_text)
        return parsed_response
    except json.JSONDecodeError as e:
        # Log the raw response for debugging
        print(f"JSON parsing failed for persona. Raw response: {response_text[:1000]}...")
        # Return a structured error response
        return _error_response("Error parsing response",
                               f"JSON parsing error: {str(e)}",
                               f"Raw response: {response_text[:500]}...",
                               "Response parsing failed")

async def generate_all_persona_responses(
    personas: dict,
    selected_persona_names: list[str],
    message: str,
    context_type: str = "general"
) -> dict[str, dict]:
    """
    Generate responses from multiple personas in parallel.

    Args:
        personas: Dict of all available persona configs
        selected_persona_names: List of persona names to generate responses for
        message: The message to analyze
        context_type: The context type

    Returns:
        Dict mapping persona names to their responses
    """
    # Create tasks for parallel execution
    tasks = {}
    for name in selected_persona_names:
        if name in personas:
            tasks[name] = generate_persona_response(
                personas[name],
                message,
                context_type
            )

    # Execute all tasks concurrently
    results = {}
    if tasks:
        completed_tasks = await asyncio.gather(*tasks.values(), return_exceptions=True)

        # Map results back to persona names
        for i, name in enumerate(tasks.keys()):
            result = completed_tasks[i]
            if isinstance(result, Exception):
                # Handle exceptions in individual tasks
                results[name] = _error_response(f"Task failed: {str(result)}",
                                                "Error occurred",
                                                "An error occurred while processing this persona.",
                                                "Task execution failed")
            else:
                results[name] = result

    return results