from agents import Agent, WebSearchTool, ModelSettings
from dotenv import load_dotenv
import os

load_dotenv(override=True)

# 注意: このエージェントだけはOpenAIのモデルを使い続けます。
# WebSearchTool()はOpenAIがホストする専用ツールで、Responses API経由でのみ動作し、
# GeminiのOpenAI互換(Chat Completions)エンドポイントでは利用できないためです。
# それ以外のエージェント(planner/writer/email)はGeminiに切り替え済みです。
MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-5.4-mini")

INSTRUCTIONS = """
You are a research assistant. Given a search term, you search the web for that term and 
produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 words.
Capture the main points and be succinct. Reply only with the summary.
"""

settings = ModelSettings(tool_choice="required")
tools = [WebSearchTool()]

search_agent = Agent(name="Search Agent", instructions=INSTRUCTIONS, tools=tools, model=MODEL_NAME, model_settings=settings)