import os
import sys
import unittest
from unittest.mock import patch, mock_open, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from agents.conversation_agent import ConversationAgent


class TestConversationAgent(unittest.TestCase):

    @patch("agents.agent_base.AgentBase.create_chatbot")
    @patch("builtins.open", new_callable=mock_open, read_data="This is a mock prompt.")
    def test_initialization(self, mock_file, mock_create_chatbot):
        mock_chatbot = MagicMock()
        mock_create_chatbot.return_value = mock_chatbot
        mock_chatbot_with_history = MagicMock()
        with patch("agents.agent_base.RunnableWithMessageHistory", return_value=mock_chatbot_with_history):
            agent = ConversationAgent()

        # 测试基础属性
        self.assertEqual(agent.name, "conversation")
        self.assertEqual(agent.prompt, "This is a mock prompt.")
        self.assertEqual(agent.chatbot_with_history, mock_chatbot_with_history)
        self.assertTrue(agent.chatbot is not None)
        self.assertTrue(agent.chatbot_with_history is not None)

        # 验证 prompt 文件路径是否正确传递
        mock_file.assert_called_once_with("prompts/conversation_prompt.txt", mode="r", encoding="utf-8")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_prompt_file_not_found(self, mock_file):
        with self.assertRaises(FileNotFoundError):
            ConversationAgent()


if __name__ == '__main__':
    unittest.main()
