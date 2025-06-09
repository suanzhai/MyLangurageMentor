import uuid

import gradio as gr
from langchain_core.chat_history import InMemoryChatMessageHistory

from agents.scenario_agent import ScenarioAgent
from enums.scenario_enum import ScenarioEnum
from utils.logger import LOG

agents = {
    ScenarioEnum.HOTEL_CHECKIN: ScenarioAgent(ScenarioEnum.HOTEL_CHECKIN),
    ScenarioEnum.JOB_INTERVIEW: ScenarioAgent(ScenarioEnum.JOB_INTERVIEW),
    ScenarioEnum.RENTING: ScenarioAgent(ScenarioEnum.RENTING),
}

def get_scenario_description(scenario : ScenarioEnum):
    if scenario not in agents:
        raise Exception(f"Unknown scenario {scenario.value}")

    try:
        with open(f"content/page/{scenario.value}.md", "r", encoding="utf-8") as file:
            scenario_intro = file.read().strip()
        return scenario_intro
    except FileNotFoundError:
        LOG.error(f"场景介绍文件 content/page/{scenario}.md 未找到！")
        return "场景介绍文件未找到。"

def start_new_scenario_chatbot(scenario : ScenarioEnum, session_id : str):
    scenario_session_id = scenario.value + session_id
    initial_ai_message = agents[scenario].start_new_session(scenario_session_id)  # 启动新会话并获取初始AI消息

    return gr.Chatbot(
        value=[(None, initial_ai_message)],  # 设置聊天机器人的初始消息
        height=600,  # 聊天窗口高度
    ), gr.State([])

def handle_scenario(user_input, chat_history, scenario, session_id : str):
    scenario_session_id = scenario + session_id
    bot_message = agents[ScenarioEnum(scenario)].chat_with_history(user_input, scenario_session_id)  # 获取场景代理的回复
    LOG.info(f"[ChatBot]: {bot_message}")  # 记录场景代理的回复
    return bot_message  # 返回场景代理的回复

def create_scenario_tab():
    with gr.Tab("场景"):  # 场景标签
        gr.Markdown("## 选择一个场景完成目标和挑战")  # 场景选择说明

        # 创建单选框组件
        scenario_radio = gr.Radio(
            choices=[
                ("酒店入住", "hotel_checkin"),  # 酒店入住选项
                ("工作面试", "job_interview"),
                ("房屋租赁", "renting")
            ],
            label="场景"  # 单选框标签
        )

        session_id_text = gr.Textbox(visible=False, value=None)
        scenario_intro = gr.Markdown()  # 场景介绍文本组件
        scenario_chatbot = gr.Chatbot(
            placeholder="<strong>你的英语私教 DjangoPeng</strong><br><br>选择场景后开始对话吧！",  # 聊天机器人的占位符
            height=600,  # 聊天窗口高度
        )
        chat_history = gr.State([])

        # 场景聊天界面
        scenario_chat_interface = gr.ChatInterface(
            fn=handle_scenario,  # 处理场景聊天的函数
            chatbot=scenario_chatbot,  # 聊天机器人组件
            additional_inputs=[scenario_radio, session_id_text],  # 额外输入为场景选择
            stop_btn=None,
            submit_btn="发送",  # 发送按钮文本
            autoscroll=True
        )

        def scenario_change(scenario, session_id):
            if not session_id:
                session_id = str(uuid.uuid4())

            desc = get_scenario_description(ScenarioEnum(scenario))
            temp_chatbot, temp_state = start_new_scenario_chatbot(ScenarioEnum(scenario), session_id)
            return session_id, desc, temp_chatbot, temp_state

        # 更新场景介绍并在场景变化时启动新会话
        scenario_radio.change(
            fn=scenario_change,     # 更新场景介绍和聊天机器人
            inputs=[scenario_radio, session_id_text], # 输入为选择的场景
            outputs=[session_id_text, scenario_intro, scenario_chatbot, chat_history],  # 输出为场景介绍和聊天机器人组件
        )