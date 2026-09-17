/**
 * Step2: 実行する。
 *
 * メッセージを送り、返信を待ち、結果の.textを表示する。まだツールがないのでループする
 * ものがなく、エージェントはただ答えるだけである。これはまだ単なるLLM呼び出しである。
 * 実行するには: npm run step2
 */

import "./env.ts";
import { Agent } from "@mastra/core/agent";
import { gemini } from "./gemini.ts";

const agent = new Agent({
  id: "assistant",
  name: "Assistant",
  instructions: "You are a concise, friendly assistant. Reply in a single short sentence.",
  model: gemini("gemini-flash-latest"),
});

const reply = await agent.generate("Say hello in Spanish.");
console.log(reply.text);

process.exit(0); // Mastraはモデルの接続プールを開いたままにするので、作業が終わったら明示的に終了する
