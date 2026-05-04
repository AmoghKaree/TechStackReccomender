import json
import time
from utils.claude_client import call_claude_json, is_mock_mode
from utils.mock_data import MOCK_EVALUATOR_RESPONSE

CONFIDENCE_THRESHOLD = 7.0

SYSTEM_PROMPT = """You are a technology evaluation expert. Given project requirements 
and a set of technology options per stack category, score each option on 5 dimensions.

Respond with ONLY a JSON object in this exact format:

{
  "category_name": [
    {
      "name": "Technology Name",
      "requirements_fit": 8.0,
      "learning_curve": 7.5,
      "scalability": 9.0,
      "cost": 8.0,
      "community_support": 8.5,
      "average": 8.2,
      "justification": "Brief 1-2 sentence explanation of the scores"
    }
  ]
}

Scoring rules:
- Each dimension is scored 1.0 to 10.0 (use one decimal place)
- "average" must be the arithmetic mean of the 5 scores, rounded to 1 decimal
- Be HONEST and CRITICAL — do not inflate scores
- A score of 7+ means "good fit for this project"
- A score below 5 means "poor fit — likely problematic"
- Learning curve should be scored FROM THE TEAM'S PERSPECTIVE (consider their stated familiarity)
- Cost should reflect the stated budget constraints
- Justification should reference specific project requirements

Respond with ONLY valid JSON. No markdown, no explanation."""


def evaluator_agent(state: dict) -> dict:
    if is_mock_mode():
        time.sleep(1.5)
        scores = MOCK_EVALUATOR_RESPONSE
        weak_categories = _find_weak_categories(scores)
        state["scores"] = scores
        state["weak_categories"] = weak_categories
        return state

    requirements = state["requirements"]
    options = state["options"]

    user_message = (
        f"Project requirements:\n"
        f"```json\n{json.dumps(requirements, indent=2)}\n```\n\n"
        f"Technology options to evaluate:\n"
        f"```json\n{json.dumps(options, indent=2)}\n```\n\n"
        f"Score every option in every category on the 5 dimensions."
    )

    scores = call_claude_json(
        system_prompt=SYSTEM_PROMPT,
        user_message=user_message,
    )

    weak_categories = _find_weak_categories(scores)

    state["scores"] = scores
    state["weak_categories"] = weak_categories
    return state


def _find_weak_categories(scores: dict) -> list[str]:
    weak = []

    for category, option_scores in scores.items():
        if not option_scores:
            weak.append(category)
            continue

        best_avg = max(
            _safe_average(opt) for opt in option_scores
        )

        if best_avg < CONFIDENCE_THRESHOLD:
            weak.append(category)

    return weak


def _safe_average(option: dict) -> float:
    if "average" in option:
        try:
            return float(option["average"])
        except (TypeError, ValueError):
            pass

    dims = [
        "requirements_fit", "learning_curve", "scalability",
        "cost", "community_support"
    ]
    values = []
    for d in dims:
        if d in option:
            try:
                values.append(float(option[d]))
            except (TypeError, ValueError):
                continue

    return sum(values) / len(values) if values else 0.0
