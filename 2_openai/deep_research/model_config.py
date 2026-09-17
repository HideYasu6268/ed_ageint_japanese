"""
このコースのメインLLMをOpenAIからGeminiに切り替えるための共通設定。

やっていることはシンプルです:
1. GeminiのOpenAI互換エンドポイントを指す AsyncOpenAI クライアントを作る
2. それをOpenAI Agents SDKの OpenAIChatCompletionsModel でラップする
3. 各エージェントファイルはこの MODEL_NAME を import して使うだけでよい

注意: search_agent.py だけは例外です。OpenAI Agents SDKの WebSearchTool は
OpenAIがホストする専用ツールで、Responses API経由でしか動作しません。
Geminiの Chat Completions 互換エンドポイントでは使えないため、
search_agent.py は引き続きOpenAIのモデルを使うようにしてあります。
（Web検索が必要な部分だけOpenAI、それ以外はGemini、という構成です）
"""

import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel, set_tracing_disabled

load_dotenv(override=True)

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY が.envに設定されていません。Google AI StudioでAPIキーを取得してください。")

gemini_client = AsyncOpenAI(api_key=google_api_key, base_url=GEMINI_BASE_URL)

# 使いたいGeminiモデルを変えたい場合は、.envに GEMINI_MODEL_NAME を設定してください
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-flash-latest")

# このコースの「メインモデル」。各エージェントファイルはこれをimportして使う
MODEL_NAME = OpenAIChatCompletionsModel(model=GEMINI_MODEL_NAME, openai_client=gemini_client)

# GeminiのAPIキーではOpenAIのトレース機能(platform.openai.com/traces)は使えないため無効化
set_tracing_disabled(True)
