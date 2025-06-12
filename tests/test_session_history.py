import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from agents.session_history import get_session_history, store
from langchain_core.chat_history import InMemoryChatMessageHistory


class TestGetSessionHistory(unittest.TestCase):
    def setUp(self):
        store.clear()  # 清除全局 store，防止测试间互相影响

    @patch("agents.session_history.LOG")
    def test_creates_new_history_when_not_exists(self, mock_log):
        session_id = "new-session"
        history = get_session_history(session_id)

        self.assertIn(session_id, store)
        self.assertIsInstance(history, InMemoryChatMessageHistory)
        self.assertEqual(store[session_id], history)
        mock_log.info.assert_called_once_with(f"Session history for {session_id}: {session_id}")

    @patch("agents.session_history.LOG")
    def test_returns_existing_history(self, mock_log):
        session_id = "existing-session"
        existing_history = InMemoryChatMessageHistory()
        store[session_id] = existing_history

        result = get_session_history(session_id)

        self.assertIs(result, existing_history)
        mock_log.info.assert_called_once_with(f"Session history for {session_id}: {session_id}")

    def test_store_is_shared(self):
        session_id = "shared"
        h1 = get_session_history(session_id)
        h2 = get_session_history(session_id)

        self.assertIs(h1, h2)
        self.assertEqual(len(store), 1)


if __name__ == "__main__":
    unittest.main()
