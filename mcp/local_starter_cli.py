"""
Interactive CLI for dbt-mcp with Pydantic AI
Simple command-line interface to ask questions about your dbt project
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.mcp import MCPServerStreamableHTTP
from pydantic_ai.messages import FunctionToolCallEvent
import httpx

BASE_DIR = Path(__file__).parent.parent

async def test_mcp_connection(url: str, headers: dict) -> bool:
    """Test if the MCP server is accessible"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=10.0)
            print(f"✓ Server connection test: {response.status_code}")
            return response.status_code < 500
    except Exception as e:
        print(f"✗ Connection test failed: {e}")
        return False

async def main():
    """Start a conversation using PydanticAI with an HTTP MCP server."""
    
    # Load environment variables with verification
    env_loaded = load_dotenv(BASE_DIR / ".env", override=True)
    starter_loaded = load_dotenv(BASE_DIR / ".env.starter", override=True)
    
    print(f"Environment files loaded: .env={env_loaded}, .env.starter={starter_loaded}\n")
    
    # Get credentials
    token = os.getenv("DBT_TOKEN")
    prod_environment_id = os.getenv("DBT_PROD_ENV_ID")
    host = os.getenv("DBT_HOST", "cloud.getdbt.com")
    
    # Validate required variables
    if not token:
        print("ERROR: DBT_TOKEN not found in environment")
        print("Please set DBT_TOKEN in your .env file")
        return
    
    if not prod_environment_id:
        print("ERROR: DBT_PROD_ENV_ID not found in environment")
        print("Please set DBT_PROD_ENV_ID in your .env file")
        return
    
    print(f"Configuration:")
    print(f"  Host: {host}")
    print(f"  Prod Env ID: {prod_environment_id}")
    print(f"  Token: {'*' * 20}{token[-4:]}\n")
    
    # Configure MCP server connection
    mcp_server_url = f"https://{host}/api/ai/v1/mcp/"
    mcp_server_headers = {
        "Authorization": f"token {token}",
        "x-dbt-prod-environment-id": prod_environment_id,
    }
    
    # Test connection before proceeding
    print("Testing MCP server connection...")
    if not await test_mcp_connection(mcp_server_url, mcp_server_headers):
        print("\nFailed to connect to MCP server. Please check:")
        print("  1. Your DBT_TOKEN is valid")
        print("  2. Your DBT_PROD_ENV_ID is correct")
        print("  3. Your network allows access to", host)
        return
    
    print("\nInitializing agent...")
    server = MCPServerStreamableHTTP(url=mcp_server_url, headers=mcp_server_headers)
    
    # Use a valid OpenAI model
    agent = Agent(
        "openai:gpt-4o",  # Changed from gpt-5 which doesn't exist
        toolsets=[server],
        system_prompt="You are a helpful AI assistant with access to MCP tools for dbt.",
    )
    
    print("\n" + "="*60)
    print("Starting conversation with PydanticAI + MCP server...")
    print("Type 'quit' to exit")
    print("="*60 + "\n")
    
    try:
        async with agent:
            while True:
                try:
                    user_input = input("You: ").strip()
                    
                    if user_input.lower() in ["quit", "exit", "q"]:
                        print("Goodbye!")
                        break
                    
                    if not user_input:
                        continue
                    
                    # Event handler for real-time tool call detection
                    async def event_handler(ctx: RunContext, event_stream):
                        async for event in event_stream:
                            if isinstance(event, FunctionToolCallEvent):
                                print(f"\n🔧 Tool called: {event.part.tool_name}")
                                print(f"   Arguments: {event.part.args}")
                                print("Assistant: ", end="", flush=True)
                    
                    # Stream the response with real-time events
                    print("Assistant: ", end="", flush=True)
                    async with agent.run_stream(
                        user_input, event_stream_handler=event_handler
                    ) as result:
                        async for text in result.stream_text(delta=True):
                            print(text, end="", flush=True)
                    print()  # New line after response
                
                except KeyboardInterrupt:
                    print("\nGoodbye!")
                    break
                except Exception as e:
                    print(f"\nError during conversation: {e}")
                    print("You can continue chatting or type 'quit' to exit.\n")
    
    except Exception as e:
        print(f"\nFailed to initialize agent: {e}")
        print("\nPossible causes:")
        print("  1. Invalid credentials")
        print("  2. MCP server is not responding")
        print("  3. Network connectivity issues")

if __name__ == "__main__":
    asyncio.run(main())