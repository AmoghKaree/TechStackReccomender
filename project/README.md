# Tech Stack Recommender

**An Agentic AI System for Intelligent Technology Selection**

CS301 — Introduction to AI Systems | Professor Akm Islam

---

## The Problem

Developers — especially those newer to a domain — frequently struggle to choose the right technologies for a project. The technology landscape is vast, rapidly changing, and highly context-dependent. Variables like team size, budget, performance requirements, and existing familiarity all influence the ideal choice, and a single Google search rarely produces a personalized, justified answer.

This project builds a multi-agent AI system that takes a natural language project description and produces a scored, justified technology stack recommendation through iterative reasoning. Rather than producing a single-shot answer, the system routes the problem through four specialized agents, each responsible for a distinct stage of reasoning. The output is a structured Markdown report that a developer or team could use directly when starting a new project.

This problem is a natural fit for an agentic workflow for several reasons. The answer cannot be correct in a single step because vague requirements must first be clarified before meaningful research can begin. Different subtasks require different expertise — clarifying requirements, researching technologies, evaluating fitness, and writing reports are fundamentally different skills. There is a natural evaluation mechanism in the form of numerical confidence scores on recommendations. And failure at one stage should change what happens next — if a recommendation scores poorly, the system should re-research that category rather than blindly proceeding.

---

## System Design

The system is composed of four specialized agents connected by a shared state dictionary. Control flows sequentially through the pipeline, with a conditional feedback loop between the Evaluator and Researcher agents.

```
User Input (project description)
      │
      ▼
┌──────────────────┐
│  Clarifier Agent  │ → Structured requirements dict
└────────┬─────────┘
         ▼
┌──────────────────┐
│  Researcher Agent │ → 2-3 tech options per category
└────────┬─────────┘
         ▼
┌──────────────────┐
│  Evaluator Agent  │ → Scored options + weak category flags
└────────┬─────────┘
         │
         ▼  ┌─────────────────────────────────┐
    ╔════╧══╧═══╗                              │
    ║ Confidence ║──── avg < 7.0 ──► Re-research│
    ║   Check    ║     (max 3x)       weak cats │
    ╚════╤══════╝                              │
         │ all pass                             │
         ▼                    ◄─────────────────┘
┌──────────────────┐
│   Report Agent    │ → Final Markdown recommendation
└──────────────────┘
```

**Clarifier Agent** takes the raw user description and extracts structured requirements including project type, scale, budget, team size, tech familiarity across four domains, key features, explicit constraints, and assumptions it had to infer. This structured output becomes the foundation every downstream agent relies on.

**Researcher Agent** breaks the stack into five categories (frontend, backend, database, hosting, auth) and identifies 2-3 candidate technologies per category tailored to the requirements. When called during a feedback loop iteration, it only re-researches the weak categories and keeps the strong ones intact.

**Evaluator Agent** scores each technology option on five dimensions — requirements fit, learning curve, scalability, cost, and community support — each on a 1 to 10 scale. It computes an average score per option and flags any category where even the best option scores below 7.0.

**Report Agent** compiles everything into a readable Markdown report with a top recommendation per category, runner-up comparisons, stack synergy analysis, tradeoffs and risks, and areas of uncertainty.

All agents communicate through a single shared state dictionary rather than calling each other directly. This keeps agents loosely coupled — any agent can be swapped, tested, or modified independently. The orchestrator in main.py controls the execution order and manages the feedback loop.

The file structure reflects this separation of concerns:

```
project/
├── main.py              ← Orchestrator: controls agent execution and feedback loop
├── state.py             ← Shared state dict schema with type hints
├── agents/
│   ├── clarifier.py     ← Clarifier Agent
│   ├── researcher.py    ← Researcher Agent
│   ├── evaluator.py     ← Evaluator Agent
│   └── reporter.py      ← Report Agent
├── utils/
│   ├── claude_client.py ← Centralized Anthropic API wrapper
│   └── mock_data.py     ← Pre-saved responses for mock/demo mode
├── output/
│   └── report.md        ← Final generated report (created at runtime)
└── requirements.txt     ← Python dependencies
```

---

## How the Agentic Workflow Operates

The orchestrator in main.py drives the entire pipeline. On startup, it collects a project description from the user (either via command line argument or interactive prompt) and initializes a shared state dictionary with that raw input. It then calls each agent in sequence, passing the state forward.

The Clarifier Agent runs first. It sends the raw description to Claude with a system prompt instructing it to extract a structured JSON object covering project type, scale, budget, team size, familiarity levels, key features, constraints, and assumptions. The parsed JSON is written back to the state under the `requirements` key.

The Researcher Agent runs next. It reads the requirements and asks Claude to recommend 2-3 technology options for each of the five stack categories. Each option includes a name, description, pros, and cons specific to the project requirements. The results are written to the state under the `options` key.

