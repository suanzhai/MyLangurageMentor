from .agent_base import AgentBase

class ConversationAgent(AgentBase):
    """
    对话代理类，负责处理与用户的对话。
    """
    def __init__(self):
        super().__init__(
            name="conversation",
            prompt_file="prompts/conversation_prompt.txt"
        )
