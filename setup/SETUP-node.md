# NodeJSとPlaywrightの追加セットアップ詳細

_Cursorでは、このファイルをExplorerで右クリックして「Open Preview」を選択すると整形された表示で見られます。または、Github上のオンライン版をご覧ください。_

第4週と第6週で、コンピューター上のNodeJSを使用します。

PCユーザーの方へ注意: WSLを使う場合は、Ubuntu側でも再度Node.jsをインストールする必要があります。

## Nodeのインストール手順

Node.jsがインストールされているか確認してください - v22以降である必要があります:  
`!node --version` 

インストールが必要な場合は、お使いのプラットフォームのパッケージマネージャーを使用してください:

Windowsの場合、PowerShellで:  
`winget install OpenJS.NodeJS.LTS`

Macの場合、Terminalで:  
`brew install node`

Linux(およびWSLを使うPCユーザー)の場合は、https://nodejs.org/en/download のLinux向け手順に従ってください。上記のパッケージマネージャーが使えない場合(例えば制限された業務用マシンなど)は、同じページでDockerやバージョンマネージャーの選択肢は無視して、**Windows Installer (.msi)** / **macOS Installer (.pkg)** ボタンをすべてデフォルト設定のまま使用してください。

**インストール後は、Cursorを完全に終了してから再度起動してください**(開いているターミナルもすべて閉じてください)。新しくインストールされたNodeは、すでに実行中だったプログラムからは見えません。ノートブックのカーネルだけを再起動しても不十分です - カーネルはCursorから環境を引き継いでいます。再起動後、ノートブックで以下が動作することを確認してください:

`!node --version`  
`!npx --version`
