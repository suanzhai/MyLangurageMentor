import os
import sys
import unittest
from unittest.mock import patch, MagicMock, mock_open

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from agents.scenario_agent import ScenarioAgent
from enums.scenario_enum import ScenarioEnum


class TestScenarioAgent(unittest.TestCase):
    def setUp(self):
        self.mock_prompt = "mock prompt"
        self.mock_intro = ['Hello', 'Hi']
        self.prompt_file = "prompts/test_prompt.txt"
        self.intro_file = "content/intro/test.json"

    @patch("agents.agent_base.AgentBase.create_chatbot")
    @patch("builtins.open", new_callable=mock_open, read_data='["Hello", "Hi"]')
    def test_initialization(self, mock_file, mock_create_chatbot):
        mock_chatbot = MagicMock()
        mock_create_chatbot.return_value = mock_chatbot
        mock_chatbot_with_history = MagicMock()
        with patch("agents.agent_base.RunnableWithMessageHistory", return_value=mock_chatbot_with_history):
            agent = ScenarioAgent(ScenarioEnum.JOB_INTERVIEW)  # 假设 ScenarioEnum.TEST.value == "test"

        self.assertEqual(agent.name, "job_interview")
        self.assertEqual(agent.prompt, '["Hello", "Hi"]')  # prompt 是通过 `open().read().strip()` 得到的
        self.assertEqual(agent.intro, ["Hello", "Hi"])
        mock_file.assert_any_call("prompts/job_interview_prompt.txt", mode="r", encoding="utf-8")
        mock_file.assert_any_call("content/intro/job_interview.json", mode="r", encoding="utf-8")

    @patch("agents.agent_base.AgentBase.create_chatbot")
    @patch("agents.scenario_agent.get_session_history")
    @patch("agents.scenario_agent.random.choice", return_value="Hi")
    @patch("agents.scenario_agent.AIMessage")
    @patch("agents.scenario_agent.LOG")
    @patch("builtins.open", new_callable=mock_open, read_data='["Hi"]')
    def test_start_new_session_adds_intro_if_empty_history(
            self, mock_file, mock_log, mock_ai_message, mock_random_choice, mock_get_history, mock_create_chatbot
    ):
        mock_history = MagicMock()
        mock_history.messages = []
        mock_history.add_message = MagicMock(side_effect=lambda message: mock_history.messages.append(message))
        mock_get_history.return_value = mock_history

        mock_ai_message_instance = MagicMock()
        mock_ai_message.return_value = mock_ai_message_instance
        mock_ai_message_instance.content = "Hi"

        mock_chatbot = MagicMock()
        mock_create_chatbot.return_value = mock_chatbot
        mock_chatbot_with_history = MagicMock()
        with patch("agents.agent_base.RunnableWithMessageHistory", return_value=mock_chatbot_with_history):
            agent = ScenarioAgent(ScenarioEnum.JOB_INTERVIEW)

        content = agent.start_new_session(session_id="session-1")

        mock_get_history.assert_called_once_with("session-1")
        mock_history.add_message.assert_called_once_with(mock_ai_message_instance)
        self.assertEqual(content, "Hi")

    @patch("agents.agent_base.AgentBase.create_chatbot")
    @patch("agents.scenario_agent.get_session_history")
    @patch("agents.scenario_agent.LOG")
    @patch("builtins.open", new_callable=mock_open, read_data='["Hi"]')
    def test_start_new_session_skips_intro_if_history_exists(
            self, mock_file, mock_log, mock_get_history, mock_create_chatbot
    ):
        mock_message = MagicMock()
        mock_message.content = "Already here"

        mock_history = MagicMock()
        mock_history.messages = [mock_message]
        mock_get_history.return_value = mock_history

        mock_chatbot = MagicMock()
        mock_create_chatbot.return_value = mock_chatbot
        mock_chatbot_with_history = MagicMock()
        with patch("agents.agent_base.RunnableWithMessageHistory", return_value=mock_chatbot_with_history):
            agent = ScenarioAgent(ScenarioEnum.HOTEL_CHECKIN)

        content = agent.start_new_session(session_id="session-1")

        mock_get_history.assert_called_once_with("session-1")
        mock_history.add_message.assert_not_called()
        self.assertEqual(content, "Already here")


if __name__ == "__main__":
    unittest.main()
