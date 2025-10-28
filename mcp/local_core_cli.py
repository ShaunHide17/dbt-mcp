"""
Interactive CLI for dbt-mcp with Pydantic AI
Simple command-line interface to ask questions about your dbt project
"""

# Troubleshooting: Uncomment to see the environment variables
# for key in sorted(os.environ.keys()):
#     value = os.environ[key]
#     # Optionally mask sensitive values
#     if any(sensitive in key.upper() for sensitive in ['PASSWORD', 'SECRET', 'KEY', 'TOKEN']):
#         value = '***REDACTED***'
#     print(f"{key}={value}")

import asyncio
from pathlib import Path
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
import os

# Load the base environment variables
BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env", override=True)
load_dotenv(BASE_DIR / ".env.core", override=True)

async def main() -> None:
    print("\n" + "=" * 70)
    print("🔧 dbt Assistant - Interactive CLI")
    print("=" * 70)
    print("Initializing...")

    # Local dbt MCP server over stdio
    dbt_server = MCPServerStdio(
        command=os.getenv("DBT_MCP_BIN"),
        args=[],
        env={
            **os.environ,
        },
        timeout=30,
    )

    # Create the agent
    agent = Agent(
        model=os.getenv("OPENAI_MODEL"),
        toolsets=[dbt_server], 
        instructions=(
            "You are a helpful dbt assistant. "
            "Provide clear, concise answers about the dbt project. "
            "When listing items, be organized and easy to read."
        ),
    )

    print("✓ Ready!\n")

    # Start/stop MCP servers with the agent context
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
                print(result.output)
                print()

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    asyncio.run(main())
