# この日のモデルを別のものに切り替える

ADKはネイティブにGeminiと通信します。代わりにOpenAI互換のエンドポイント(OpenAI、OpenRouter、ローカルサーバーなど)に対して実行するには、ADKはLiteLLMを経由してルーティングします。

このフォルダで拡張機能をインストールしてください:

```bash
uv add "google-adk[extensions]"
```

次に、モデルをラップします。`task_worker/agent.py`で、モデル文字列を`LiteLlm`インスタンスに置き換えてください:

```python
from google.adk.models.lite_llm import LiteLlm

root_agent = LlmAgent(
    model=LiteLlm(model="openai/gpt-5.4-mini"),   # LiteLLMのモデル文字列であれば何でも可
    name="task_worker",
    description="Works one task from the SQLite board using its files.",
    instruction=...,        # 変更なし
    tools=[show_todos, plan_steps, complete_task, filesystem],
)
```

`openai/`というプレフィックスは、LiteLLMにOpenAIのチャットプロトコルを使うよう指示します。`.env`に`OPENAI_API_KEY`があれば、`openai/gpt-5.4-mini`はそれ以上の設定なしで動作します。

OpenRouterのようなカスタムエンドポイントの場合は、`api_base`と`api_key`を渡してください:

```python
import os

model = LiteLlm(
    model="openai/gpt-5.4-mini",
    api_base="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
```

この日の他のすべての部分はまったく同じままです。ツール、ファイルシステムMCPサーバー、そしてボードはすべてモデルに依存しないため、変更が必要なのはこの1行のモデル指定だけです。
