"""Quickstart — Connect any script to FuseIQ in 3 lines.

Run:
    export FUSEIQ_API_KEY="fk_live_your_key"
    python quickstart.py
"""

import os
import time
from fuseiq_agent import FuseIQAgent

# 1. Create agent (appears live in dashboard)
agent = FuseIQAgent(
    api_key=os.environ["FUSEIQ_API_KEY"],
    name="My First Agent",
)

# 2. Send heartbeat
agent.heartbeat("online", task="Starting up...")

# 3. Simulate work
for i in range(5):
    agent.heartbeat("busy", task=f"Processing batch {i + 1}/5")
    agent.log(f"Completed batch {i + 1}")
    time.sleep(1)

agent.heartbeat("idle", task="All done")
print("✅ Agent finished. View at https://fuseiq.io/dashboard")
