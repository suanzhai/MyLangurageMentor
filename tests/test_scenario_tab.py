import unittest
from unittest.mock import patch, MagicMock, mock_open

from enums.scenario_enum import ScenarioEnum
from tabs.scenario_tab import ScenarioTab


class TestScenarioTab(unittest.TestCase):

    def setUp(self):
        mock_create_chatbot = MagicMock()
        mock_create_chatbot.invoke.return_value = MagicMock()
        mock_chatbot_with_history = MagicMock()
        mock_chatbot_with_history.invoke.return_value.content = "Response from agent"
        mock_load_prompt = MagicMock()
        mock_load_prompt.invoke.return_value = "Hi"
        mock_load_intro = MagicMock()
        mock_load_intro.invoke.return_value = '["Hi", "Hello"]'

        with patch("agents.agent_base.AgentBase.create_chatbot", return_value=mock_create_chatbot), \
                patch("agents.agent_base.RunnableWithMessageHistory", return_value=mock_chatbot_with_history), \
                patch("agents.agent_base.AgentBase.load_prompt", return_value=mock_load_prompt), \
                patch("agents.agent_base.AgentBase.load_intro", return_value=mock_load_intro):
            self.tab = ScenarioTab()

    @patch("builtins.open", new_callable=mock_open, read_data="This is the scenario description.")
    def test_get_scenario_description_success(self, mock_file):
        desc = self.tab.get_scenario_description(ScenarioEnum.HOTEL_CHECKIN)
        self.assertEqual(desc, "This is the scenario description.")

    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("tabs.scenario_tab.LOG")
    def test_get_scenario_description_file_not_found(self, mock_log, mock_file):
        desc = self.tab.get_scenario_description(ScenarioEnum.HOTEL_CHECKIN)
        self.assertEqual(desc, "场景介绍文件未找到。")
        mock_log.error.assert_called_once()

    @patch("agents.scenario_agent.ScenarioAgent.start_new_session", return_value="Hello!")
    def test_start_new_scenario_chatbot(self, mock_start):
        chatbot, state = self.tab.start_new_scenario_chatbot(ScenarioEnum.HOTEL_CHECKIN, "123")
        self.assertIsNotNone(chatbot)
        self.assertEqual(chatbot.value, [[None, "Hello!"]])
        self.assertIsNotNone(state)

    @patch("tabs.scenario_tab.LOG")
    def test_handle_scenario(self, mock_log):
        response = self.tab.handle_scenario("Hi", [], "hotel_checkin", "123")
        self.assertEqual(response, "Response from agent")
        mock_log.info.assert_called_once()

    @patch.object(ScenarioTab, "get_scenario_description", return_value="desc")
    @patch.object(ScenarioTab, "start_new_scenario_chatbot", return_value=("chatbot", "state"))
    def test_scenario_change_with_session(self, mock_start, mock_desc):
        session_id, desc, chatbot, state = self.tab.scenario_change("hotel_checkin", "456")
        self.assertEqual(session_id, "456")
        self.assertEqual(desc, "desc")
        self.assertEqual(chatbot, "chatbot")
        self.assertEqual(state, "state")

    @patch("uuid.uuid4", return_value="uuid123")
    @patch.object(ScenarioTab, "get_scenario_description", return_value="desc")
    @patch.object(ScenarioTab, "start_new_scenario_chatbot", return_value=("chatbot", "state"))
    def test_scenario_change_without_session(self, mock_start, mock_desc, mock_uuid):
        session_id, desc, chatbot, state = self.tab.scenario_change("job_interview", None)
        self.assertEqual(session_id, "uuid123")
        self.assertEqual(desc, "desc")
        self.assertEqual(chatbot, "chatbot")
        self.assertEqual(state, "state")


if __name__ == "__main__":
    unittest.main()
