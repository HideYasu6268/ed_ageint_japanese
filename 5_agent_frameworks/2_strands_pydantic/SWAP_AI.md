# この日のモデルを別のものに切り替える

この日には`strands_worker.py`と`pydantic_worker.py`という2つのワーカーがあります。どちらもデフォルトでOpenAIの`gpt-5.4-mini`を使い、`WORKER_MODEL`環境変数から読み込むため、別のOpenAIモデルに切り替える最も簡単な方法は、実行時にそれを設定することです。例: `WORKER_MODEL=gpt-5.4 uv run strands_worker.py`。別のプロバイダーや任意のOpenAI互換エンドポイント(OpenRouter、ローカルサーバーなど)を使うには、各フレームワークがモデルにアクセスする箇所は1か所だけなので、実行しているワーカーの中でそこを変更してください。

## Strands

Strandsは専用のモデルクラスを通じて複数のプロバイダーと通信し、この日は`OpenAIModel`を使用しています。`client_args`(StrandsがそのままOpenAIクライアントに渡す引数)に`base_url`を追加することで別のエンドポイントを指定でき、そのエンドポイントが提供するモデルを`model_id`に設定してください:

```python
from strands.models.openai import OpenAIModel

model = OpenAIModel(
    client_args={
        "api_key": os.environ["OPENROUTER_API_KEY"],  # ローカルサーバーの場合は空でない任意の文字列でよい
        "base_url": "https://openrouter.ai/api/v1",   # Ollamaの場合は http://localhost:11434/v1
    },
    model_id="gpt-5.4-mini",
)
```

`base_url`を指定しない場合、`OpenAIModel`は`OPENAI_API_KEY`を使って直接OpenAIを呼び出します。`strands_worker.py`の他の部分は変更ありません。

## Pydantic AI

Pydantic AIは`provider:model`という文字列でプロバイダーを選択し、この日は`openai-chat:gpt-5.4-mini`(Chat Completionsを明示するプレフィックス)を使用しています。別のエンドポイントに接続するには、`base_url`と`api_key`を持つ`OpenAIProvider`を使って`OpenAIChatModel`を構築し、その文字列の代わりにそのモデルをエージェントに渡してください:

```python
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

model = OpenAIChatModel(
    "gpt-5.4-mini",
    provider=OpenAIProvider(
        base_url="https://openrouter.ai/api/v1",      # Ollamaの場合は http://localhost:11434/v1
        api_key=os.environ["OPENROUTER_API_KEY"],
    ),
)

worker = Agent(model, instructions=INSTRUCTIONS, tools=[show_todos, plan_steps, complete_task], toolsets=[filesystem])
```

クラス名は古い`OpenAIModel`ではなく`OpenAIChatModel`です。`openai-chat:gpt-5.4-mini`という文字列をそのまま残し、`.env`に`OPENAI_BASE_URL`と`OPENAI_API_KEY`を設定するだけでも構いません。

この日の他のすべての部分はまったく同じままです。ボードツール、ファイルシステムMCPサーバー、そしてボードはすべてモデルに依存しないため、変更が必要なのはこの1行のモデル指定だけです。
