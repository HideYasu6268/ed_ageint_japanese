"""Sidekick用のツール群: MCPサーバー、既製のLangChainツール、そして自作ツールの組み合わせ。"""

import asyncio
import os
from contextlib import AsyncExitStack

import requests
import wikipedia
from dotenv import load_dotenv
from langchain_community.tools import GoogleSerperRun, WikipediaQueryRun
from langchain_community.utilities import GoogleSerperAPIWrapper, WikipediaAPIWrapper
from langchain_core.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools

load_dotenv(override=True)

# WikimediaはwikipediaライブラリのデフォルトのUser-Agentを拒否するため、正しく自分自身を名乗る
wikipedia.set_user_agent("agentic-track-course (https://edwarddonner.com)")

search = GoogleSerperRun(api_wrapper=GoogleSerperAPIWrapper())

wikipedia_lookup = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())


@tool
def send_push_notification(text: str) -> str:
    """Send a short push notification to the user's phone."""
    response = requests.post(
        "https://api.pushover.net/1/messages.json",
        data={"token": os.getenv("PUSHOVER_TOKEN"), "user": os.getenv("PUSHOVER_USER"), "message": text},
    )
    response.raise_for_status()
    return "Notification sent"


@tool
def request_human_help(instructions: str) -> str:
    """Ask the user to do something in the browser window that you cannot do yourself,
    such as logging in to a site, passing a captcha, or approving two-factor authentication.
    Explain exactly what you need them to do. The run pauses until they have done it."""
    return "The user says it is done. Continue with the task."


def mcp_connections(sandbox: str) -> dict:
    """Sidekickが使用するMCPサーバー: 画面付き(headed)のブラウザとサンドボックスファイルシステム。"""
    return {
        "playwright": {
            "transport": "stdio",
            "command": "npx",
            "args": ["@playwright/mcp@latest", "--isolated"],
        },
        "filesystem": {
            "transport": "stdio",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", sandbox],
        },
    }


class McpSessions:
    """MCPセッションを永続的に開いたままにし、ツール呼び出しの間もブラウザが状態を
    保持できるようにする。

    stdioトランスポートは同じasyncioタスクから開いて閉じなければならないため、
    1つのバックグラウンドタスクがセッションを保有する: それを開き、待機し、
    stop()が呼ばれたら後片付けをする。停止するとサーバーがシャットダウンし、
    ブラウザが閉じるのが見える。
    """

    def __init__(self, connections: dict):
        self.connections = connections
        self.tools = []
        self._ready = asyncio.Event()
        self._stop = asyncio.Event()
        self._task = None

    async def _run(self):
        client = MultiServerMCPClient(self.connections)
        async with AsyncExitStack() as stack:
            for name in self.connections:
                session = await stack.enter_async_context(client.session(name))
                self.tools += await load_mcp_tools(session, server_name=name)
            self._ready.set()
            await self._stop.wait()

    async def start(self) -> list:
        self._task = asyncio.create_task(self._run())
        ready = asyncio.create_task(self._ready.wait())
        await asyncio.wait([ready, self._task], return_when=asyncio.FIRST_COMPLETED)
        ready.cancel()
        if self._task.done():
            self._task.result()  # サーバーの起動に失敗した場合、本来のエラーを発生させる
        return self.tools

    def stop(self):
        self._stop.set()


async def get_all_tools(sandbox: str):
    """完全なツールリスト(自作ツールとMCPサーバーのツール)とセッションホルダーを返す。"""
    sessions = McpSessions(mcp_connections(sandbox))
    mcp_tools = await sessions.start()
    our_tools = [search, send_push_notification, wikipedia_lookup, request_human_help]
    return our_tools + mcp_tools, sessions
