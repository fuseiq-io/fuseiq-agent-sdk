"""LangChain Agent with FuseIQ Heartbeat — Governed Agent Example.

Run:
    export FUSEIQ_API_KEY="fk_live_your_key"
    export OPENAI_API_KEY="sk-your-key"
    python langchain_agent.py

Requirements:
    pip install fuseiq-agent langchain langchain-openai
"""

import os
import time
from fuseiq_agent import FuseIQAgent

# ── LangChain imports ──────────────────────────────────────────
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


# ════════════════════════════════════════════════════════════════
# 1. Connect to FuseIQ (appears live in dashboard)
# ════════════════════════════════════════════════════════════════

fuseiq = FuseIQAgent(
    api_key=os.environ["FUSEIQ_API_KEY"],
    name="LangChain Governor",
    framework="LangChain",
)

# ════════════════════════════════════════════════════════════════
# 2. Define Tools (each tool reports to FuseIQ)
# ════════════════════════════════════════════════════════════════

@tool
def search_knowledge(query: str) -> str:
    """Search the knowledge base for relevant information."""
    fuseiq.log(f"🔍 Searching: {query}")
    # Simulated search
    time.sleep(0.3)
    return f"Knowledge base result for '{query}': Found 3 relevant documents."

@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression."""
    fuseiq.log(f"🧮 Calculating: {expression}")
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {e}"

@tool
def fetch_weather(city: str) -> str:
    """Get current weather for a city."""
    fuseiq.log(f"🌤 Fetching weather for: {city}")
    time.sleep(0.2)
    return f"Weather in {city}: 22°C, partly cloudy."


# ════════════════════════════════════════════════════════════════
# 3. Build LangChain Agent
# ════════════════════════════════════════════════════════════════

tools = [search_knowledge, calculate, fetch_weather]

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    openai_api_key=os.environ.get("OPENAI_API_KEY"),
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant with access to tools. "
               "Use tools when needed, then give a concise final answer."),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_openai_functions_agent(llm, tools, prompt)
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True,
)


# ════════════════════════════════════════════════════════════════
# 4. Run with FuseIQ heartbeat every step
# ════════════════════════════════════════════════════════════════

fuseiq.heartbeat("online", task="LangChain agent ready")

def governed_invoke(executor: AgentExecutor, user_input: str, heartbeat_every: int = 2):
    """Invoke agent with FuseIQ heartbeat every N intermediate steps.

    This wraps the standard executor.invoke() so the FuseIQ dashboard
    shows real-time progress including tool calls, observations, and
    the final answer.
    """
    step = 0

    # AgentExecutor doesn't expose step-by-step callbacks easily,
    # so we override the tools to count steps.
    original_tools = {t.name: t.func for t in executor.tools}

    for t in executor.tools:
        original = t.func
        def make_wrapped(orig, name):
            def wrapped(*args, **kwargs):
                nonlocal step
                fuseiq.heartbeat("busy", task=f"Tool: {name}")
                result = orig(*args, **kwargs)
                step += 1
                if step % heartbeat_every == 0:
                    fuseiq.log(f"Step {step} complete — tool '{name}' returned: {str(result)[:100]}")
                return result
            return wrapped
        t.func = make_wrapped(original, t.name)

    fuseiq.log(f"User input: {user_input[:200]}")
    result = executor.invoke({"input": user_input})

    # Restore original tool functions
    for t, orig_name in zip(executor.tools, original_tools):
        t.func = original_tools[orig_name]

    fuseiq.heartbeat("idle", task="Finished")
    fuseiq.log(f"Final output: {result['output'][:200]}")
    return result


# ════════════════════════════════════════════════════════════════
# 5. Demo
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🤖 LangChain Governor starting...")
    print("   View live at: https://fuseiq.io/dashboard\n")

    queries = [
        "What's the weather in Tokyo? Also calculate 15 * 7 + 3.",
        "Search for 'quantum computing basics' and then tell me what you found.",
    ]

    for q in queries:
        print(f"\n📥 User: {q}")
        result = governed_invoke(executor, q, heartbeat_every=1)
        print(f"📤 Agent: {result['output']}\n")
        time.sleep(1)

    print("✅ All queries complete. Check your FuseIQ dashboard!")
