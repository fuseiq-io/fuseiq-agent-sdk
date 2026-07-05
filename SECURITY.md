# Security

## Reporting vulnerabilities

**Do not** open public GitHub issues for security bugs in the **hosted platform** (fuseiq.io).

Email **hello@fuseiq.io** with:

- Description and impact
- Steps to reproduce (SDK/CLI/template issues)
- Your GitHub handle (optional)

We respond within **72 hours** for confirmed reports.

## Scope

| In scope | Out of scope |
|----------|----------------|
| fuseiq-agent-sdk, fuseiq-cli, fuseiq-templates (this repo) | fuseiq.io hosted platform (email only) |
| Dependency vulnerabilities in public repos | Other users' workspaces without permission |
| Good-faith research on **public MIT repos** | Billing, Paddle, marketplace payout internals |

## Safe harbor

Good-faith security research on **public repos only** is welcome.

**Never open-source or share:** Platform monorepo (billing, Paddle, marketplace payouts); Multi-tenant Supabase schema + RLS policies; OAuth credential encryption and integration dispatch.

## Community safety

- Never commit API keys or `.env` files in PRs
- Redact workspace IDs in screenshots and Discord posts
- Join [Discord](https://discord.gg/pDFgmqkf) #builders-lounge before large changes
