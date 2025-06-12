import uuid

from agents.agent_base import AgentBase
from agents.session_history import get_session_history
from utils.logger import LOG


class VocabAgent(AgentBase):
    def __init__(self):
        prompt_file = f"prompts/vocab_study_prompt.txt"
        super().__init__(
            name="单词",
            prompt_file=prompt_file,
        )

    def start_new_session(self, session_id: str = None):
        if not session_id:
            session_id = self.name + str(uuid.uuid4())

        history = get_session_history(session_id)
        LOG.info(f"[history][{session_id}]:{history}")
        history.clear()
        
        return history
