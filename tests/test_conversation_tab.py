# tests/test_conversation_tab.py

import unittest
from unittest.mock import patch, MagicMock
from tabs.conversation_tab import ConversationTab


class TestConversationTab(unittest.TestCase):

    @patch("tabs.conversation_tab.ConversationAgent")
    def test_handle_conversation_with_session_id(self, MockAgent):
        # Mock ConversationAgent 的返回值
        mock_agent_instance = MockAgent.return_value
        mock_agent_instance.chat_with_history.return_value = "Hello, how can I help you?"

        tab = ConversationTab()
        user_input = "Hi"
        session_id = "123abc"
        chat_history = []

        response = tab.handle_conversation(user_input, chat_history, session_id)

        self.assertEqual(response, "Hello, how can I help you?")
        mock_agent_instance.chat_with_history.assert_called_with(user_input, "conversation123abc")

    @patch("tabs.conversation_tab.uuid.uuid4", return_value="mocked-uuid")
    @patch("tabs.conversation_tab.ConversationAgent")
    def test_handle_conversation_without_session_id(self, MockAgent, mock_uuid):
        mock_agent_instance = MockAgent.return_value
        mock_agent_instance.chat_with_history.return_value = "What's your name?"

        tab = ConversationTab()
        user_input = "Who are you?"
        chat_history = []

        response = tab.handle_conversation(user_input, chat_history, session_id=None)

        self.assertEqual(response, "What's your name?")
        mock_agent_instance.chat_with_history.assert_called_with(user_input, "conversationmocked-uuid")

if __name__ == '__main__':
    unittest.main()
