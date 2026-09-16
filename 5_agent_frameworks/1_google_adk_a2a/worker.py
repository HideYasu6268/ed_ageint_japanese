"""Day1のワーカーを、単純なサブプロセスとしてボードに対して実行する。

1つのタスク(「notes.txtを読み、スペイン語に翻訳し、spanish.txtに書き出す」)を仕込み、
あとはADKのエージェントループに作業させる。ボードを読み、filesystem MCPサーバー経由で
ファイルを読み、翻訳し、スペイン語の結果を書き戻し、タスクを完了にする。これはDay5で
ワーカーが動く仕組みと全く同じで、タスクが1つだけという点が違うだけである。

    uv run worker.py              # 新しいタスクを仕込んでエージェントを実行する
    uv run worker.py --seed-only  # 仕込みだけ行い、`adk web` から動かす
"""

from __future__ import annotations

import argparse
import asyncio

from quiet import silence

silence()

import board  # noqa: E402
from google.adk.runners import InMemoryRunner  # noqa: E402
from task_worker.agent import WORKSPACE, root_agent  # noqa: E402

TASK = "Read notes.txt, translate its contents into natural Spanish, and write the Spanish to spanish.txt."


def seed() -> int:
    """ボードをリセットし、notes.txtを配置し、1つのゴールを追加する。"""
    board.reset_board()
    WORKSPACE.mkdir(exist_ok=True)
    (WORKSPACE / "spanish.txt").unlink(missing_ok=True)
    return board.add_goal(TASK)


async def run() -> None:
    runner = InMemoryRunner(agent=root_agent)
    await runner.run_debug("Please work the pending task on the board.", verbose=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Day 1 ADK board worker.")
    parser.add_argument(
        "--seed-only",
        action="store_true",
        help="Seed a fresh task without running the agent (for the adk web demo).",
    )
    args = parser.parse_args()

    goal_id = seed()
    print(f"Seeded goal {goal_id}: {TASK}\n")
    if args.seed_only:
        print("Board is ready. Run `uv run adk web` and ask the worker to work the board.")
        return

    board.claim_todo(goal_id)  # ワーカーがゴールを取り込む: pending -> in_progress
    asyncio.run(run())

    print("\nBoard after the run:")
    board.show_board()

    spanish = WORKSPACE / "spanish.txt"
    if spanish.exists():
        print("\nspanish.txt:\n" + spanish.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
