# tabs/conversation_tab.py
import uuid

import gradio as gr
from agents.conversation_agent import ConversationAgent
from utils.logger import LOG

# 初始化对话代理
conversation_agent = ConversationAgent()

def create_conversation_tab():
    with gr.Tab("对话"):
        gr.Markdown("## 练习英语对话 ")  # 对话练习说明
        session_id_text = gr.Textbox(visible=False, value=None)
        conversation_chatbot = gr.Chatbot(
            placeholder="<strong>你的英语私教 DjangoPeng</strong><br><br>想和我聊什么话题都可以，记得用英语哦！",  # 聊天机器人的占位符
            height=800,  # 聊天窗口高度
            type="messages"
        )

        # 处理用户对话的函数
        def handle_conversation(user_input, chat_history, session_id=None):
            if not session_id:
                session_id = str(uuid.uuid4())

            bot_message = conversation_agent.chat_with_history(user_input, "conversation" + session_id)  # 获取聊天机器人的回复
            LOG.info(f"[ChatBot]: {bot_message}")  # 记录聊天机器人的回复
            return bot_message  # 返回机器人的回复

        gr.ChatInterface(
            fn=handle_conversation,  # 处理对话的函数
            chatbot=conversation_chatbot,  # 聊天机器人组件
            additional_inputs=[session_id_text],
            stop_btn=None,
            submit_btn="发送",  # 发送按钮文本
            type="messages",
        )