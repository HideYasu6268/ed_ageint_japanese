/**
 * Step1: エージェントを作成する。
 *
 * Mastraでは、エージェントはAgentであり、名前、instructions(システムプロンプト)、
 * モデルを持つ。モデルはGeminiのOpenAI互換エンドポイントを指すプロバイダー(./gemini.ts)
 * から作られ、環境変数からGOOGLE_API_KEYを読み取る。まだ何も
 * 実行されず、ここでは組み立てるだけである。実行するには: npm run step1
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

console.log(`Created agent: ${agent.name}`);
