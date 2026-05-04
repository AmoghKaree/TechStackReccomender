import json
import time
from utils.claude_client import call_claude_json, is_mock_mode
from utils.mock_data import MOCK_RESEARCHER_RESPONSE

SYSTEM_PROMPT = """You are a senior software architect with deep knowledge of modern 
technology stacks. Given structured project requirements, recommend 2-3 technology 
options for each stack category.

Respond with ONLY a JSON object in this exact format:

{
  "frontend": [
    {
      "name": "Technology Name",
      "description": "1-2 sentence description of what it is",
      "pros": ["advantage 1", "advantage 2", "advantage 3"],
      "cons": ["disadvantage 1", "disadvantage 2"]
    }
  ],
  "backend": [ ... same structure ... ],
  "database": [ ... same structure ... ],
  "hosting": [ ... same structure ... ],
  "auth": [ ... same structure ... ]
}

Rules:
- Provide EXACTLY 2-3 options per category
- Tailor choices to the project requirements (scale, budget, team expertise)
- Include at least one "safe/popular" choice and one "modern/emerging" choice per category
- Be specific — name exact technologies, not categories (e.g., "PostgreSQL" not "SQL database")
- Pros and cons should be specific to this project's requirements, not generic
- Respond with ONLY valid JSON. No markdown, no explanation."""

TARGETED_SYSTEM_PROMPT = """You are a senior software architect. The previous research 
round produced low-confidence results for certain stack categories. You need to 
re-research ONLY the weak categories listed below and provide better, more tailored options.

Respond with ONLY a JSON object mapping each weak category to a list of 2-3 options:

{
  "category_name": [
    {
      "name": "Technology Name",
      "description": "1-2 sentence description",
      "pros": ["advantage 1", "advantage 2", "advantage 3"],
      "cons": ["disadvantage 1", "disadvantage 2"]
    }
  ]
}

Rules:
- Only include the categories that need re-research (listed below)
- Provide DIFFERENT options than the previous round where possible
- Focus on better fit for the stated requirements
- Respond with ONLY valid JSON. No markdown, no explanation."""


def researcher_agent(state: dict) -> dict:
    if is_mock_mode():
        time.sleep(1.5)
        state["options"] = MOCK_RESEARCHER_RESPONSE
        return state

    requirements = state["requirements"]
    weak_categories = state.get("weak_categories", [])

    if weak_categories:
        options = _research_targeted(requirements, weak_categories, state.get("options", {}))
    else:
        options = _research_full(requirements)

    state["options"] = options
    return state


def _research_full(requirements: dict) -> dict:
    user_message = (
        f"Here are the structured project requirements:\n\n"
        f"```json\n{json.dumps(requirements, indent=2)}\n```\n\n"
        f"Recommend 2-3 technology options for each of these categories: "
        f"frontend, backend, database, hosting, auth."
    )

    return call_claude_json(
        system_prompt=SYSTEM_PROMPT,
        user_message=user_message,
    )


def _research_targeted(requirements: dict, weak_categories: list, existing_options: dict) -> dict:
    previous_picks = {}
    for cat in weak_categories:
        if cat in existing_options:
            previous_picks[cat] = [opt.get("name", "unknown") for opt in existing_options[cat]]

    user_message = (
        f"Project requirements:\n"
        f"```json\n{json.dumps(requirements, indent=2)}\n```\n\n"
        f"Weak categories that need re-research: {weak_categories}\n\n"
        f"Previous options that scored poorly:\n"
        f"```json\n{json.dumps(previous_picks, indent=2)}\n```\n\n"
        f"Provide better-fitting alternatives for ONLY the weak categories."
    )

    new_options = call_claude_json(
        system_prompt=TARGETED_SYSTEM_PROMPT,
        user_message=user_message,
    )

    merged = dict(existing_options)
    for cat, opts in new_options.items():
        merged[cat] = opts

    return merged
