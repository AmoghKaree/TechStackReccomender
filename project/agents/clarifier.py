import json
import time
from utils.claude_client import call_claude_json, is_mock_mode
from utils.mock_data import MOCK_CLARIFIER_RESPONSE

SYSTEM_PROMPT = """You are a senior technical consultant. Your job is to take a vague 
project description from a developer and extract structured, actionable requirements 
that will inform technology selection.

Analyze the project description and produce a JSON object with EXACTLY these keys:

{
  "project_summary": "1-2 sentence summary of what the user wants to build",
  "project_type": "web_app | mobile_app | api_service | data_pipeline | desktop_app | cli_tool | other",
  "scale": "small | medium | large | enterprise",
  "team_size": "solo | small_team | medium_team | large_team",
  "budget": "free_tier | low | moderate | high | unlimited",
  "performance_requirements": "low | moderate | high | critical",
  "tech_familiarity": {
    "frontend": "beginner | intermediate | advanced",
    "backend": "beginner | intermediate | advanced",
    "databases": "beginner | intermediate | advanced",
    "devops": "beginner | intermediate | advanced"
  },
  "key_features": ["list", "of", "core", "features"],
  "constraints": ["any explicit constraints or preferences mentioned"],
  "assumptions": ["things you inferred that were not explicitly stated"]
}

Rules:
- If the user does not mention something, infer a REASONABLE default and list it 
  under "assumptions"
- Be conservative: prefer "moderate" over extreme values when uncertain
- Extract every concrete detail the user provides — do not lose information
- Respond with ONLY the JSON object. No explanation, no markdown fences."""


def clarifier_agent(state: dict) -> dict:
    if is_mock_mode():
        time.sleep(1)
        state["requirements"] = MOCK_CLARIFIER_RESPONSE
        return state

    raw_input = state["raw_input"]

    user_message = (
        f"Here is the project description from the user:\n\n"
        f"---\n{raw_input}\n---\n\n"
        f"Extract structured requirements from this description."
    )

    requirements = call_claude_json(
        system_prompt=SYSTEM_PROMPT,
        user_message=user_message,
    )

    state["requirements"] = requirements
    return state
