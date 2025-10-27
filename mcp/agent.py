import os
import sys
import shutil
from pathlib import Path
from dotenv import load_dotenv

import asyncio
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio

# Load env from ../.env
ENV_FILE = Path(__file__).parent.parent / ".env"
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)

# Environment to forward to dbt-mcp
MCP_ENV_KEYS = [
    "DBT_PROJECT_DIR",
    "DBT_PROFILES_DIR",
    "DBT_PATH",
    "DISABLE_SEMANTIC_LAYER",
    "DISABLE_DISCOVERY",
    "DISABLE_SQL",
    "DISABLE_ADMIN_API",
]
MCP_ENV = {k: v for k, v in ((k, os.getenv(k)) for k in MCP_ENV_KEYS) if v is not None}

MODEL_NAME = os.getenv("OPENAI_MODEL", "openai:gpt-4o-mini")

DBT_MCP_BIN = os.getenv("DBT_MCP_BIN")  # optional absolute path to dbt-mcp

def _build_mcp_stdio() -> MCPServerStdio:
    """
    Prefer launching the dbt-mcp console script if available.
    Fallback to 'python -m dbt_mcp.main' when the console script isn't found.
    This avoids the closed-stdin issues seen when chaining through 'uvx' under Streamlit.
    """
    # 1) Explicit binary set by user
    if DBT_MCP_BIN and Path(DBT_MCP_BIN).exists():
        print(f"[agent] launching dbt-mcp via DBT_MCP_BIN: {DBT_MCP_BIN}")
        return MCPServerStdio(
            command=DBT_MCP_BIN,
            args=[],
            env=MCP_ENV,
            timeout=90,
        )

    # 2) Binary next to this Python (same venv): <venv>/bin/dbt-mcp
    venv_dir = Path(sys.executable).parent
    venv_dbt_mcp = venv_dir / ("dbt-mcp.exe" if os.name == "nt" else "dbt-mcp")
    if venv_dbt_mcp.exists():
        print(f"[agent] launching dbt-mcp via venv binary: {venv_dbt_mcp}")
        return MCPServerStdio(
            command=str(venv_dbt_mcp),
            args=[],
            env=MCP_ENV,
            timeout=90,
        )

    # 3) Binary on PATH
    which_dbt_mcp = shutil.which("dbt-mcp")
    if which_dbt_mcp:
        print(f"[agent] launching dbt-mcp via PATH: {which_dbt_mcp}")
        return MCPServerStdio(
            command=which_dbt_mcp,
            args=[],
            env=MCP_ENV,
            timeout=90,
        )

    # 4) Fallback: module entrypoint
    # NOTE: 'dbt_mcp' has no __main__, so use 'dbt_mcp.main'
    print("[agent] launching dbt-mcp via module: python -m dbt_mcp.main")
    return MCPServerStdio(
        command=sys.executable,
        args=["-m", "dbt_mcp.main"],
        env=MCP_ENV,
        timeout=90,
    )

# ---------- Agent / MCP ----------
def build_agent() -> Agent:
    """Create a fresh Agent wired to a local dbt-mcp via stdio."""
    dbt_server = _build_mcp_stdio()
    return Agent(
        model=MODEL_NAME,
        toolsets=[dbt_server],
        instructions=(
            "You are a helpful dbt assistant. "
            "Provide clear, concise answers about the dbt project. "
            "When listing items, be organized and easy to read."
        ),
    )

def agent_ask(agent: Agent, user_text: str) -> str:
    """Run one question/answer round synchronously for Streamlit."""
    async def _run_once() -> str:
        async with agent:
            res = await agent.run(user_text)
            return res.output
    return asyncio.run(_run_once())
