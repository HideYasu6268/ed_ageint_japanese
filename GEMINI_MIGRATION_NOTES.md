# Gemini移行メモ

このリポジトリのメインLLMをOpenAIから **Gemini (`gemini-flash-latest`)** に切り替えた際の変更点まとめです。

## 必要な準備

1. `.env` に `GOOGLE_API_KEY=...` を設定してください（Google AI Studioで取得）。
   Week 2/3日目の`.env`説明にすでに項目があるはずです。
2. `4_langchain_langgraph` を使う場合は、リポジトリルートで `uv sync` を実行してください
   （`pyproject.toml` に `langchain-google-genai` を追加したため）。
3. `5_agent_frameworks/4_mastra` はnpmパッケージの追加は不要です
   （既存の `@ai-sdk/openai` の `baseURL` をGeminiに向けているだけです）。

## 変更方式（共通の考え方）

- OpenAI Agents SDK系（`2_openai`, `6_mcp`）: `AsyncOpenAI(base_url=Geminiのエンドポイント)` を
  `OpenAIChatCompletionsModel` でラップし、`MODEL_NAME` としてどのエージェントにも渡す。
- LangChain（`4_langchain_langgraph`）: `ChatOpenAI` → `ChatGoogleGenerativeAI`、
  `create_agent(model="openai:...")` → `model="google_genai:gemini-flash-latest"`。
- Google ADK（`5_agent_frameworks/1_google_adk_a2a`）: もとからGeminiネイティブ。
  モデル文字列を`gemini-flash-latest`に統一しただけ。
- Strands / Pydantic AI（`2_strands_pydantic`）、MAF / Agno（`3_maf_agno`）:
  各フレームワークのOpenAI互換クライアント（`OpenAIModel`, `OpenAIChatModel`, `OpenAIChatClient`,
  `OpenAILike`）の`base_url`をGeminiのエンドポイントに向けた。
- Mastra（`4_mastra`, TypeScript）: `@ai-sdk/openai`の`createOpenAI({baseURL, apiKey})`を
  Gemini向けに構築し、共通の`gemini.ts`から読み込む。

## 意図的にOpenAIのまま残した箇所

- `2_openai/deep_research/search_agent.py`、`2_openai/4_lab4.ipynb`の検索エージェント:
  OpenAI Agents SDKの`WebSearchTool()`はOpenAIホスト専用ツールで、
  GeminiのOpenAI互換(Chat Completions)エンドポイントでは動作しないため。
- `3_lab3.ipynb`（`2_openai`, `4_langchain_langgraph`両方）のGroq/OpenRouter比較セクション:
  ご指示により変更していません。

## 解決済みだった問題（Gemini移行とは無関係、リポジトリ自体の欠落）

`6_mcp`フォルダで、以下のファイルが**存在しないのに参照されている**ことが判明しましたが、
本家の英語版リポジトリ(`ed-donner/agents`)から取得して復元しました:

- `backend/__init__.py`
- `backend/traders.py` — デフォルトモデルを`gemini-flash-latest`に変更済み。
  内部の`get_model()`がモデル名に`"gemini"`を含む場合、自動でGeminiのOpenAI互換
  エンドポイントを使うようになっている(このロジックはもともと入っていた)。
- `backend/tracers.py` — ローカルDBにログを書き込む`LogTracer`。OpenAIのトレースAPIには
  依存しないため、そのままGemini環境でも動作する。
- `backend/trading_floor.py` — `USE_MANY_MODELS=False`時のデフォルトモデルを
  `gemini-flash-latest`に変更済み。`USE_MANY_MODELS=True`時の多モデル比較リストは
  意図的にそのまま(GPT/DeepSeek/Gemini/Grokの比較用)。
- `frontend/`ディレクトリ一式 — OpenAI/モデルへの依存はなく、バックエンドAPIを
  読むだけの表示層なので無変更でコピー。

`4_lab4.ipynb`のセットアップセルも、この復元後の`traders.py`の設計(`get_model()`が
Gemini判定を内部で行う)に合わせて簡略化しました。**`set_tracing_disabled(True)`は
呼んでいません** — `tracers.py`のダッシュボード用ローカルトレースがそれに依存しているためです。
(OpenAIのホスト型トレースビューア(platform.openai.com/traces)だけは、有効なAPIキーが
ないため引き続き使えません。)
