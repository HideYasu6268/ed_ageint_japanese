"""ライブラリの出力音量を下げて、エージェント自身のトレースを読みやすくする。

ADKは[EXPERIMENTAL]機能の通知をいくつも出力し、google-genaiはGOOGLE_API_KEYと
GEMINI_API_KEYが両方環境変数にあると毎回ログを出す(CrewAIの週の名残で、実害はない)。
どちらもこちらで対処すべきものではないので、静かにする。ADKをimportする前にsilence()を
呼び出すこと。
"""

import logging
import warnings


def silence() -> None:
    warnings.filterwarnings("ignore", message=r".*\[EXPERIMENTAL\].*")
    logging.getLogger("google_genai._api_client").setLevel(logging.ERROR)
