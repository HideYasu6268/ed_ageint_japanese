/**
 * 小さなSQLite製のtodoボード。Week5の各ワーカーが共有する基盤。
 *
 * これはDay1〜3のPython版board.pyに対応するTypeScript版である。MastraはPythonを
 * importできないため、この日は自前のboard.tsを持っている。どちらも同じ種類の単一の
 * SQLiteファイルを、同じ1つのテーブルで開くので、こちら側のゴールはあちら側のゴールと
 * 同じものになる。ワーカーには1つのゴールが与えられる。そこに到達するため、ワーカーは
 * そのゴールの下に自分でステップのtodoを書き込み、終わったものから順にチェックを入れ、
 * すべてのステップが終わったらゴール自体を完了にする。WALモードとbusy timeoutの組み合わせ
 * により、複数のエージェントが互いを妨げることなく同時に読み書きできる。また、SQLiteは
 * MacとWindowsで同じように動く。
 *
 * NodeはSQLiteを標準ライブラリにnode:sqliteとして同梱しているため、追加のインストールは
 * 不要である。
 */

import { DatabaseSync } from "node:sqlite";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

export const BOARD_PATH =
  process.env.BOARD_PATH ?? join(dirname(fileURLToPath(import.meta.url)), "board.sqlite");

export interface Todo {
  id: number;
  parent_id: number | null;
  task: string;
  status: string;
  result: string;
}

function connect(path = BOARD_PATH): DatabaseSync {
  const db = new DatabaseSync(path);
  db.exec("PRAGMA journal_mode=WAL");
  db.exec("PRAGMA busy_timeout=5000");
  return db;
}

/** 既存の内容を破棄して、新しい空のボードを作成する。 */
export function resetBoard(path = BOARD_PATH): void {
  const db = connect(path);
  db.exec("DROP TABLE IF EXISTS todos");
  db.exec(`CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id INTEGER,
    task TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    result TEXT NOT NULL DEFAULT ''
  )`);
  db.close();
}

/** トップレベルのゴールをボードに追加し、そのidを返す。 */
export function addGoal(task: string, path = BOARD_PATH): number {
  const db = connect(path);
  const id = db.prepare("INSERT INTO todos (task) VALUES (?)").run(task).lastInsertRowid;
  db.close();
  return Number(id);
}

/** ゴールの下にステップを追加し、そのidを返す。 */
export function addStep(goalId: number, task: string, path = BOARD_PATH): number {
  const db = connect(path);
  const id = db.prepare("INSERT INTO todos (parent_id, task) VALUES (?, ?)").run(goalId, task).lastInsertRowid;
  db.close();
  return Number(id);
}

/** ボード上のすべてのtodo(ゴールとステップ)を、古い順に返す。 */
export function listTodos(path = BOARD_PATH): Todo[] {
  const db = connect(path);
  const rows = db.prepare("SELECT id, parent_id, task, status, result FROM todos ORDER BY id").all();
  db.close();
  return rows as unknown as Todo[]; // node:sqliteはrowsの型をunknownとしているので、このキャストは正直な最小限のもの
}

/** todoを進行中としてマークし、ワーカーがそれに取り組み始めたことを示せるようにする。 */
export function claimTodo(taskId: number, path = BOARD_PATH): void {
  const db = connect(path);
  db.prepare("UPDATE todos SET status = 'in_progress' WHERE id = ?").run(taskId);
  db.close();
}

/** todoを完了としてマークし、その結果を記録する。 */
export function completeTodo(taskId: number, result: string, path = BOARD_PATH): void {
  const db = connect(path);
  db.prepare("UPDATE todos SET status = 'done', result = ? WHERE id = ?").run(result, taskId);
  db.close();
}

const RESET = "\x1b[0m";
const GREEN = "\x1b[32m";
const YELLOW = "\x1b[33m";
const DIM = "\x1b[2m";
const STRIKE = "\x1b[9m";

/**
 * 人間向けにボードを表示する。各ゴールの下にステップをインデントして並べ、完了した
 * todoは緑色の取り消し線、進行中のものは黄色で表示する。これは見た目を整えるためだけの
 * ものであり、エージェントのshow_todosツールは変わらずプレーンなオブジェクトを受け取る。
 */
export function showBoard(path = BOARD_PATH): void {
  const todos = listTodos(path);
  for (const goal of todos.filter((t) => t.parent_id === null)) {
    console.log(formatLine(goal, "Goal", ""));
    for (const step of todos.filter((t) => t.parent_id === goal.id)) {
      console.log(formatLine(step, "Step", "  "));
    }
  }
}

function formatLine(todo: Todo, kind: string, indent: string): string {
  const label = `${indent}${kind} #${todo.id}: ${todo.task}`;
  if (todo.status === "done") {
    const result = todo.result ? `  ${DIM}${todo.result}${RESET}` : "";
    return `${GREEN}${STRIKE}${label}${RESET}${result}`;
  }
  if (todo.status === "in_progress") return `${YELLOW}${label}${RESET}`;
  return label;
}
