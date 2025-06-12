import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from unittest.mock import patch, mock_open, MagicMock

# 正确导入 src.agents.agent_base 中的类
from agents.agent_base import AgentBase


class TestAgentBase(unittest.TestCase):

    def setUp(self):
        self.prompt_text = "This is a system prompt."
        self.intro_data = [{"role": "system", "content": "Welcome!"}]
        self.prompt_file = "dummy_prompt.txt"
        self.intro_file = "dummy_intro.json"

    @patch("builtins.open", new_callable=mock_open, read_data="This is a system prompt.")
    def test_load_prompt_success(self, mock_file):
        mock_create_chatbot = MagicMock()
        mock_create_chatbot.invoke.return_value = MagicMock()
        with patch("agents.agent_base.AgentBase.create_chatbot", return_value=mock_create_chatbot):
            agent = AgentBase("TestAgent", self.prompt_file)
            self.assertEqual(agent.prompt, "This is a system prompt.")
            mock_file.assert_called_with(self.prompt_file, mode="r", encoding="utf-8")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_prompt_file_not_found(self, mock_file):
        with self.assertRaises(FileNotFoundError):
            AgentBase("TestAgent", "missing_prompt.txt")

    @patch("builtins.open", new_callable=mock_open, read_data='[{"role": "system", "content": "Welcome!"}]')
    def test_load_intro_success(self, mock_file):
        mock_create_chatbot = MagicMock()
        mock_create_chatbot.invoke.return_value = MagicMock()
        with patch("agents.agent_base.AgentBase.create_chatbot", return_value=mock_create_chatbot):
            agent = AgentBase("TestAgent", self.prompt_file, self.intro_file)
            self.assertEqual(agent.intro, self.intro_data)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_intro_file_not_found(self, mock_file):
        mock_create_chatbot = MagicMock()
        mock_create_chatbot.invoke.return_value = MagicMock()
        with patch("agents.agent_base.AgentBase.create_chatbot", return_value=mock_create_chatbot), \
                self.assertRaises(FileNotFoundError):
            AgentBase("TestAgent", self.prompt_file, "missing_intro.json")

    @patch("agents.agent_base.ChatOpenAI")
    @patch("agents.agent_base.ChatPromptTemplate.from_messages")
    def test_create_chatbot_pipeline(self, mock_from_messages, mock_chat_openai):
        mock_prompt_template = MagicMock()
        mock_from_messages.return_value = mock_prompt_template
        mock_chat_openai_instance = MagicMock()
        mock_chat_openai.return_value = mock_chat_openai_instance
        mock_prompt_template.__or__.return_value = mock_chat_openai_instance

        with patch("builtins.open", mock_open(read_data=self.prompt_text)):
            agent = AgentBase("TestAgent", self.prompt_file)

        self.assertEqual(agent.chatbot, mock_chat_openai_instance)

    @patch("agents.agent_base.AgentBase.create_chatbot")
    def test_chat_with_history(self, mock_create_chatbot):
        mock_chatbot = MagicMock()
        mock_chatbot_with_history = MagicMock()
        mock_chatbot_with_history.invoke.return_value.content = "Mock Response"

        mock_create_chatbot.return_value = mock_chatbot
        with patch("builtins.open", mock_open(read_data=self.prompt_text)), \
                patch("agents.agent_base.RunnableWithMessageHistory", return_value=mock_chatbot_with_history), \
                patch("agents.agent_base.LOG") as mock_log:
            agent = AgentBase("TestAgent", self.prompt_file)
            response = agent.chat_with_history("Hello!", session_id="test-session")

            self.assertEqual(response, "Mock Response")
            mock_chatbot_with_history.invoke.assert_called_once()
            mock_log.debug.assert_called()


if __name__ == "__main__":
    unittest.main()
