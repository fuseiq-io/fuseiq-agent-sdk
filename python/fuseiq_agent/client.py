"""FuseIQ Agent SDK — Client implementation."""

import hashlib
import json
import time
import uuid
from typing import Optional

import requests


class FuseIQAgent:
    """Connect an external AI agent to FuseIQ.

    Args:
        api_key: API key from fuseiq.io/settings/api-keys
        name: Display name in the FuseIQ dashboard
        agent_id: Optional stable ID for reconnection
        framework: Agent framework name (Custom, CrewAI, LangChain, etc.)
        base_url: FuseIQ API endpoint
    """

    def __init__(
        self,
        api_key: str,
        name: str,
        agent_id: Optional[str] = None,
        framework: str = "Custom",
        base_url: str = "https://fuseiq.io",
    ):
        self.api_key = api_key
        self.name = name
        self.agent_id = agent_id or str(uuid.uuid4())
        self.framework = framework
        self.base_url = base_url.rstrip("/")
        self._session = requests.Session()
        self._session.headers.update({
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "User-Agent": f"fuseiq-agent-sdk/0.1.0",
        })

    def heartbeat(
        self,
        status: str = "online",
        task: str = "",
        metadata: Optional[dict] = None,
    ) -> dict:
        """Send a heartbeat to update agent status in the dashboard.

        Args:
            status: One of "online", "idle", "busy", "offline"
            task: Current task description
            metadata: Additional key-value data

        Returns:
            Response dict with success status and agent_id
        """
        payload = {
            "agent_name": self.name,
            "status": status,
            "framework": self.framework,
            "metadata": {
                "agent_id": self.agent_id,
                "task": task,
                **(metadata or {}),
            },
        }

        for attempt in range(3):
            try:
                resp = self._session.post(
                    f"{self.base_url}/api/external/heartbeat",
                    json=payload,
                    timeout=10,
                )
                if resp.status_code == 429:
                    time.sleep(2 ** attempt)
                    continue
                resp.raise_for_status()
                return resp.json()
            except requests.RequestException as e:
                if attempt == 2:
                    return {"success": False, "error": str(e)}
                time.sleep(2 ** attempt)

        return {"success": False, "error": "Max retries exceeded"}

    def log(self, message: str) -> dict:
        """Send a log message for this agent.

        Args:
            message: Log line text

        Returns:
            Response dict
        """
        payload = {
            "agent_name": self.name,
            "metadata": {
                "agent_id": self.agent_id,
                "log": message,
            },
        }

        try:
            resp = self._session.post(
                f"{self.base_url}/api/external/heartbeat",
                json=payload,
                timeout=10,
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            return {"success": False, "error": str(e)}

    def __repr__(self) -> str:
        return f"<FuseIQAgent '{self.name}' ({self.framework})>"
