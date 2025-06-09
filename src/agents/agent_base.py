import json
import uuid
from abc import ABC

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable, RunnableWithMessageHistory, RunnableConfig
from langchain_openai import ChatOpenAI

from agents.session_history import get_session_history
from utils.logger import LOG


class AgentBase(ABC):
    def __init__(self, name, prompt_file, intro_file = None):
        self.name = name
        self.prompt_file = prompt_file
        self.intro_file = intro_file
        self.prompt = self.load_prompt()
        self.intro = self.load_intro() if intro_file else []
        self.chatbot = self.create_chatbot()
        self.chatbot_with_history = RunnableWithMessageHistory(self.chatbot, get_session_history)

    def load_prompt(self) -> str:
        try:
            with open(self.prompt_file, mode="r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f'Prompt file {self.prompt_file} not found')

    def load_intro(self) -> list:
        try:
            with open(self.intro_file, mode="r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f'Intro file {self.intro_file} not found')

    def create_chatbot(self) -> Runnable:
        system_prompt = ChatPromptTemplate.from_messages([
            ("system", self.prompt),
            MessagesPlaceholder(variable_name="messages")
        ])

        return system_prompt | ChatOpenAI(model="gpt-4o-mini")

    def chat_with_history(self, user_input, session_id=None) -> str:
        if session_id is None:
            session_id = self.name + str(uuid.uuid4())

        response = self.chatbot_with_history.invoke(
            [HumanMessage(content=user_input)],
            RunnableConfig(configurable={"session_id": session_id}),
        )

        LOG.debug(f"[ChatBot][{self.name}] {response.content}")  # 记录调试日志
        return response.content