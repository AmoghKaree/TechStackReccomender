import json
import re
import os
from anthropic import Anthropic

_client: Anthropic | None = None
MOCK_MODE = False


def set_mock_mode(enabled: bool):
    global MOCK_MODE
    MOCK_MODE = enabled


def is_mock_mode() -> bool:
    return MOCK_MODE


def _get_client() -> Anthropic:
    global _client
    if _client is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "ANTHROPIC_API_KEY not set. "
                "Export it before running: export ANTHROPIC_API_KEY=sk-..."
            )
        _client = Anthropic(api_key=api_key)
    return _client


def call_claude(
    system_prompt: str,
    user_message: str,
    model: str = "claude-sonnet-4-20250514",
    max_tokens: int = 4096,
    temperature: float = 0.4,
) -> str:
    client = _get_client()

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message}
        ],
    )

    text_parts = [
        block.text for block in response.content if block.type == "text"
    ]
    return "\n".join(text_parts)


def call_claude_json(
    system_prompt: str,
    user_message: str,
    model: str = "claude-sonnet-4-20250514",
    max_tokens: int = 4096,
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
        f"Could not parse Claude response as JSON.\n"
        f"Raw response (first 500 chars):\n{raw[:500]}"
    )
