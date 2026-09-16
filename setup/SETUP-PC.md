## Master AI Agentic Engineering -  build autonomous AI Agents

# PC用セットアップ手順

PCの皆さん、ようこそ!

AIの最前線で作業するための強力な環境を整えるのは、私が望むほど簡単ではありません。難しい場合もあるでしょう。でも、この手順が確実に機能することを心から願っています!

問題にぶつかったら、遠慮なく連絡してください。私はあなたが素早く動き出せるようにここにいます。_詰まってしまう_感覚ほど嫌なものはありません。メッセージでも、メールでも、LinkedInのメッセージでも、すぐに解決できるようにお手伝いします!

メール: ed@edwarddonner.com  
LinkedIn: https://www.linkedin.com/in/eddonner/  
よくある質問に答えるデジタルアバター: https://edwarddonner.com/avatar

_Cursorでこれを見ている場合は、左側のExplorerでファイル名を右クリックし、「Open preview」を選択すると、整形されたバージョンを表示できます。_

コマンドプロンプトの使用に比較的不慣れな場合は、手順と練習問題付きの優れた[ガイド](https://chatgpt.com/share/67b0acea-ba38-8012-9c34-7a2541052665)がこちらにあります。まずこれに取り組んで、自信をつけることをお勧めします。

### 始める前に - 注意!PCの「4つの落とし穴」。必ずお読みください。

**特に注意**: 何人かの受講生が下記リストの3番と4番でつまずいています。これまでに自分のコンピューターで対処していない場合、いつか痛い目に遭うことになります 😅 - ぜひ以下を読んで確認してください!あなたのPCは260文字を超えるファイル名をサポートし、Microsoft Build Toolsがインストールされている必要があります。そうでないと、一部のデータサイエンス系パッケージが壊れてしまいます。

Windowsで開発する際に知っておくべき、よくある4つの落とし穴があります:

1. パーミッション。Windowsのパーミッションに関する[このチュートリアル](https://chatgpt.com/share/67b0ae58-d1a8-8012-82ca-74762b0408b0)をご覧ください  
2. アンチウイルス、ファイアウォール、VPN。これらはインストールやネットワークアクセスを妨げることがあります。必要に応じて一時的に無効化してみてください  
3. 悪名高いWindowsの260文字のファイル名制限 - 完全な[説明と修正方法](https://chatgpt.com/share/67b0afb9-1b60-8012-a9f7-f968a5a910c7)はこちらです!変更後は再起動が必要です。  
4. これまでコンピューターでデータサイエンス系パッケージを扱ったことがない場合は、Microsoft Build Toolsをインストールする必要があります。[こちらの手順](https://chatgpt.com/share/67b0b762-327c-8012-b809-b4ec3b9e7be0)を参照してください。ある受講生によると、Windows 11の方には[こちらの手順](https://github.com/bycloudai/InstallVSBuildToolsWindows)も役立つかもしれません。

### パート1: Cursorのインストール(下記の重要な注意点も参照!)

Cursorについて一言: かっこいいプロダクトですが、誰にでも合うわけではありません。AIの提案が不安定になる癖もあります。画面が表示されるまで時間がかかることもあります。お好みであれば、代わりにVS Code(または他の任意のIDE)を使うこともできます。Cursor自体はVS Codeをベースに構築されており、このコースのすべての内容はどちらでも問題なく動作します。

1. https://www.cursor.com/ からCursorにアクセスしてください
2. 右上の「Sign In」をクリックし、次に「Sign Up」でアカウントを作成してください
3. ダウンロードし、指示に従ってCursorをインストール・起動してください

Cursorを起動したら、すべての質問でデフォルトを選択して構いません。

重要な注意: Cursorは最近、起動後のデフォルト画面として新しい「Agents」スプラッシュ画面を表示するようになりました。Ctrl+Shift+Nで通常の画面に戻れます。この仕様が変わってほしいものです!詳細はこちらのQ54で:  
https://edwarddonner.com/avatar?q=54

### パート2: リポジトリのクローン

1. Cursorで新しいウィンドウを開く(File >> New WindowまたはCtrl+Shift+N)

2. そのウィンドウでターミナルを開く(View >> TerminalまたはCtrl+バッククォート)

3. `git --version` でgitがインストールされていることを確認してください

4. インストールされていなければ、**Gitをインストール**してください

動画で説明したよりもさらに簡単な方法として、Windows 11の方はターミナルで次のコマンドを入力すればインストールできるはずです: `winget install --id Git.Git -e`

Windows 10の方は、動画で紹介した方法はこちらです:

- https://git-scm.com/download/win からGitをダウンロード
- インストーラーを実行し、デフォルトのオプションでプロンプトに従ってください(OKを何度も押します!)

5. Cursorのターミナルに戻り、**プロジェクトフォルダに移動**してください:

プロジェクト用の特定のフォルダがある場合は、cdコマンドで移動してください。例:  
`cd C:\Users\YourUsername\projects`  
YourUsernameは実際のWindowsユーザー名に置き換えてください

プロジェクトフォルダがない場合は、作成できます:
```
mkdir C:\Users\YourUsername\projects
cd C:\Users\YourUsername\projects
```

6. **リポジトリをクローンする:**

Projectsフォルダのコマンドプロンプトで以下を入力してください:

`git clone https://github.com/ed-donner/agents.git`

これにより、Projectsフォルダ内に新しい`agents`ディレクトリが作成され、コースのコードがダウンロードされます。
`cd agents` でその中に移動してください。この`agents`ディレクトリは「プロジェクトのルートディレクトリ」と呼ばれます。

ディスク容量やネットワーク帯域に余裕がない場合は、mainブランチの最新版だけを取得する代替コマンドがあります:

`git clone --depth 1 --branch main https://github.com/ed-donner/agents.git`

7. このプロジェクトをCursorで開く(動画では誤って「ステップ3」と呼んでいます!)

ターミナルの上にあるメインのCursorウィンドウで、「Open Project」をクリックしてください

`agents`フォルダに移動し、ダブルクリックして内容を表示してください。

`agents`フォルダの中に入ったら「Select Folder」をクリックしてください。

Cursorのプロジェクトウィンドウが表示され、File Explorerの左上に大文字でAGENTSと表示されていれば、Agentsプロジェクトを正しく開けたことを示しています。

8. Cursorで拡張機能をインストールする

拡張機能ウィンドウを開いてください(Ctrl+Shift+XまたはViewメニュー >> Extensions)。  
「python」を検索し、AnysphereまたはMs-pythonのものをインストールしてください。  
「jupyter」を検索し、ms-toolsaiのものをインストールしてください。  
これらはすでにインストールされている場合もあります。

### パート3: 驚異的な`uv`

このコースでは、超高速なパッケージマネージャーであるuvを使用します。データサイエンスの世界で大きく普及していますが、それには理由があります。

高速で信頼性が高く、きっと気に入るはずです!

以下の手順に従ってuvをインストールしてください - 一番上にあるスタンドアロンインストーラーの方法を使うことをお勧めします:

https://docs.astral.sh/uv/getting-started/installation/

新しいターミナルを開く必要がある場合があります(+ボタン、またはCtrl+Shift+バッククォート)。

その後、`uv --version` を実行すると、バージョン番号が表示されるはずです。

uvのインストールで問題があれば、[私のFAQページのQ11](https://edwarddonner.com/avatar?q=11)を参照してください。

次に、Cursor内のプロジェクトで、View >> Terminalを選択して、Cursor内にターミナルウィンドウを表示してください。  
`pwd` と入力して現在のディレクトリを確認し、`C:\Users\YourUsername\Documents\Projects\agents` のような'agents'ディレクトリにいることを確認してください

まず `uv self update` を実行して、uvが最新バージョンであることを確認してください。

そして、単純に以下を実行してください:  
`uv sync`  
そのスピードと信頼性に驚いてください!必要であれば、uvがPython 3.12をインストールし、その後すべてのパッケージをインストールします。  

uvに関する問題があれば、[私のFAQページのQ11](https://edwarddonner.com/avatar?q=11)を参照してください。

すべてが正しく設定されているかの確認:  
1. プロジェクトのルートディレクトリ(agents)に'.venv'という名前のフォルダができていることを確認してください
2. `uv python list` を実行すると、リストにPython 3.12のバージョンが表示されるはずです(複数表示されることもあります)

参考として、uvを使う際の違い:  
uvでは、いくつかの操作が異なります:  
- `pip install xxx` の代わりに `uv add xxx` を使います - これは`pyproject.toml`ファイルに含まれ、次に必要になったときに自動的にインストールされます  
- `python my_script.py` の代わりに `uv run my_script.py` を使います。これは環境を更新・有効化してスクリプトを呼び出します  
- `uv run` を呼び出すたびにuvが自動で行うため、実際には`uv sync`を実行する必要はありません  
- pyproject.tomlは自分で編集しない方が良く、uv.lockは絶対に編集しないでください  
- uvには[こちら](https://docs.astral.sh/uv/)にとても優れたドキュメントがあります - 一読の価値ありです!

### パート4: OpenAIキー

これは**オプション**です - APIにお金を使いたくない場合は不要です。

しかし、Agenticシステムの最高のパフォーマンスを得るためには強くお勧めします。

APIコストが気になり、安価または無料の代替手段を使いたい場合は、[このガイド](../guides/09_ai_apis_and_ollama.ipynb)を参照してください。  
これには、OpenAIの代わりにOpenRouterを使う方法も含まれています。国によっては、こちらの方が便利な課金システムになっている場合があります。

_無料の代替手段(Ollama)を使うことにした場合は、このセットアップガイドのパート4とパート5をスキップしてください。APIキーも.envファイルも不要です。下記の「これで完了です!」の項目に直接進んでください。_

OpenAIの場合:

1. まだOpenAIアカウントがない場合は、こちらから作成してください:  
https://platform.openai.com/

2. OpenAIはAPI利用に最低額のクレジットを求めます。私の場合(米国)は\$5です。API呼び出しはこの\$5から消費されます。このコースでは、その一部しか使用しません。この投資はお勧めします。とても有効に活用できるはずです。ただし注意点として: Agenticシステムは従来のソフトウェアエンジニアリングよりも予測しにくく、それは通常意図されたものです!つまり、コストに関してはいくつかのリスクもあります。LLMには固定の予算を設定し、コストを注意深く監視してください。

OpenAIへのクレジット残高の追加は、Settings > Billingで行えます:  
https://platform.openai.com/settings/organization/billing/overview

自動チャージは**無効にする**ことをお勧めします!

3. APIキーを作成する

OpenAIのキーを設定するウェブページは https://platform.openai.com/api-keys です - 緑色の「Create new secret key」ボタンを押し、「Create secret key」を押してください。APIキーはどこか非公開の場所に記録しておいてください。後でOpenAIの画面から取得することはできません。`sk-proj-`で始まるはずです。

AnthropicとGoogleのキーも設定します。これは該当箇所に到達したときに行えます。  
- AnthropicのClaude APIは https://console.anthropic.com/  
- GoogleのGemini APIは https://aistudio.google.com/

コースの中で、無料または非常に低コストな他のAPIをいくつか設定するようご案内します。

### パート5: `.env`ファイル

キーを手に入れたら、`.env`ファイルを作成しましょう:

Cursorで、File Explorerのファイル一覧の下の空白部分を右クリックし、「New File」を選択して`.env`という名前を付けてください。

重要な点として: これは`agents`という名前のディレクトリの中に**必ず**置く必要があり、名前は正確に`.env`である**必要**があります - 「env」でも「env.txt」でも「.env.txt」でもなく、正確に4文字の`.env`でなければ動作しません!!

ファイルの中に、以下の内容を、正確に間違いなく入力してください:

`OPENAI_API_KEY=`

そして等号の後に、OpenAIから取得したキーを貼り付けてください。完了すると、次のようになるはずです:

`OPENAI_API_KEY=sk-proj-lots_of_characters_here`

もちろん、等号の右側の内容はあなたのキーと正確に一致している必要があります。

OPEN_API_KEY(AIの文字が欠けている)と誤って入力してしまう人や、値が`sk-proj-sk-proj-...`のようになってしまう人もいますので注意してください。

他のキーがあれば、それも追加できます。または今後の週にまた戻ってきても構いません:  
```
GOOGLE_API_KEY=xxxx
ANTHROPIC_API_KEY=xxxx
DEEPSEEK_API_KEY=xxxx
```

これで、あなた自身のキーが入った`.env`ファイルの誇らしい持ち主になり、準備は完了です。

**重要: .envファイルを編集した後は、必ず保存してください。**

停止サインの横にある白い点は、ファイルが保存されていないことを示しています。必ず保存してください!

## これで完了です!!

Cursorで始めるには、パート2で説明したPythonとJupyterの拡張機能がインストールされていることを確認してください。次に、左側のExplorerで`1_foundations`ディレクトリを開き、`1_lab1.ipynb`をダブルクリックして最初のラボを起動してください。右上付近の「Select Kernel」と表示されている箇所をクリックし、`.venv (Python 3.12.12)`またはそれに似た選択肢(最初の選択肢、または最も目立つ選択肢のはずです)を選択してください(先に「Python Environments」をクリックする必要があるかもしれません)。次に、最初のコードセルをクリックし、Shift + Enterを押して実行してください。

「Select Kernel」をクリックしても`.venv (Python 3.12.12)`のような選択肢が表示されない場合は、以下を行ってください:  
1. Fileメニューから、Preferences >> VSCode Settingsを選択してください(注意: `Cursor Settings`ではなく`VSCode Settings`を選択してください)  
2. Settingsの検索バーに「venv」と入力してください  
3. 「Path to folder with a list of Virtual Environments」というフィールドに、プロジェクトのルートのパス(例: C:\Users\username\projects\agents)を入力してください
そして再度試してください。

問題があれば、https://edwarddonner.com/avatar のデジタルアバターに質問してみてください。

これで動作しない場合や、何かお手伝いできることがあれば、ぜひメッセージまたはed@edwarddonner.comへメールをください。あなたがどう進んでいるか、楽しみにしています。
