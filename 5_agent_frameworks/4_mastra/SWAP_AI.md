# この日のモデルを別のものに切り替える

MastraはVercel AI SDKを通じてモデルを解決するため、`model`フィールドには`provider/model`というルーティング文字列を指定します。私たちは`"openai/gpt-5.4-mini"`を使っており、これはOpenAIを選択し、`.env`から`OPENAI_API_KEY`を読み込みます。代わりに任意のOpenAI互換エンドポイント(OpenRouter、ローカルサーバー、ゲートウェイ)に対して実行するには、`baseURL`を持つプロバイダーを構築し、その結果得られるモデルインスタンスをエージェントに渡してください。

このフォルダにプロバイダーをインストールしてください(すでに依存関係に含まれているため、通常は何も起きません):

```bash
npm i @ai-sdk/openai
```

次に、プロバイダーを構築し、ルーティング文字列の代わりに使用してください:

```typescript
import { createOpenAI } from "@ai-sdk/openai";

const provider = createOpenAI({
  baseURL: process.env.OPENAI_BASE_URL, // 例: https://openrouter.ai/api/v1 や http://localhost:11434/v1
  apiKey: process.env.OPENAI_API_KEY,
});

const worker = new Agent({
  name: "Worker",
  instructions: INSTRUCTIONS,
  model: provider("gpt-5.4-mini"), // "openai/gpt-5.4-mini" という文字列の代わりに
  tools: { ...boardTools, ...(await filesystem.listTools()) },
});
```

デフォルトのベースURLは`https://api.openai.com/v1`です。`baseURL`を設定すると、すべての呼び出しがそこにリダイレクトされます。chat-completions形式を模倣するだけのエンドポイントの場合は、`@ai-sdk/openai-compatible`の`createOpenAICompatible({ baseURL, name, apiKey })`がより軽量な選択肢で、使い方も同じです: `compat("model-name")`。

この日の他のすべての部分はまったく同じままです。ボードツール、ファイルシステムMCPサーバー、そしてボードはすべてモデルに依存しないため、変更が必要なのはこの1行のモデル指定だけです。
