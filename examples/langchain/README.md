# LangChain + FuseIQ Example

Runnable example showing a **LangChain agent loop** with FuseIQ heartbeats every N steps.

## Prerequisites

- Python 3.10+
- FuseIQ API key ([sign up](https://fuseiq.io/signup) · code `FUSEIQ1M`)
- Optional: OpenAI API key for a live LLM run

## Install

```bash
pip install fuseiq-agent langchain langchain-openai
```

## Run

```bash
export FUSEIQ_API_KEY="fk_live_your_key"
export OPENAI_API_KEY="sk-..."   # optional — demo mode works without it
python langchain_agent.py
```

## What it does

1. Registers a LangChain agent with FuseIQ (`framework="LangChain"`)
2. Runs a small multi-step research loop
3. Sends a FuseIQ **heartbeat every 2 steps** (configurable via `HEARTBEAT_EVERY`)
4. Logs progress to the [FuseIQ dashboard](https://fuseiq.io/dashboard)

## Quick start

New to FuseIQ? Follow the platform guide: **[fuseiq.io/quick-start](https://fuseiq.io/quick-start)**

## Related

- [FuseIQ Agent SDK README](../../README.md)
- [CrewAI example](../crewai-agent.py)
- Issue: [#1 LangChain adapter example](https://github.com/fuseiq-io/fuseiq-agent-sdk/issues/1)
