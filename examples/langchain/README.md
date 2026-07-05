# LangChain Agent + FuseIQ Heartbeat

A governed LangChain agent example showing how to integrate
[FuseIQ](https://fuseiq.io) heartbeat monitoring into any
LangChain agent loop.

## Quick Start

```bash
# 1. Set API keys
export FUSEIQ_API_KEY="fk_live_your_key"   # from fuseiq.io/settings/api-keys
export OPENAI_API_KEY="sk-your-key"

# 2. Install dependencies
pip install fuseiq-agent langchain langchain-openai

# 3. Run the example
cd examples/langchain
python langchain_agent.py
```

## What It Does

1. **Creates a LangChain agent** with search, math, and weather tools
2. **Wraps tool calls** so every invocation reports to FuseIQ
3. **Heartbeat every N steps** — the agent's status updates live in
   the FuseIQ dashboard as it runs
4. **Logs all actions** — tool calls, user input, and final output
   are recorded for governance and debugging

## Dashboard

Open [https://fuseiq.io/dashboard](https://fuseiq.io/dashboard) while
the script runs — you'll see your "LangChain Governor" agent appear
with real-time status transitions (online → busy → idle) and a full
log trail.

## Customizing

- **Heartbeat frequency**: change `heartbeat_every` in `governed_invoke()`
- **Framework label**: passes `framework="LangChain"` to FuseIQ so
  your dashboard shows which framework each agent uses
- **Add more tools**: define new `@tool` functions — the heartbeat
  wrapper applies automatically

## See Also

- [FuseIQ Quick Start](https://fuseiq.io/quick-start)
- [FuseIQ Agent SDK Docs](https://github.com/fuseiq-io/fuseiq-agent-sdk)
- [LangChain Documentation](https://python.langchain.com)
