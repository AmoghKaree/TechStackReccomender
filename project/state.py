from typing import TypedDict, Optional


class TechOption(TypedDict, total=False):
    name: str
    description: str
    pros: list[str]
    cons: list[str]


class EvalScores(TypedDict, total=False):
    requirements_fit: float
    learning_curve: float
    scalability: float
    cost: float
    community_support: float
    average: float


class AgentState(TypedDict, total=False):
    raw_input: str
    requirements: dict
    options: dict[str, list[TechOption]]
    scores: dict[str, list[EvalScores]]
    weak_categories: list[str]
    iteration_count: int
    final_report: str


def create_initial_state(user_input: str) -> AgentState:
    return AgentState(
        raw_input=user_input,
        requirements={},
        options={},
        scores={},
        weak_categories=[],
        iteration_count=0,
        final_report=""
    )
