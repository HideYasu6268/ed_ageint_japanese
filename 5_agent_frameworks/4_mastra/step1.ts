/**
 * Step1: エージェントを作成する。
 *
 * Mastraでは、エージェントはAgentであり、名前、instructions(システムプロンプト)、
 * モデルを持つ。モデルはルーティング用の文字列 "openai/gpt-5.4-mini" で、Vercel AI SDK
 * によって解決され、OpenAIを選び、環境変数からOPENAI_API_KEYを読み取る。まだ何も
 * 実行されず、ここでは組み立てるだけである。実行するには: npm run step1
 */

import "./env.ts";
import { Agent } from "@mastra/core/agent";

const agent = new Agent({
  id: "assistant",
  name: "Assistant",
  instructions: "You are a concise, friendly assistant. Reply in a single short sentence.",
  model: "openai/gpt-5.4-mini",
});

console.log(`Created agent: ${agent.name}`);
