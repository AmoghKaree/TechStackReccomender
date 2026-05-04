import sys
import json
import argparse
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

from state import create_initial_state
from agents.clarifier import clarifier_agent
from agents.researcher import researcher_agent
from agents.evaluator import evaluator_agent
from agents.reporter import reporter_agent
from utils.claude_client import set_mock_mode

CONFIDENCE_THRESHOLD = 7.0
MAX_ITERATIONS = 3
OUTPUT_DIR = Path("output")
MOCK_INPUT = "I want to build a SaaS dashboard for tracking fitness metrics. Solo developer, free tier preferred, targeting a few hundred users initially."

console = Console()


def display_banner():
    console.print(Panel.fit(
        "[bold cyan]Tech Stack Recommender[/bold cyan]\n"
        "[dim]An Agentic AI System for Intelligent Technology Selection[/dim]",
        border_style="cyan",
    ))
    console.print()


def display_agent_start(agent_name: str, description: str):
    console.print(f"\n[bold yellow]▶ {agent_name}[/bold yellow]")
    console.print(f"  [dim]{description}[/dim]")


def display_agent_done(agent_name: str, summary: str):
    console.print(f"  [green]✓[/green] {agent_name} complete — {summary}")


def display_scores_table(scores: dict):
    table = Table(title="Evaluation Scores", show_lines=True)
    table.add_column("Category", style="cyan", no_wrap=True)
    table.add_column("Option", style="white")
    table.add_column("Fit", justify="center")
    table.add_column("Learn", justify="center")
    table.add_column("Scale", justify="center")
    table.add_column("Cost", justify="center")
    table.add_column("Community", justify="center")
    table.add_column("AVG", justify="center", style="bold")

    for category, options in scores.items():
        for i, opt in enumerate(options):
            avg = opt.get("average", 0)
            avg_style = "green" if avg >= CONFIDENCE_THRESHOLD else "red"

            table.add_row(
                category if i == 0 else "",
                opt.get("name", "?"),
                str(opt.get("requirements_fit", "?")),
                str(opt.get("learning_curve", "?")),
                str(opt.get("scalability", "?")),
                str(opt.get("cost", "?")),
                str(opt.get("community_support", "?")),
                f"[{avg_style}]{avg}[/{avg_style}]",
            )

    console.print()
    console.print(table)


def display_feedback_loop(iteration: int, weak: list):
    console.print(
        f"\n[bold red]⟳ Feedback Loop (iteration {iteration})[/bold red]"
    )
    console.print(
        f"  Weak categories (avg < {CONFIDENCE_THRESHOLD}): "
        f"[yellow]{', '.join(weak)}[/yellow]"
    )
    console.print(f"  Re-researching and re-evaluating...")


def run_pipeline(user_input: str) -> str:
    display_banner()

    state = create_initial_state(user_input)
    console.print(f"[bold]Project Description:[/bold]\n  {user_input}\n")

    display_agent_start("Clarifier Agent", "Parsing project description into structured requirements...")
    state = clarifier_agent(state)
    req = state["requirements"]
    display_agent_done(
        "Clarifier Agent",
        f"Identified project type: {req.get('project_type', '?')}, "
        f"scale: {req.get('scale', '?')}, "
        f"team: {req.get('team_size', '?')}"
    )
    console.print(f"  [dim]Key features: {req.get('key_features', [])}[/dim]")
    console.print(f"  [dim]Assumptions made: {req.get('assumptions', [])}[/dim]")

    display_agent_start("Researcher Agent", "Researching technology options for each stack category...")
    state = researcher_agent(state)
    categories = list(state["options"].keys())
    total_options = sum(len(v) for v in state["options"].values())
    display_agent_done(
        "Researcher Agent",
        f"Found {total_options} options across {len(categories)} categories: {categories}"
    )

    display_agent_start("Evaluator Agent", "Scoring all options on 5 evaluation dimensions...")
    state = evaluator_agent(state)
    display_agent_done(
        "Evaluator Agent",
        f"Weak categories: {state['weak_categories'] if state['weak_categories'] else 'none'}"
    )
    display_scores_table(state["scores"])

    iteration = 0
    while state["weak_categories"] and iteration < MAX_ITERATIONS:
        iteration += 1
        state["iteration_count"] = iteration
        display_feedback_loop(iteration, state["weak_categories"])

        display_agent_start("Researcher Agent", f"Re-researching: {state['weak_categories']}")
        state = researcher_agent(state)
        display_agent_done("Researcher Agent", "New options generated for weak categories")

        display_agent_start("Evaluator Agent", "Re-scoring updated options...")
        state = evaluator_agent(state)
        display_agent_done(
            "Evaluator Agent",
            f"Weak categories remaining: {state['weak_categories'] if state['weak_categories'] else 'none'}"
        )
        display_scores_table(state["scores"])

    if not state["weak_categories"]:
        console.print(
            f"\n[bold green]✓ All categories pass confidence threshold "
            f"({CONFIDENCE_THRESHOLD}/10) after {iteration} iteration(s)[/bold green]"
        )
    else:
        console.print(
            f"\n[bold yellow]⚠ Max iterations ({MAX_ITERATIONS}) reached. "
            f"Remaining weak categories: {state['weak_categories']}[/bold yellow]"
        )

    state["iteration_count"] = iteration

    display_agent_start("Report Agent", "Generating final recommendation report...")
    state = reporter_agent(state)
    display_agent_done("Report Agent", "Markdown report generated")

    OUTPUT_DIR.mkdir(exist_ok=True)
    report_path = OUTPUT_DIR / "report.md"
    report_path.write_text(state["final_report"], encoding="utf-8")
    console.print(f"\n[bold green]✓ Report saved to {report_path}[/bold green]")

    state_path = OUTPUT_DIR / "full_state.json"
    serializable_state = {k: v for k, v in state.items() if k != "final_report"}
    state_path.write_text(json.dumps(serializable_state, indent=2), encoding="utf-8")
    console.print(f"[dim]  Full state saved to {state_path}[/dim]")

    return state["final_report"]


def main():
    parser = argparse.ArgumentParser(
        description="Tech Stack Recommender — Agentic AI System"
    )
    parser.add_argument(
        "--input", "-i",
        type=str,
        default=None,
        help="Project description (if omitted, will prompt interactively)"
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Run in mock mode with pre-saved responses (no API key needed)"
    )
    args = parser.parse_args()

    if args.mock:
        set_mock_mode(True)
        console.print("[bold magenta]⚡ Running in MOCK MODE (no API calls)[/bold magenta]\n")
        user_input = args.input if args.input else MOCK_INPUT
    elif args.input:
        user_input = args.input
    else:
        console.print("[bold]Describe your project:[/bold]")
        console.print("[dim](What are you building? Include details about scale, team, budget, etc.)[/dim]")
        user_input = input("\n> ").strip()

        if not user_input:
            console.print("[red]No input provided. Exiting.[/red]")
            sys.exit(1)

    report = run_pipeline(user_input)

    console.print("\n" + "=" * 60)
    console.print("[bold cyan]FINAL REPORT[/bold cyan]")
    console.print("=" * 60)
    console.print(report)


if __name__ == "__main__":
    main()
