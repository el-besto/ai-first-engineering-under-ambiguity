"""LangGraph workflow and state inspection commands."""

import json
from pathlib import Path

import typer

from app.adapters.document_intake.fake import FakeDocumentStore
from app.adapters.evals.fake import FakeEvaluationRecorder
from app.adapters.model.fake import FakeModelAdapter
from app.adapters.model.live_chat_model_adapter import LiveChatModelAdapter
from app.adapters.policy_lookup.fake import FakePolicyLookup
from app.adapters.review_queue.fake import FakeReviewQueue
from app.adapters.safety.fake import FakePIIGuardrail
from app.interface_adapters.orchestrators.triage_graph_factory import (
    AdapterRegistry,
    build_triage_graph,
)
from drivers.cli.config import settings
from drivers.cli.utils.console import print_error, print_info, print_success

app = typer.Typer(help="LangGraph debugging and execution tools.")


def get_cli_triage_graph():
    """Builds the triage graph for CLI execution."""
    import os

    import dspy

    from app.adapters.safety.vaultless_guardrail import VaultlessPIIGuardrail

    if settings.llm_main_api_key:
        model_adapter = LiveChatModelAdapter(
            model_name="gpt-4o-mini",
            api_key=settings.llm_main_api_key,
        )
    else:
        model_adapter = FakeModelAdapter()

    if settings.llm_guardrail_secret_key:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        model_path = os.path.join(base_dir, "app", "adapters", "safety", "compiled_pii_extractor.json")
        if settings.llm_guardrail_model:
            lm = dspy.LM(
                settings.llm_guardrail_model,
                api_base=settings.llm_guardrail_api_base or "http://localhost:11434",
                api_key=settings.llm_guardrail_api_key,
            )
            dspy.settings.configure(lm=lm)
        pii_guardrail = VaultlessPIIGuardrail(
            secret_key_hex=settings.llm_guardrail_secret_key, compiled_model_path=model_path
        )
    else:
        pii_guardrail = FakePIIGuardrail()

    adapters = AdapterRegistry(
        document_store=FakeDocumentStore(),
        policy_lookup=FakePolicyLookup(),
        review_queue=FakeReviewQueue(),
        pii_guardrail=pii_guardrail,
        model=model_adapter,
        evaluation_recorder=FakeEvaluationRecorder(),
    )
    return build_triage_graph(adapters)


@app.command()
def run(
    fixture: str = typer.Argument(
        ...,
        help="The fixture scenario. Options: [COMPLETE, MISSING, AMBIGUOUS]",
    ),
) -> None:
    """Execute the graph head-less using a predefined fake data fixture scenario."""
    import dataclasses
    import typing

    from app.entities.claim_intake_bundle import ClaimIntakeBundle
    from app.interface_adapters.orchestrators.triage_graph_state import (
        TriageGraphState,
        map_state_to_triage_result,
    )

    scenario = fixture.upper()
    if scenario == "MISSING":
        bundle = ClaimIntakeBundle.fake_missing_information()
    elif scenario == "AMBIGUOUS":
        bundle = ClaimIntakeBundle.fake_ambiguous()
    elif scenario == "COMPLETE":
        bundle = ClaimIntakeBundle.fake_complete()
    else:
        print_error(f"Unknown fixture '{fixture}'. Use COMPLETE, MISSING, or AMBIGUOUS")
        raise typer.Exit(code=1)

    print_info(f"Executing graph with fixture scenario: {scenario}...")
    graph = get_cli_triage_graph()

    initial_state = {"claim_bundle": bundle}

    try:
        result = typing.cast(TriageGraphState, graph.invoke(initial_state))
        triage_result = map_state_to_triage_result(result)
        print_success("Graph execution complete!")
        print_info(json.dumps(dataclasses.asdict(triage_result), indent=2))
    except Exception as e:
        print_error(f"Graph execution failed: {e}")
        raise typer.Exit(code=1) from e


@app.command()
def trace(
    output: str | None = typer.Option(
        None, help="Output image file to save the Mermaid diagram to. Defaults to out/graph/<timestamp>.png"
    ),
) -> None:
    """Generate and save the LangGraph Mermaid topology as a PNG image."""
    from datetime import datetime

    if output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = f"out/graph/{timestamp}.png"

    # Ensure parent directory exists
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print_info(f"Generating LangGraph Mermaid topology image to {output_path}...")
    graph = get_cli_triage_graph()
    try:
        png_data = graph.get_graph().draw_mermaid_png()
        with open(output_path, "wb") as f:
            f.write(png_data)
        print_success(f"Successfully wrote trace image to {output_path}")
    except Exception as e:
        print_error(f"Failed to generate trace image: {e}")
        raise typer.Exit(code=1) from e
