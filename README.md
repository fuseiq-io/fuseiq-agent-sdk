# FuseIQ Agent SDK — Connect any AI agent in 3 lines

[![PyPI version](https://img.shields.io/pypi/v/fuseiq-agent)](https://pypi.org/project/fuseiq-agent/)
[![npm version](https://img.shields.io/npm/v/@fuseiq/agent-sdk)](https://www.npmjs.com/package/@fuseiq/agent-sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/abbasi8586/fuseiq-agent-sdk?style=social)](https://github.com/abbasi8586/fuseiq-agent-sdk)

**Connect any AI agent to a live dashboard. No infrastructure. 3 lines of code.**

```python
from fuseiq_agent import FuseIQAgent

agent = FuseIQAgent(api_key="fk_live_your_key", name="MyAgent")
agent.heartbeat("online", task="Processing emails")
```

Your agent appears **live** in the [FuseIQ](https://fuseiq.io) dashboard — status, logs, costs, all in real-time.

> **FuseIQ v2.2.6** — Outcome OS for governed agent fleets: Quick Start, Swarm Canvas, Library (Blueprints + Playbooks), Content Studio, and 157+ integrations. [Sign up free →](https://fuseiq.io/signup)

### Ecosystem

| Repo | Purpose |
|------|---------|
| **fuseiq-agent-sdk** (this repo) | Python + Node SDK — connect agents in 3 lines |
| [fuseiq-templates](https://github.com/abbasi8586/fuseiq-templates) | Ready-to-run example agents |
| [fuseiq-cli](https://github.com/abbasi8586/fuseiq-cli) | Terminal deploy and monitor |

Docs: [fuseiq.io/docs](https://fuseiq.io/docs) · Help: [fuseiq.io/help](https://fuseiq.io/help) · Changelog: [fuseiq.io/changelog](https://fuseiq.io/changelog)

---

## Why FuseIQ?

| Feature | FuseIQ | n8n | LangChain | CrewAI | Dify |
|---------|--------|-----|-----------|--------|------|
| Live agent dashboard | ✅ Real-time | ❌ | ❌ | ❌ | ❌ |
| Multi-agent orchestration | ✅ Visual canvas | ✅ | ❌ | ✅ | ✅ |
| White-label reselling | ✅ Built-in | ❌ | ❌ | ❌ | ❌ |
| Bring your own storage | ✅ S3/R2/Minio | ❌ | ❌ | ❌ | ❌ |
| 50+ LLM providers | ✅ Direct + BYOK | ✅ | ✅ | ✅ | ✅ |
| Free tier | ✅ 2 agents | ✅ | ✅ | ✅ | ✅ |
| Open source | ✅ SDK | ✅ Core | ✅ SDK | ✅ Framework | ✅ Core |

---

## Quick Start (Python)

### Install

```bash
pip install fuseiq-agent
```

### Connect an agent

```python
from fuseiq_agent import FuseIQAgent
import time

agent = FuseIQAgent(
    api_key="fk_live_your_key",
    name="My Newsletter Agent",
    agent_id="newsletter-v1"  # optional — stable ID for reconnection
)

# Report status
agent.heartbeat("online", task="Processing incoming emails")

# Log progress
agent.log("Starting NLP pipeline...")

while True:
    # ... your agent logic here ...
    agent.heartbeat("online", task="Waiting for new emails")
    time.sleep(30)
```

### View in dashboard

Your agent appears at **fuseiq.io/dashboard** with live status, execution history, and cost tracking.

---

## Quick Start (Node.js)

```bash
npm install @fuseiq/agent-sdk
```

```javascript
const { FuseIQAgent } = require('@fuseiq/agent-sdk');

const agent = new FuseIQAgent({
  apiKey: 'fk_live_your_key',
  name: 'My Node Agent',
});

agent.heartbeat('online', { task: 'Running analysis' });
```

---

## API Reference

### `FuseIQAgent(apiKey, name, options)`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `apiKey` | string | required | API key from fuseiq.io/settings/api-keys |
| `name` | string | required | Display name in dashboard |
| `options.agentId` | string | auto-generated | Stable ID for reconnection |
| `options.framework` | string | "Custom" | One of: Custom, CrewAI, LangChain, AutoGPT, OpenAI, Claude, Gemini |
| `options.baseUrl` | string | "https://api.fuseiq.io" | API endpoint |

### `.heartbeat(status, options)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | string | `"online"`, `"idle"`, `"busy"`, or `"offline"` |
| `options.task` | string | Current task description (shows in dashboard) |
| `options.metadata` | object | Custom key-value data |

Returns: `{ success: true, agent_id: "uuid" }`

### `.log(message)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `message` | string | Log line to append to agent's timeline |

### `.sendOutput(output)`

Send structured output (JSON, text, file reference) — appears as an artifact in the dashboard.

---

## Examples

Check out the [examples](./examples) directory:

- [Quickstart](./examples/quickstart.py) — Connect any script in 3 lines
- [CrewAI Integration](./examples/crewai-agent.py) — Wrap a CrewAI agent
- [Custom Agent](./examples/custom-agent.py) — Full-featured agent with task loop

---

## Pricing

| Plan | Agents | Cost |
|------|--------|------|
| Free | 2 | $0 |
| Starter | 5 | $39/mo |
| Pro | 25 | $99/mo |
| Team Plus | 100 | $299/mo |
| Enterprise | Unlimited | $349/mo |

[See full pricing →](https://fuseiq.io/pricing)

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

- Report bugs via [GitHub Issues](https://github.com/abbasi8586/fuseiq-agent-sdk/issues)
- Submit PRs for new features, examples, or docs
- Join our [Discord](https://discord.gg/pDFgmqkf)

---

## Links

- [Documentation](https://fuseiq.io/help)
- [Dashboard](https://fuseiq.io)
- [Pricing](https://fuseiq.io/pricing)
- [Changelog](https://fuseiq.io/changelog)
- [Community Discord](https://discord.gg/pDFgmqkf)

---

**Star this repo** ⭐ — help other developers find FuseIQ.

[![Twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fabbasi8586%2Ffuseiq-agent-sdk)](https://twitter.com/intent/tweet?text=Connect%20any%20AI%20agent%20to%20a%20live%20dashboard%20in%203%20lines%20of%20code.%20No%20infrastructure%20needed.&url=https://github.com/abbasi8586/fuseiq-agent-sdk)