The Evaluator Agent then scores every option. It receives both the requirements and the options, and returns a score from 1 to 10 on each of the five evaluation dimensions: requirements fit, learning curve, scalability, cost, and community support. It computes an average for each option and identifies any category where the best available option still falls below the 7.0 confidence threshold. These weak categories are written to the state.

The feedback loop is the core agentic behavior that separates this system from a simple chain of prompts. After evaluation, the orchestrator checks the weak categories list. If any categories are flagged, it sends the Researcher Agent back to re-research only those categories with instructions to propose different alternatives than the previous round. The Evaluator then re-scores the updated options. This loop repeats until either all categories pass the 7.0 threshold or a maximum of 3 iterations is reached:

```python
THRESHOLD = 7.0
MAX_ITERATIONS = 3

while iteration < MAX_ITERATIONS:
    weak = [c for c in scores if best_avg(scores[c]) < THRESHOLD]
    if not weak:
        break
    state['weak_categories'] = weak
    researcher_agent(state)
    evaluator_agent(state)
    iteration += 1

report_agent(state)
```

The iteration cap prevents infinite loops. If a category still fails after 3 attempts, the Report Agent explicitly acknowledges it as an area of uncertainty in the final output rather than hiding it.

Finally, the Report Agent reads the full state and generates a Markdown report with a recommendation per category, runner-up comparisons, a stack synergy paragraph, tradeoffs and risks, and evaluation metadata. The report is saved to `output/report.md`.

Throughout execution, the terminal displays live progress using the rich library — colored agent headers, a formatted scores table after each evaluation pass, and feedback loop status indicators.

---

## Key Results and Observations

A sample run was performed with the following input:

> "I want to build a SaaS dashboard for tracking fitness metrics. Solo developer, free tier preferred, targeting a few hundred users initially."

The Clarifier Agent correctly identified this as a small-scale web application with a solo developer, free-tier budget, and moderate performance requirements. It inferred beginner-to-intermediate familiarity across all domains and flagged this as an assumption.

The Researcher Agent proposed 15 total options across 5 categories, including React, Vue, and Svelte for frontend; FastAPI, Express.js, and Django for backend; Supabase, PlanetScale, and Firebase for database; Vercel, Railway, and Fly.io for hosting; and Supabase Auth, Clerk, and Auth0 for authentication.

The Evaluator Agent scored all options and every category passed the 7.0 confidence threshold on the first pass, meaning the feedback loop did not need to trigger. The final recommendations were React (8.8), FastAPI (8.7), Supabase (8.7), Vercel (8.7), and Supabase Auth (8.7). The system correctly identified Supabase as a synergistic centerpiece, recommending it for both database and auth to reduce integration complexity for a solo developer.

Several observations emerged from building and testing this system:

The shared state pattern proved effective for debugging. Because every agent writes to a single dictionary that gets dumped to `full_state.json`, it is easy to inspect exactly what each agent produced and trace where issues originate. This is significantly easier to debug than a system where agents call each other directly.

The feedback loop adds genuine value but rarely triggers more than once. In most test cases, the initial research pass produces reasonable options. When the loop does trigger, it is typically for the hosting or auth categories where free-tier constraints create a narrower solution space. This matches the intuition that some technology decisions are inherently harder to optimize under tight budget constraints.

Separating agents into distinct system prompts produces noticeably better output than a single monolithic prompt. The Evaluator in particular benefits from not having to simultaneously research and judge — it can focus entirely on critical scoring without the cognitive load of also generating options.

The 7.0 threshold was chosen empirically. Scores below 7.0 tend to correspond to recommendations that feel under-justified or forced, while scores above 7.0 consistently produce recommendations with clear, specific reasoning.

A limitation of the current system is that the Researcher Agent relies on Claude's training data rather than live web search. This means pricing information and release dates may be outdated. A future improvement would integrate real-time web search for current pricing and compatibility data.

The sample output from this run is included in `output/report.md`.

---

## How to Run

### Prerequisites
- Python 3.10+
- pip

### Setup
```bash
pip install -r requirements.txt
```

### Mock Mode (no API key needed)
To run the full pipeline with pre-saved responses for demonstration purposes:
```bash
python main.py --mock
```
This executes the complete workflow — Clarifier, Researcher, Evaluator, feedback loop check, and Report Agent — using realistic pre-saved data. The terminal output, scores table, and final report are all generated as they would be in a live run.

### Live Mode (requires Anthropic API key)
To run with real API calls against Claude:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python main.py --input "I want to build a real-time chat app for 10k users"
```
Or run interactively without the --input flag:
```bash
python main.py
```

### Output
- `output/report.md` — the final Markdown recommendation report
- `output/full_state.json` — the complete pipeline state for inspection

---

*Built as a course project for CS301 — Introduction to AI Systems*
