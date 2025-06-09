from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from utils.logger import LOG

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()

    LOG.info(f"Session history for {session_id}: {session_id}")
    return store[session_id]