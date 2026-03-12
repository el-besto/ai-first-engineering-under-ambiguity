"""LLM and Provider management commands."""

import json
import time
import urllib.error
import urllib.request

import typer

from drivers.cli.config import settings
from drivers.cli.utils.console import print_error, print_info, print_success

app = typer.Typer(help="LLM Provider and Quota validation tools.")


@app.command()
def quota(
    target: str = typer.Option(
        "main",
        "--target",
        "-t",
        help="Target LLM environment to check (e.g. main, guardrail)",
    ),
) -> None:
    """Verify API key validity, print available models, and check ratelimits.

    Currently supports checking OpenAI configuration.
    """
    if target != "main":
        print_error(f"Target '{target}' check is not yet implemented.")
        raise typer.Exit(code=1)

    api_key = settings.openai_api_key or settings.llm_main_api_key
    if not api_key:
        print_error("Error: OPENAI_API_KEY or LLM_MAIN_API_KEY environment variable is not set.")
        raise typer.Exit(code=1)

    print_info("Checking OpenAI API Key...")

    req = urllib.request.Request("https://api.openai.com/v1/models", headers={"Authorization": f"Bearer {api_key}"})

    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print_success("API Key is VALID.")
                models_data = json.loads(response.read().decode())
                models = [m["id"] for m in models_data.get("data", [])]

                core_chat_models = sorted(
                    [
                        m
                        for m in models
                        if m.startswith("gpt-4") or m.startswith("gpt-3.5") or m.startswith("o1") or m.startswith("o3")
                    ]
                )

                print_info(f"\nDiscovered {len(models)} total models. Available Core Chat Models:")
                for m in core_chat_models:
                    print_info(f"  - {m}")
    except urllib.error.HTTPError as e:
        print_error(f"Failed to validate API key. Status code: {e.code}")
        print_error(e.read().decode())
        raise typer.Exit(code=1) from e

    print_info("\nChecking Rate Limits and Quota via a test ChatCompletion...")

    data = json.dumps(
        {"model": "gpt-4.1-mini ", "messages": [{"role": "user", "content": "Hi"}], "max_tokens": 1}
    ).encode("utf-8")

    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=data,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req) as response:
            headers = response.headers
            print_success("Chat Completion Test: SUCCESS\n")
            print_info("-" * 50)
            print_info("Rate Limit & Quota Indicators:")
            print_info(f"  Requests Limit:    {headers.get('x-ratelimit-limit-requests', 'N/A')}")
            print_info(f"  Requests Remaining:{headers.get('x-ratelimit-remaining-requests', 'N/A')}")
            print_info(f"  Tokens Limit:      {headers.get('x-ratelimit-limit-tokens', 'N/A')}")
            print_info(f"  Tokens Remaining:  {headers.get('x-ratelimit-remaining-tokens', 'N/A')}")
            print_info(f"  Reset Requests:    {headers.get('x-ratelimit-reset-requests', 'N/A')}")
            print_info(f"  Reset Tokens:      {headers.get('x-ratelimit-reset-tokens', 'N/A')}")
            print_info("-" * 50)
            print_info("\nNote: OpenAI no longer explicitly exposes remaining dollar balance via API.")
            print_info("If you have remaining rate limits and requests succeed, your quota is active.")

    except urllib.error.HTTPError as e:
        if e.code == 429:
            print_error("Chat Completion Test: FAILED (Rate Limit / Quota Exceeded)")
            print_info("\nThis typically means your key is valid, but you have NO available quota (insufficient_quota)")
            print_info("or have hit a strict rate limit.")
            error_msg = json.loads(e.read().decode())
            print_info(f"\nError Details: {error_msg.get('error', {}).get('message', 'Unknown 429 error')}")

            headers = e.headers
            print_info("\nRate Limit Headers (if any):")
            print_info(f"  Requests Limit:    {headers.get('x-ratelimit-limit-requests', 'N/A')}")
            print_info(f"  Requests Remaining:{headers.get('x-ratelimit-remaining-requests', 'N/A')}")
            print_info(f"  Tokens Limit:      {headers.get('x-ratelimit-limit-tokens', 'N/A')}")
            print_info(f"  Tokens Remaining:  {headers.get('x-ratelimit-remaining-tokens', 'N/A')}")
        else:
            print_error(f"Chat Completion Test: FAILED. Status code: {e.code}")
            print_info(e.read().decode())


@app.command()
def ping(
    target: str = typer.Option(
        "main",
        "--target",
        "-t",
        help="Target LLM environment to check (e.g. main, guardrail)",
    ),
) -> None:
    """Send a basic 1-token prompt to verify latency and connection."""
    if target != "main":
        print_error(f"Target '{target}' ping is not yet implemented.")
        raise typer.Exit(code=1)

    api_key = settings.openai_api_key or settings.llm_main_api_key
    if not api_key:
        print_error("Error: API Key is not set.")
        raise typer.Exit(code=1)

    print_info(f"Pinging target LLM: {target} (gpt-4.1-mini )...")

    data = json.dumps(
        {"model": "gpt-4.1-mini ", "messages": [{"role": "user", "content": "ping"}], "max_tokens": 1}
    ).encode("utf-8")

    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=data,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )

    start_time = time.time()
    try:
        with urllib.request.urlopen(req) as response:
            latency = (time.time() - start_time) * 1000
            if response.status == 200:
                print_success(f"Pong! Latency: {latency:.2f}ms")
            else:
                print_error(f"Ping failed with status: {response.status}")
    except urllib.error.HTTPError as e:
        latency = (time.time() - start_time) * 1000
        print_error(f"Ping failed! Latency: {latency:.2f}ms. Status: {e.code}")
        print_error(e.read().decode())
        raise typer.Exit(code=1) from e
    except Exception as e:
        print_error(f"Network error during ping: {e}")
        raise typer.Exit(code=1) from e
