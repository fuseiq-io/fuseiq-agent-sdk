"""LangChain integration — agent loop with FuseIQ heartbeats every N steps.

Install:
    pip install fuseiq-agent langchain langchain-openai

Run:
    export FUSEIQ_API_KEY="fk_live_your_key"
    export OPENAI_API_KEY="sk-..."   # optional
    python langchain_agent.py

Quick start: https://fuseiq.io/quick-start
Fixes: fuseiq-io/fuseiq-agent-sdk#1
"""

from __future__ import annotations

import os
import sys
import time
from typing import Callable

from fuseiq_agent import FuseIQAgent

HEARTBEAT_EVERY = 2
RESEARCH_STEPS = (
    "Gather sources on governed agent platforms",
    "Summarize FuseIQ heartbeat patterns",
    "Draft integration checklist",
    "Finalize LangChain adapter notes",
)


def run_demo_loop(on_step: Callable[[int, str], None]) -> str:
    """Simulate a multi-step agent loop when LangChain is unavailable."""
    for index, step in enumerate(RESEARCH_STEPS, start=1):
        on_step(index, step)
        time.sleep(0.4)
    return "LangChain demo loop completed with FuseIQ heartbeats."


def run_langchain_loop(agent: FuseIQAgent) -> str:
    """Run a minimal LangChain loop when dependencies and API keys are present."""
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    messages = [
        SystemMessage(content="You are a concise research assistant."),
        HumanMessage(content="List three benefits of heartbeat monitoring for AI agents."),
    ]

    step_count = 0

    def on_step(step: int, task: str) -> None:
        nonlocal step_count
        step_count = step
        agent.log(f"LangChain step {step}: {task}")
        if step == 1 or step % HEARTBEAT_EVERY == 0:
            agent.heartbeat("busy", task=task, metadata={"step": step, "framework": "LangChain"})

    on_step(1, "Initializing LangChain chat model")
    response = llm.invoke(messages)
    on_step(2, "Received model response")
    agent.heartbeat("idle", task="LangChain run complete")
    return response.content


def main() -> int:
    api_key = os.environ.get("FUSEIQ_API_KEY")
    if not api_key:
        print("Set FUSEIQ_API_KEY before running. Sign up: https://fuseiq.io/signup")
        return 1

    agent = FuseIQAgent(
        api_key=api_key,
        name="LangChain Research Agent",
        framework="LangChain",
    )
    agent.heartbeat("online", task="LangChain agent initialized")

    step_counter = 0

    def on_demo_step(step: int, task: str) -> None:
        nonlocal step_counter
        step_counter = step
        agent.log(f"Step {step}: {task}")
        if step == 1 or step % HEARTBEAT_EVERY == 0:
            agent.heartbeat("busy", task=task, metadata={"step": step})

    try:
        if os.environ.get("OPENAI_API_KEY"):
            result = run_langchain_loop(agent)
        else:
            agent.log("OPENAI_API_KEY not set — running demo loop")
            result = run_demo_loop(on_demo_step)
    except ImportError:
        agent.log("LangChain not installed — running demo loop")
        result = run_demo_loop(on_demo_step)

    agent.heartbeat("idle", task="All steps finished")
    print(result)
    print("View agent activity: https://fuseiq.io/dashboard")
    print("Platform quick start: https://fuseiq.io/quick-start")
    return 0


if __name__ == "__main__":
    sys.exit(main())
