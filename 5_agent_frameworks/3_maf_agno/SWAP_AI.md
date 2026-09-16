# この日のモデルを別のものに切り替える

この日には`maf_worker.py`と`agno_worker.py`という2つのワーカーがあります。どちらもデフォルトでOpenAIの`gpt-5.4-mini`を使い、`WORKER_MODEL`環境変数から読み込むため、別のOpenAIモデルに切り替える最も簡単な方法は、実行時にそれを設定することです。例: `WORKER_MODEL=gpt-5.4 uv run maf_worker.py`。別のプロバイダーや任意のOpenAI互換エンドポイント(OpenRouter、ローカルサーバーなど)を使うには、各フレームワークがモデルにアクセスする箇所は1か所だけなので、実行しているワーカーの中でそこを変更してください。

## Microsoft Agent Framework

MAFはチャットクライアントを通じてモデルにアクセスし、この日は`OpenAIChatClient`を使用しています。そのコンストラクタは`model`、`base_url`、`api_key`を直接受け取るため、別のエンドポイントを指定するのは1行で済みます:

```python
from agent_framework.openai import OpenAIChatClient

client = OpenAIChatClient(
    model="gpt-5.4-mini",
    base_url="https://openrouter.ai/api/v1",      # Ollamaの場合は http://localhost:11434/v1
    api_key=os.environ["OPENROUTER_API_KEY"],     # ローカルサーバーの場合は空でない任意の文字列でよい
)
```

`base_url`を指定しない場合、クライアントは`.env`から`OPENAI_API_KEY`を読み込み、直接OpenAIを呼び出します。`maf_worker.py`の他の部分は変更ありません。

## Agno

Agnoは`OpenAIChat`を通じてOpenAIを呼び出しますが、他のOpenAI互換エンドポイントの場合は`OpenAILike`が提供されており、同じ`id`に加えて`base_url`と`api_key`を受け取ります:

```python
from agno.models.openai.like import OpenAILike

model = OpenAILike(
    id="gpt-5.4-mini",
    base_url="https://openrouter.ai/api/v1",      # Ollamaの場合は http://localhost:11434/v1
    api_key=os.environ["OPENROUTER_API_KEY"],     # ローカルサーバーの場合は空でない任意の文字列でよい
)
```

`OpenAIChat`も`base_url`と`api_key`を受け取りますが、OpenAI以外のエンドポイント向けにはドキュメントで推奨されている`OpenAILike`を使ってください。`OpenAIChat(id=MODEL)`をこれに置き換えれば、`agno_worker.py`の残りの部分は変更ありません。

この日の他のすべての部分はまったく同じままです。ボードツール、ファイルシステムMCPサーバー、そしてボードはすべてモデルに依存しないため、変更が必要なのはこの1行のモデル指定だけです。
