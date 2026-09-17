/**
 * メインモデルをOpenAIからGeminiに切り替える。
 *
 * MastraはVercel AI SDK経由でモデルを解決する。ここでは@ai-sdk/openaiの
 * createOpenAI()を使い、baseURLをGeminiのOpenAI互換エンドポイントに向けることで、
 * 新しいnpmパッケージを追加せずにGeminiを呼び出す。
 *
 * 使い方: 各ファイルで `model: "openai/gpt-5.4-mini"` の代わりに
 * `model: gemini("gemini-flash-latest")` を使う。
 */

import "./env.ts";
import { createOpenAI } from "@ai-sdk/openai";

export const gemini = createOpenAI({
  baseURL: "https://generativelanguage.googleapis.com/v1beta/openai/",
  apiKey: process.env.GOOGLE_API_KEY,
});
