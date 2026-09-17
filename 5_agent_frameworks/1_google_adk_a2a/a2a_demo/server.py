"""翻訳エージェントをA2Aサービスとして公開する。

`to_a2a` は通常のADKエージェントをStarletteアプリでラップし、エージェントカードを提供して
A2Aリクエストに応答するようにする。以下のようにuvicornで起動する。

    uvicorn server:a2a_app --host localhost --port 8001

to_a2aに渡すportはエージェントカードが広告する値なので、uvicornの--portと一致させる必要がある。
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
from google.adk.a2a.utils.agent_to_a2a import to_a2a  # noqa: E402

root_agent = LlmAgent(
    model="gemini-flash-latest",
    name="translator_agent",
    description="Translates English text into Spanish.",
    instruction=(
        "Translate the user's English text into natural Spanish. "
        "Reply with only the Spanish translation and nothing else."
    ),
)

# Starlette ASGIアプリを返す。ここで指定したportがエージェントカードの広告値になる。
a2a_app = to_a2a(root_agent, port=8001)
