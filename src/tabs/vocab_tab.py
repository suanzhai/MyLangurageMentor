# tabs/vocab_tab.py
import uuid
from abc import ABC

import gradio as gr

from agents.vocab_agent import VocabAgent
from utils.logger import LOG

class VocabTab(ABC):
    def __init__(self):
        # 初始化词汇代理，负责管理词汇学习会话
        self.vocab_agent = VocabAgent()
        # 定义功能名称为“vocab_study”，表示词汇学习模块
        self.feature = "vocab_study"

    # 获取页面描述，从指定的 markdown 文件中读取介绍内容
    def get_page_desc(self):
        try:
            # 打开指定的 markdown 文件来读取词汇学习介绍
            with open(f"content/page/{self.feature}.md", "r", encoding="utf-8") as file:
                scenario_intro = file.read().strip()  # 去除多余空白
            return scenario_intro
        except FileNotFoundError:
            # 如果找不到文件，记录错误并返回默认消息
            LOG.error(f"词汇学习介绍文件 content/page/{self.feature}.md 未找到！")
            return "词汇学习介绍文件未找到。"

    # 重新启动词汇学习聊天机器人会话
    def restart_vocab_study_chatbot(self, session_id:str):
        self.vocab_agent.start_new_session(session_id)  # 重启会话

        # 定义初始消息并与词汇代理交互生成机器人的回应
        _next_round = "Let's do it"
        bot_message = self.vocab_agent.chat_with_history(_next_round)

        # 返回一个带有初始消息和机器回复的聊天机器人界面
        return gr.Chatbot(
            value=[(_next_round, bot_message)],
            height=800,  # 设置聊天机器人组件的高度
        )

    # 处理用户输入的单词学习消息，并与词汇代理互动获取机器人的响应
    def handle_vocab(self, user_input, chat_history, session_id):
        bot_message = self.vocab_agent.chat_with_history(user_input, session_id)  # 获取机器回复
        LOG.info(f"[Vocab ChatBot]: {bot_message}")  # 记录机器人回应信息
        return bot_message

    # 创建词汇学习的 Tab 界面
    def create_vocab_tab(self):
        # 创建一个 Tab，标题为“单词”
        with gr.Tab("单词"):
            gr.Markdown("## 闯关背单词")  # 添加 Markdown 标题

            # 显示从文件中获取的页面描述
            gr.Markdown(self.get_page_desc())

            # 初始化一个聊天机器人组件，设置占位符文本和高度
            vocab_study_chatbot = gr.Chatbot(
                placeholder="<strong>你的英语私教 DjangoPeng</strong><br><br>开始学习新单词吧！",
                height=800,
            )

            session_id_text = gr.Textbox(visible=False, value=str(uuid.uuid4()))
            # 创建一个按钮，用于重置词汇学习状态，值为“下一关”
            restart_btn = gr.ClearButton(value="下一关")

            # 当用户点击按钮时，调用 restart_vocab_study_chatbot 函数
            restart_btn.click(
                fn=self.restart_vocab_study_chatbot,
                inputs=[session_id_text],
                outputs=vocab_study_chatbot,
            )

            # 创建聊天接口，包含处理用户消息的函数，并关联聊天机器人组件
            gr.ChatInterface(
                fn=self.handle_vocab,  # 处理用户输入的函数
                chatbot=vocab_study_chatbot,  # 关联的聊天机器人组件
                additional_inputs=[session_id_text],
                stop_btn=None,
                submit_btn="发送",  # 发送按钮的文本
            )
