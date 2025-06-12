import gradio as gr

from tabs.conversation_tab import ConversationTab
from tabs.scenario_tab import ScenarioTab
from tabs.vocab_tab import create_vocab_tab, VocabTab


def main():
    with gr.Blocks(title="LanguageMentor 英语私教") as language_mentor_app:
        ConversationTab().create_conversation_tab()
        ScenarioTab().create_scenario_tab()
        VocabTab().create_vocab_tab()
    
    # 启动应用
    language_mentor_app.launch(share=True, server_name="0.0.0.0")

if __name__ == "__main__":
    main()
