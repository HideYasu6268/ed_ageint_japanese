/**
 * Step5: ゴールを与えてループの中に置く。
 *
 * ここまでの成果を活かす番である。1つのエージェントに3つのボードツールすべてと
 * filesystemサーバーを与え、ゴールを渡して実行させる。エージェントはボード上に自分で
 * ステップを計画し、ファイルツールで作業し、1つずつチェックしていき、作業が終わったら
 * ゴールを閉じる。これこそが、自律的に動くエージェントループそのものである。読む、
 * 計画する、行動する、チェックする、繰り返す。実行するには: npm run step5
 *
 * Day5が起動するターミナルワーカーは、このファイルの隣にあるworker.tsである。同じ
 * エージェントに、プロジェクトが必要とする要素(共有ボード上の1タスクを取り込む、
 * WORKER_MODELでモデルを切り替える、各ツール呼び出しを表示する)を加えたものである。
 */

import "./env.ts";
import { join } from "node:path";
import { mkdirSync, rmSync, existsSync, readFileSync } from "node:fs";
import { Agent } from "@mastra/core/agent";
import { gemini } from "./gemini.ts";
import { boardTools, makeFilesystem, WORKSPACE } from "./tools.ts";
import { resetBoard, addGoal, claimTodo, showBoard } from "./board.ts";

const GOAL = "Read notes.txt, translate its contents into natural Spanish, and write the Spanish to spanish.txt.";

const INSTRUCTIONS = `
You are a careful worker with a shared todo board and a set of file tools.

Take the pending goal and see it through. Begin by laying out a short plan: the handful of concrete steps the work itself breaks down into, added to the board under the goal. Then carry them out with your file tools, marking each step done as you finish it. Once the steps are all done, close the goal. Your files live in the single folder your tools are allowed to use.
`;

// ボードに1つのゴールを仕込み、古い出力があれば消す。
mkdirSync(WORKSPACE, { recursive: true });
rmSync(join(WORKSPACE, "spanish.txt"), { force: true });
resetBoard();
const goalId = addGoal(GOAL);
claimTodo(goalId); // ワーカーがゴールを取り込む: pending -> in_progress
console.log(`Seeded goal ${goalId}: ${GOAL}\n`);


const filesystem = makeFilesystem();
const worker = new Agent({
  id: "worker",
  name: "Worker",
  instructions: INSTRUCTIONS,
  model: gemini("gemini-flash-latest"),
  tools: { ...boardTools, ...(await filesystem.listTools()) },
});

await worker.generate("Please work the pending goal on the board.", { maxSteps: 25 });
await filesystem.disconnect();

console.log("\nBoard after the run:");
showBoard();
const spanish = join(WORKSPACE, "spanish.txt");
if (existsSync(spanish)) {
  console.log("\nspanish.txt:\n" + readFileSync(spanish, "utf-8"));
}

process.exit(0); // Mastraはモデルの接続プールを開いたままにするので、作業が終わったら明示的に終了する
