import warnings
import gradio as gr
from demo.ui import create_ui
from demo.util import css, js

# Gradio 6.14 は新しい Starlette でリネームされた Starlette のステータス定数を参照しているため、
# リクエストごとに警告が出る。ダッシュボードのコンソールを見やすくするため、このアップストリームの非推奨警告を抑制する。
warnings.filterwarnings("ignore", message=".*HTTP_422_UNPROCESSABLE_ENTITY.*")

if __name__ == "__main__":
    ui = create_ui()
    ui.launch(
        theme=gr.themes.Default(primary_hue="sky"),
        css=css,
        js=js,
        inbrowser=True,
    )
