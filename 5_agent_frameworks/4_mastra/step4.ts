/**
 * Step4: MCPを追加する。
 *
 * MCPは単に、もう少し多くのツールにすぎない。自分では書いていないが、小さなプロトコル
 * 経由でつながっているツール群である。ここではエージェントにfilesystemのリファレンス
 * サーバーを与える。これは今週すべてのフレームワークが使う同じNode製のサーバーで、
 * 単一のworkspaceフォルダに限定されている。MastraにおけるMCPサーバーはMCPClientであり、
 * await mcp.listTools()でそのツールを取り出し、エージェントに渡す。tools.tsの
 * makeFilesystemはサーバーにstderr "ignore"とcwdを設定しており、これはMastraが
 * バナーやパスの細かい問題をきれいに処理するやり方である。実行するには: npm run step4
 */

import "./env.ts";
import { Agent } from "@mastra/core/agent";
import { gemini } from "./gemini.ts";
import { makeFilesystem } from "./tools.ts";

const filesystem = makeFilesystem();

const fileAgent = new Agent({
  id: "file-agent",
  name: "File Agent",
  instructions: "You can read and write files in your workspace. Use your tools to do what is asked.",
  model: gemini("gemini-flash-latest"),
  tools: await filesystem.listTools(),
});

const reply = await fileAgent.generate("Read notes.txt and summarize it in one short sentence.");
console.log(reply.text);

await filesystem.disconnect();

process.exit(0); // Mastraはモデルの接続プールを開いたままにするので、作業が終わったら明示的に終了する
