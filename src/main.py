import gradio as gr

from tabs.conversation_tab import create_conversation_tab
from tabs.scenario_tab import create_scenario_tab


def main():
    with gr.Blocks(title="LanguageMentor 英语私教") as language_mentor_app:
        create_conversation_tab()
        create_scenario_tab()
    
    # 启动应用
    language_mentor_app.launch(share=True, server_name="0.0.0.0")

if __name__ == "__main__":
    main()
