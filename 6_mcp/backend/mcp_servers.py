import os
from pathlib import Path
from dotenv import load_dotenv
from agents.mcp import MCPServerStdio, create_static_tool_filter
from .market import massive_api_key

load_dotenv(override=True)

PROJECT_DIR = str(Path(__file__).resolve().parent.parent)
tavily_env = {"TAVILY_API_KEY": os.getenv("TAVILY_API_KEY")}
TIMEOUT = 120

# トレーダー用の市場データサーバー。
# キーがある場合は、Massive 自身の市場データサーバーをローカルで stdio 経由で実行し、エージェントに渡す。
# キーがない場合は、シミュレートされた価格を提供する自前の市場サーバーを使う。
if massive_api_key:
    market_params = {
        "command": "uvx",
        "args": [
            "--with", "mcp<2",
            "--from", "git+https://github.com/massive-com/mcp_massive@v0.10.0",
            "mcp_massive"
        ],
        "env": {"MASSIVE_API_KEY": massive_api_key},
    }
else:
    market_params = {
        "command": "uv",
        "args": ["run", "-m", "backend.market_server"],
        "cwd": PROJECT_DIR
    }

def trader_mcp_servers() -> list[MCPServerStdio]:
    """トレーダーが使う MCP サーバー群: 自前のアカウントサーバー、プッシュ通知、市場データ。"""
    params = [
        {"command": "uv", "args": ["run", "-m", "backend.accounts_server"], "cwd": PROJECT_DIR},
        {"command": "uv", "args": ["run", "-m", "backend.push_server"], "cwd": PROJECT_DIR},
        market_params,
    ]
    return [MCPServerStdio(p, client_session_timeout_seconds=TIMEOUT) for p in params]


def researcher_mcp_servers(name: str) -> list[MCPServerStdio]:
    """リサーチャーが使う MCP サーバー群: Fetch、Tavily のウェブ検索、Memory。

    Tavily のサーバーは複数のツールを提供しているが、リサーチャーが重いクロールや
    ディープリサーチ系のツールではなく、シンプルな検索を使うように、ウェブ検索のみに制限する。
    """
    fetch = MCPServerStdio(
        {"command": "uvx", "args": ["--with", "mcp<2","mcp-server-fetch"]},
        client_session_timeout_seconds=TIMEOUT,
    )
    search = MCPServerStdio(
        {"command": "npx", "args": ["-y", "tavily-mcp@latest"], "env": tavily_env},
        client_session_timeout_seconds=TIMEOUT,
        tool_filter=create_static_tool_filter(allowed_tool_names=["tavily_search"]),
    )
    memory = MCPServerStdio(
        {
            "command": "npx",
            "args": ["-y", "mcp-memory-libsql"],
            "env": {"LIBSQL_URL": f"file:./memory/{name}.db"},
        },
        client_session_timeout_seconds=TIMEOUT,
    )
    return [fetch, search, memory]
    
