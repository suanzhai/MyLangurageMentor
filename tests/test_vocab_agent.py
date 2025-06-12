import os
import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from agents.vocab_agent import VocabAgent


class TestVocabAgent(unittest.TestCase):

    @patch("agents.agent_base.AgentBase.create_chatbot")
    @patch("builtins.open", create=True)
    def test_initialization(self, mock_open, mock_create_chatbot):
        # 模拟 prompt 文件读取内容
        mock_open.return_value.__enter__.return_value.read.return_value = "Mock prompt"
        mock_chatbot = MagicMock()
        mock_create_chatbot.return_value = mock_chatbot
        mock_chatbot_with_history = MagicMock()
        with patch("agents.agent_base.RunnableWithMessageHistory", return_value=mock_chatbot_with_history):
            agent = VocabAgent()

        self.assertEqual(agent.name, "单词")
        self.assertIn("vocab_study_prompt.txt", agent.prompt_file)
        self.assertEqual(agent.prompt, "Mock prompt")

    @patch("agents.agent_base.AgentBase.create_chatbot")
    @patch("agents.vocab_agent.get_session_history")
    @patch("agents.vocab_agent.LOG")
    @patch("builtins.open", create=True)
    def test_start_new_session_with_no_id(self, mock_open, mock_log, mock_get_history, mock_create_chatbot):
        # 模拟 prompt 文件
        mock_open.return_value.__enter__.return_value.read.return_value = "Mock prompt"

        # 准备 mock 历史
        mock_history = MagicMock()
        mock_get_history.return_value = mock_history

        mock_chatbot = MagicMock()
        mock_create_chatbot.return_value = mock_chatbot
        mock_chatbot_with_history = MagicMock()
        with patch("agents.agent_base.RunnableWithMessageHistory", return_value=mock_chatbot_with_history):
            agent = VocabAgent()

        result = agent.start_new_session()

        self.assertTrue(result is mock_history)
        mock_history.clear.assert_called_once()
        mock_log.info.assert_called_once()
        mock_get_history.assert_called_once()
        self.assertTrue(agent.name in mock_get_history.call_args[0][0])  # UUID拼接校验

    @patch("agents.agent_base.AgentBase.create_chatbot")
    @patch("agents.vocab_agent.get_session_history")
    @patch("agents.vocab_agent.LOG")
    @patch("builtins.open", create=True)
    def test_start_new_session_with_custom_id(self, mock_open, mock_log, mock_get_history, mock_create_chatbot):
        mock_open.return_value.__enter__.return_value.read.return_value = "Mock prompt"

        mock_history = MagicMock()
        mock_get_history.return_value = mock_history

        mock_chatbot = MagicMock()
        mock_create_chatbot.return_value = mock_chatbot
        mock_chatbot_with_history = MagicMock()
        with patch("agents.agent_base.RunnableWithMessageHistory", return_value=mock_chatbot_with_history):
            agent = VocabAgent()

        session_id = "test-session"
        result = agent.start_new_session(session_id)

        self.assertEqual(result, mock_history)
        mock_get_history.assert_called_once_with(session_id)
        mock_history.clear.assert_called_once()
        mock_log.info.assert_called_once_with(f"[history][{session_id}]:{mock_history}")


if __name__ == "__main__":
    unittest.main()
