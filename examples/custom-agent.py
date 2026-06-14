"""Custom Agent — Full-featured agent with task loop."""

import os
import time
import json
from datetime import datetime
from fuseiq_agent import FuseIQAgent

class MyCustomAgent:
    """A custom AI agent that reports to FuseIQ."""

    def __init__(self, api_key: str, name: str = "Custom Analyst"):
        self.fuseiq = FuseIQAgent(api_key=api_key, name=name, framework="Custom")
        self.task_count = 0

    def run_analysis(self, data_path: str):
        """Analyze a JSON data file and report progress."""
        self.fuseiq.heartbeat("online", task=f"Starting analysis of {data_path}")

        # Load data
        with open(data_path) as f:
            data = json.load(f)

        results = []
        for i, item in enumerate(data):
            self.task_count += 1
            self.fuseiq.heartbeat("busy", task=f"Processing item {i + 1}/{len(data)}")

            # Simulate analysis
            result = self._analyze_item(item)
            results.append(result)

            self.fuseiq.log(f"Item {i + 1}: {result['summary']}")
            time.sleep(0.5)

        self.fuseiq.heartbeat("idle", task=f"Completed {len(results)} items")
        return results

    def _analyze_item(self, item: dict) -> dict:
        return {
            "id": item.get("id"),
            "summary": f"Analysis complete for {item.get('name', 'unknown')}",
            "timestamp": datetime.now().isoformat(),
        }

if __name__ == "__main__":
    api_key = os.environ.get("FUSEIQ_API_KEY")
    if not api_key:
        print("Set FUSEIQ_API_KEY environment variable")
        exit(1)

    agent = MyCustomAgent(api_key)
    print("🤖 Custom agent running. View at https://fuseiq.io/dashboard")

    # Run with sample data
    import tempfile
    sample = [{"id": 1, "name": "Q1 Report"}, {"id": 2, "name": "Q2 Forecast"}]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(sample, f)
        temp_path = f.name

    results = agent.run_analysis(temp_path)
    print(f"✅ Done. {len(results)} items processed.")
