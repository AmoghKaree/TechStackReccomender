# StackAI — AI-Powered Tech Stack Recommender

StackAI is a multi-agent AI pipeline that takes a plain-English project description and returns a scored, justified technology recommendation across five stack categories: **Frontend, Backend, Database, Hosting, and Auth**.

Built with FastAPI + Gemini AI. Runs entirely on Gemini's free tier.


---

## How It Works

Four specialized AI agents run sequentially every time you submit a project:

| Agent | Role |
|---|---|
| **Clarifier** | Parses your description into structured requirements (type, scale, budget, team size) |
| **Researcher** | Finds 2–3 best-fit technology options per stack category |
| **Evaluator** | Scores every option on 5 dimensions (1–10): Requirements Fit, Learning Curve, Scalability, Cost, Community Support |
| **Reporter** | Writes a full markdown report with recommendations, runner-ups, synergy notes, and risk flags |

If any category scores below **7.0/10**, the pipeline automatically re-researches that category and re-evaluates — up to 3 iterations.

---

## Demo

**Landing page** (`/`) — marketing page with live tech logo cloud

**App** (`/app`) — input your project description and get a recommendation

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/AmoghKaree/TechStackReccomender.git
cd TechStackReccomender
```

### 2. Install dependencies

```bash
cd project
pip install -r requirements.txt
```

### 3. Get a free Gemini API key

1. Go to [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Click **Create API key** (no credit card required)
3. Copy the key — it starts with `AIza...`

### 4. Add your key

Create `project/.env`:

```env
GEMINI_API_KEY=AIza...your-key-here
```

### 5. Run the server

```bash
cd project
python -m uvicorn server:app --reload --port 8002
```

Open [http://localhost:8002](http://localhost:8002)

---

## Project Structure

```
TechStackReccomender/
├── project/
│   ├── agents/
│   │   ├── clarifier.py      # Parses project description → structured requirements
│   │   ├── researcher.py     # Finds technology options per category
│   │   ├── evaluator.py      # Scores options on 5 dimensions
│   │   └── reporter.py       # Generates the final markdown report
│   ├── utils/
│   │   ├── claude_client.py  # Gemini API wrapper (call_claude / call_claude_json)
│   │   └── mock_data.py      # Pre-saved responses for offline testing
│   ├── static/
│   │   ├── home.html         # Marketing landing page
│   │   ├── index.html        # App UI (input → loading → results)
│   │   └── favicon.svg       # Site icon
│   ├── server.py             # FastAPI server — routes and pipeline orchestration
│   ├── state.py              # AgentState TypedDict definition
│   ├── main.py               # Original CLI entry point
│   └── requirements.txt
└── README.md
```

---

## CLI Usage

The original CLI still works:

```bash
cd project

# Interactive
python main.py

# With input
python main.py --input "E-commerce platform, 2-person team, moderate budget"

# Mock mode (no API key needed)
python main.py --mock
```

---

## API

### `POST /api/recommend`

**Request body:**
```json
{
  "description": "I want to build a SaaS dashboard...",
  "mock": false
}
```

**Response:**
```json
{
  "requirements": { "project_type": "web_app", "scale": "small", ... },
  "options":      { "frontend": [...], "backend": [...], ... },
  "scores":       { "frontend": [{ "name": "React", "average": 8.8, ... }], ... },
  "weak_categories": [],
  "iteration_count": 0,
  "final_report": "# Tech Stack Recommendation Report\n..."
}
```

---

## Tech Stack (meta)

| Layer | Technology |
|---|---|
| Backend | Python + FastAPI |
| AI | Google Gemini 2.5 Flash (`google-genai`) |
| Frontend | Vanilla HTML/CSS/JS |
| Server | Uvicorn |

---

## Scoring Dimensions

Every technology option is scored **1.0–10.0** on:

- **Requirements Fit** — how well it matches the stated project needs
- **Learning Curve** — from the team's stated familiarity level
- **Scalability** — ability to grow with the project
- **Cost** — alignment with the stated budget constraints
- **Community Support** — ecosystem maturity, docs, and resources

Categories scoring below **7.0** trigger automatic re-research.

---

## Mock Mode

Enable mock mode to test the full pipeline without an API key — pre-saved responses simulate all four agents.

In the UI: toggle **Mock mode** before clicking Analyze.
In the CLI: `python main.py --mock`
