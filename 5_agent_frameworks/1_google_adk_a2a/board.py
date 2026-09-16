"""小さなSQLite製のtodoボード。Week5の各ワーカーが共有する基盤。

ワーカーには1つのゴールが与えられる。そこに到達するため、ワーカーはそのゴールの下に自分で
ステップのtodoを書き込み、終わったものから順にチェックを入れ、すべてのステップが終わったら
ゴール自体を完了にする。Day1〜4ではそれぞれがこの小さなボードを個別に動かし、Day5では同じ
仕組みがチーム全体を協調させる共有ボードへと発展する。ボードはテーブル1つだけの単一ファイルなので
サーバーを必要とせず、MacとWindowsで同じように動く。WALモードとbusy timeoutの組み合わせにより、
複数のエージェントが互いを妨げることなく同時に読み書きできる。
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

from rich.console import Console

BOARD_PATH = Path(os.environ.get("BOARD_PATH", Path(__file__).resolve().parent / "board.sqlite"))


def _connect(path: Path = BOARD_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def reset_board(path: Path = BOARD_PATH) -> None:
    """既存の内容を破棄して、新しい空のボードを作成する。"""
    with _connect(path) as conn:
        conn.execute("DROP TABLE IF EXISTS todos")
        conn.execute(
            """CREATE TABLE todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parent_id INTEGER,
                task TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                result TEXT NOT NULL DEFAULT ''
            )"""
        )


def add_goal(task: str, path: Path = BOARD_PATH) -> int:
    """トップレベルのゴールをボードに追加し、そのidを返す。"""
    with _connect(path) as conn:
        cur = conn.execute("INSERT INTO todos (task) VALUES (?)", (task,))
        return cur.lastrowid


def add_step(goal_id: int, task: str, path: Path = BOARD_PATH) -> int:
    """ゴールの下にステップを追加し、そのidを返す。"""
    with _connect(path) as conn:
        cur = conn.execute(
            "INSERT INTO todos (parent_id, task) VALUES (?, ?)", (goal_id, task)
        )
        return cur.lastrowid


def list_todos(path: Path = BOARD_PATH) -> list[dict]:
    """ボード上のすべてのtodo(ゴールとステップ)を、古い順に返す。"""
    with _connect(path) as conn:
        rows = conn.execute(
            "SELECT id, parent_id, task, status, result FROM todos ORDER BY id"
        ).fetchall()
        return [dict(row) for row in rows]


def claim_todo(task_id: int, path: Path = BOARD_PATH) -> None:
    """todoを進行中としてマークし、ワーカーがそれに取り組み始めたことを示せるようにする。"""
    with _connect(path) as conn:
        conn.execute("UPDATE todos SET status = 'in_progress' WHERE id = ?", (task_id,))


def complete_todo(task_id: int, result: str, path: Path = BOARD_PATH) -> None:
    """todoを完了としてマークし、その結果を記録する。"""
    with _connect(path) as conn:
        conn.execute(
            "UPDATE todos SET status = 'done', result = ? WHERE id = ?",
            (result, task_id),
        )


def show_board(path: Path = BOARD_PATH) -> None:
    """人間向けにボードを表示する。各ゴールの下にステップをインデントして並べ、完了したtodoは
    緑色の取り消し線、進行中のものは黄色で表示する。これは見た目を整えるためだけのものであり、
    エージェントのshow_todosツールは変わらずプレーンなdictを受け取る。
    """
    todos = list_todos(path)
    lines = []
    for goal in [t for t in todos if t["parent_id"] is None]:
        lines.append(_format(goal, "Goal", ""))
        for step in [t for t in todos if t["parent_id"] == goal["id"]]:
            lines.append(_format(step, "Step", "  "))
    if lines:
        # ボード全体を一度に出力する。1行ずつ出力するとJupyterカーネルが行ごとに別のブロックとして
        # 出力してしまい、隙間ができて積み重なってしまう。soft_wrapは長いゴールの行が折り返されるのを防ぐ。
        Console().print("\n".join(lines), soft_wrap=True)


def _format(todo: dict, kind: str, indent: str) -> str:
    label = f"{indent}{kind} #{todo['id']}: {todo['task']}"
    if todo["status"] == "done":
        line = f"[green][strike]{label}[/strike][/green]"
        if todo["result"]:
            line += f"  [dim]{todo['result']}[/dim]"
        return line
    if todo["status"] == "in_progress":
        return f"[yellow]{label}[/yellow]"
    return label
