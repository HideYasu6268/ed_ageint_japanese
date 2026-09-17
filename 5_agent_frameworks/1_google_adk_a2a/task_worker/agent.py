"""Day1のワーカーエージェント。SQLiteボードを使って作業する単一のLlmAgent。

同じエージェントを3つの方法で動かせる。`adk web` でビジュアルに、`adk run` でターミナルから、
または worker.py から単純なサブプロセスとして起動する。ボードツールがタスクを与え、
filesystem MCPサーバーがファイルを与え、あとはエージェントループが残りをこなす。
Day2〜4では、この同じ契約を別のフレームワークで作り直す。
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from quiet import silence

silence()

from dotenv import load_dotenv  # noqa: E402

import board  # noqa: E402

from google.adk.agents import LlmAgent  # noqa: E402
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams  # noqa: E402
from mcp import StdioServerParameters  # noqa: E402

load_dotenv(override=True)
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "FALSE")

MODEL = "gemini-flash-latest"
WORKSPACE = Path(__file__).resolve().parent / "workspace"
WORKSPACE.mkdir(exist_ok=True)


def show_todos() -> list[dict]:
    """List every todo on the board. A goal has parent_id None; a step has parent_id set to its goal's id."""
    return board.list_todos()


def plan_steps(goal_id: int, steps: list[str]) -> dict:
    """Break a goal into an ordered checklist of steps on the board. Pass the goal's id and a short list of step descriptions."""
    step_ids = [board.add_step(goal_id, step) for step in steps]
    return {"goal_id": goal_id, "step_ids": step_ids}


def complete_task(task_id: int, result: str) -> dict:
    """Mark a todo (a step or the goal) with this id as done and record a short result summary."""
    board.complete_todo(task_id, result)
    return {"task_id": task_id, "status": "done"}


# filesystem MCPサーバーはnpx経由で動作し、workspaceフォルダに限定されているため、
# エージェントはその中のファイルにしか触れられない。これは今週の各フレームワークで
# 同じように接続されている、同じサーバーである。
filesystem = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", str(WORKSPACE)],
            cwd=str(WORKSPACE),  # workspace内でサーバーを起動し、相対ファイル名がそこで解決されるようにする
        ),
        timeout=60
    ),
    # サーバーのstderrをDEVNULLに送る。これによって起動時のログ出力が静かになり、また
    # Windows上でJupyterカーネルからこのサーバーを起動できるようにもなる。Windowsでは
    # カーネルのstderrに実体のあるファイルディスクリプタが存在しないためである。
    errlog=subprocess.DEVNULL,
)

INSTRUCTIONS = """
You are a careful worker with a shared todo board and a set of file tools.

Take the pending goal and see it through. Begin by laying out a short plan: the handful of concrete steps the work itself breaks down into, added to the board under the goal. Then carry them out with your file tools, marking each step done as you finish it. Once the steps are all done, close the goal. Your files live in the single folder your tools are allowed to use.
"""

root_agent = LlmAgent(
    model=MODEL,
    name="task_worker",
    description="Works one goal from the SQLite board using its files.",
    instruction=INSTRUCTIONS,
    tools=[show_todos, plan_steps, complete_task, filesystem],
)
