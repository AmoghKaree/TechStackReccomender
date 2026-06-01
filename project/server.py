import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).parent))

from state import create_initial_state
from agents.clarifier import clarifier_agent
from agents.researcher import researcher_agent
from agents.evaluator import evaluator_agent
from agents.reporter import reporter_agent
from utils.claude_client import set_mock_mode

CONFIDENCE_THRESHOLD = 7.0
MAX_ITERATIONS = 3

app = FastAPI(title="TechStackRecommender API")

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


class RecommendRequest(BaseModel):
    description: str
    mock: bool = False


@app.get("/")
async def home():
    return FileResponse(str(static_dir / "home.html"))

@app.get("/app")
async def app_page():
    return FileResponse(str(static_dir / "index.html"))


@app.post("/api/recommend")
async def recommend(req: RecommendRequest):
    import asyncio
    from fastapi import HTTPException
    loop = asyncio.get_event_loop()
    try:
        with ThreadPoolExecutor() as pool:
            result = await loop.run_in_executor(pool, _run_pipeline, req.description, req.mock)
        return result
    except Exception as e:
        import traceback
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}\n{traceback.format_exc()}")


def _run_pipeline(description: str, mock: bool) -> dict:
    set_mock_mode(mock)

    state = create_initial_state(description)

    state = clarifier_agent(state)
    state = researcher_agent(state)
    state = evaluator_agent(state)

    iteration = 0
    while state["weak_categories"] and iteration < MAX_ITERATIONS:
        iteration += 1
        state["iteration_count"] = iteration
        state = researcher_agent(state)
        state = evaluator_agent(state)

    state["iteration_count"] = iteration
    state = reporter_agent(state)

    return {
        "requirements": state.get("requirements", {}),
        "options": state.get("options", {}),
        "scores": state.get("scores", {}),
        "weak_categories": state.get("weak_categories", []),
        "iteration_count": state.get("iteration_count", 0),
        "final_report": state.get("final_report", ""),
    }
