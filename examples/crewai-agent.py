"""CrewAI Integration — Wrap a CrewAI agent with FuseIQ.

Install: pip install fuseiq-agent crewai
Run:     export FUSEIQ_API_KEY="fk_live_..." && python crewai-agent.py
"""

import os
from fuseiq_agent import FuseIQAgent

# Connect to FuseIQ dashboard
agent = FuseIQAgent(
    api_key=os.environ["FUSEIQ_API_KEY"],
    name="CrewAI Researcher",
    framework="CrewAI",
)

# Send heartbeat when agent starts
agent.heartbeat("online", task="CrewAI agent initialized")

try:
    from crewai import Agent, Task, Crew

    researcher = Agent(
        role="Senior Researcher",
        goal="Find trending AI topics",
        backstory="Expert in AI trends",
    )

    task = Task(
        description="Research top 3 AI trends for Q3",
        agent=researcher,
    )

    crew = Crew(
        agents=[researcher],
        tasks=[task],
        verbose=True,
    )

    agent.heartbeat("busy", task="Running CrewAI research...")
    result = crew.kickoff()
    agent.heartbeat("idle", task="Research complete")

    print("✅ CrewAI agent finished. Result:", result)

except ImportError:
    agent.heartbeat("offline", task="CrewAI not installed")
    print("Install CrewAI: pip install crewai")
