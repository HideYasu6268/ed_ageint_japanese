/**
 * Step3: ツールを追加する。
 *
 * まずは今週のプロジェクトの土台となる、小さなSQLite製のtodoボードから。これはNode
 * 組み込みのnode:sqliteを使った、Day1〜3のboard.pyに対応するTypeScript版である。実体は
 * board.tsにあるので、開いて読んでみるとよい。ワーカーには1つのゴールが与えられ、そこに
 * 到達するために自分でそのゴールの下にステップのtodoを書き込み、それぞれをチェックして
 * いき、ゴールを閉じる。
 *
 * Mastraにおけるツールとは、id、description、zodの入力スキーマ、非同期のexecuteを持つ
 * createToolである。3つのボードツール(show_todos、plan_steps、complete_task)は
 * tools.tsにある。ここではエージェントにボードツールを与え、ボード上に何があるかを尋ねる。
 * 答える前に自分の判断でshow_todosを呼び出す様子を見てほしい。実行するには: npm run step3
 */

import "./env.ts";
import { Agent } from "@mastra/core/agent";
import { gemini } from "./gemini.ts";
import { showTodos, completeTask } from "./tools.ts";
import { resetBoard, addGoal, showBoard } from "./board.ts";

resetBoard();
addGoal("Read notes.txt, translate its contents into natural Spanish, and write the Spanish to spanish.txt.");

const boardAgent = new Agent({
  id: "board-agent",
  name: "Board Agent",
  instructions: "You help manage a shared todo board.",
  model: gemini("gemini-flash-latest"),
  tools: { showTodos, completeTask },
});

const reply = await boardAgent.generate("What is on the board right now, and what is its status?");
console.log(reply.text);

console.log("\nThe board:");
showBoard();

process.exit(0); // Mastraはモデルの接続プールを開いたままにするので、作業が終わったら明示的に終了する
