"""翻訳をリモートのA2Aエージェントに委任するローカルコンシェルジュ。

RemoteA2aAgentはリモートエージェントのカードを読み込み、その後はローカルのサブエージェントの
ように振る舞う。コンシェルジュがユーザーとの対話を担当し、翻訳作業はA2A経由でリモートの
翻訳エージェントに引き渡す。a2a_demoフォルダから `adk web .` で起動する。
"""

import logging
import os
import warnings

from dotenv import load_dotenv

warnings.filterwarnings("ignore", message=r".*\[EXPERIMENTAL\].*")
logging.getLogger("google_genai._api_client").setLevel(logging.ERROR)

load_dotenv(override=True)
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "FALSE")

from google.adk.agents import LlmAgent  # noqa: E402
from google.adk.agents.remote_a2a_agent import (  # noqa: E402
    AGENT_CARD_WELL_KNOWN_PATH,
    RemoteA2aAgent,
)

# カードの完全なURL。RemoteA2aAgentは渡された文字列をそのまま使うため、ホスト名だけを渡すのではなく
# ベースURLとwell-knownパスを連結して組み立てる。
translator = RemoteA2aAgent(
    name="translator_agent",
    description="Remote agent that translates English into Spanish.",
    agent_card=f"http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}",
    use_legacy=False,
)

root_agent = LlmAgent(
    model="gemini-3.1-flash-lite",
    name="spanish_concierge",
    description="A concierge that answers in Spanish by delegating translation.",
    instruction=(
        "When the user wants something translated into Spanish, delegate to "
        "translator_agent and return its result."
    ),
    sub_agents=[translator],
)
