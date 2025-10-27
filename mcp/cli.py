"""
Interactive CLI for dbt-mcp with Pydantic AI
Simple command-line interface to ask questions about your dbt project
"""

import asyncio
from pathlib import Path
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio

# Load env from data/.env (optional but handy if you also run dbt-mcp outside)
ENV_FILE = Path(__file__).parent.parent / ".env"
load_dotenv(ENV_FILE)

async def main() -> None:
    print("\n" + "=" * 70)
    print("🔧 dbt Assistant - Interactive CLI")
    print("=" * 70)
    print("Initializing...")

    # Local dbt MCP server over stdio
    dbt_server = MCPServerStdio(
        command="/Users/shaunhide/projects/data/.venv/bin/dbt-mcp",
        args=[],
        env={
            "DBT_PROJECT_DIR": "/Users/shaunhide/projects/data/transforms",
            "DBT_PROFILES_DIR": "/Users/shaunhide/projects/data/transforms/profiles",
            "DBT_PATH": "/Users/shaunhide/projects/data/.venv/bin/dbt",
            "DISABLE_SEMANTIC_LAYER": "true",
            "DISABLE_DISCOVERY": "true",
            "DISABLE_SQL": "true",
            "DISABLE_ADMIN_API": "true",
        },
        timeout=30,
    )

    agent = Agent(
        model="openai:gpt-4o-mini",
        toolsets=[dbt_server],  # <- replaces mcp_servers
        instructions=(
            "You are a helpful dbt assistant. "
            "Provide clear, concise answers about the dbt project. "
            "When listing items, be organized and easy to read."
        ),
    )

    # If you want the same sampling model applied to all MCP servers (optional):
    # agent.set_mcp_sampling_model()  # defaults to the agent's model

    print("✓ Ready!\n")

    # Start/stop MCP servers with the agent context (replaces run_mcp_servers)
    async with agent:
        print("Ask questions about your dbt project (type 'exit' to quit)")
        print("Example: 'List all models in my project'\n")

        while True:
            try:
                query = input("You: ").strip()
                if query.lower() in {"exit", "quit", "q"}:
                    print("\n👋 Goodbye!")
                    break
                if not query:
                    continue

                print("\n🤖 Assistant: ", end="", flush=True)
                result = await agent.run(query)
                print(result.output)  # <- use .output for plain-text results
                print()

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    asyncio.run(main())
