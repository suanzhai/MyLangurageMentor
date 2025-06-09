import random
import uuid

from langchain_core.messages import AIMessage

from agents.agent_base import AgentBase
from agents.session_history import get_session_history
from enums.scenario_enum import ScenarioEnum
from utils.logger import LOG


class ScenarioAgent(AgentBase):
    def __init__(self, scenario : ScenarioEnum):
        prompt_file =  f"prompts/{scenario.value}_prompt.txt"
        intro_file = f"content/intro/{scenario.value}.json"
        super().__init__(
            name=scenario.value,
            prompt_file=prompt_file,
            intro_file=intro_file
        )

    def start_new_session(self, session_id: str = None):
        if not session_id:
            session_id = self.name + str(uuid.uuid4())

        history = get_session_history(session_id)
        LOG.info(f"[history][{session_id}]:{history}")

        if not history.messages:
            first_message = AIMessage(content=random.choice(self.intro))
            history.add_message(first_message)

        return history.messages[-1].content