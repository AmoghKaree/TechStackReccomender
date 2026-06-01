import json
import re
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load .env from project root (the directory containing this utils/ folder)
load_dotenv(Path(__file__).parent.parent / ".env")

MOCK_MODE = False
DEFAULT_MODEL = "gemini-2.5-flash"

_client: genai.Client | None = None


def set_mock_mode(enabled: bool):
    global MOCK_MODE
    MOCK_MODE = enabled


def is_mock_mode() -> bool:
    return MOCK_MODE


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "GEMINI_API_KEY not set. "
                "Get a free key at https://aistudio.google.com/apikey "
                "then: export GEMINI_API_KEY=your-key"
            )
        _client = genai.Client(api_key=api_key)
    return _client


def call_claude(
    system_prompt: str,
    user_message: str,
    model: str = DEFAULT_MODEL,
    max_tokens: int = 16384,
    temperature: float = 0.4,
) -> str:
    import time, re as _re
    from google.genai import errors as _errors

    client = _get_client()
    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=temperature,
        max_output_tokens=max_tokens,
    )

    for attempt in range(4):
        try:
            response = client.models.generate_content(
                model=model, contents=user_message, config=config
            )
            return response.text
        except _errors.ClientError as e:
            if e.code != 429 or attempt == 3:
                raise
            # Parse retry-after from error message, default 30s
            m = _re.search(r"retry in (\d+)", str(e))
            wait = int(m.group(1)) + 2 if m else 30
            time.sleep(wait)


def call_claude_json(
    system_prompt: str,
    user_message: str,
    model: str = DEFAULT_MODEL,
    max_tokens: int = 16384,
    temperature: float = 0.3,
) -> dict:
    raw = call_claude(
        system_prompt=system_prompt,
        user_message=user_message,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return _parse_json_response(raw)


def _parse_json_response(raw: str) -> dict:
    cleaned = re.sub(r"```json\s*", "", raw)
    cleaned = re.sub(r"```\s*", "", cleaned)
    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    raise ValueError(
        f"Could not parse Gemini response as JSON.\n"
        f"Raw response (first 500 chars):\n{raw[:500]}"
    )
