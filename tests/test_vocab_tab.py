# tests/test_vocab_tab.py

import unittest
from unittest.mock import patch, MagicMock, mock_open
from tabs.vocab_tab import VocabTab


class TestVocabTab(unittest.TestCase):

    @patch("tabs.vocab_tab.VocabAgent")
    def setUp(self, mock_agent_cls):
        self.mock_agent = mock_agent_cls.return_value
        self.tab = VocabTab()

    @patch("builtins.open", new_callable=mock_open, read_data="This is a test intro.")
    def test_get_page_desc_file_exists(self, mock_file):
        result = self.tab.get_page_desc()
        self.assertEqual(result, "This is a test intro.")
        mock_file.assert_called_once_with("content/page/vocab_study.md", "r", encoding="utf-8")

    @patch("tabs.vocab_tab.LOG")
    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_get_page_desc_file_not_found(self, mock_open_func, mock_log):
        result = self.tab.get_page_desc()
        self.assertEqual(result, "词汇学习介绍文件未找到。")
        mock_log.error.assert_called_once()

    @patch("tabs.vocab_tab.VocabAgent")
    def test_restart_vocab_study_chatbot(self, mock_agent_cls):
        mock_agent = mock_agent_cls.return_value
        mock_agent.chat_with_history.return_value = "Great! Let's go."

        tab = VocabTab()
        session_id = "12345"
        chatbot_component = tab.restart_vocab_study_chatbot(session_id)

        mock_agent.start_new_session.assert_called_once_with(session_id)
        mock_agent.chat_with_history.assert_called_once_with("Let's do it")

        self.assertEqual(chatbot_component.value, [["Let's do it", "Great! Let's go."]])
        self.assertEqual(chatbot_component.height, 800)

    @patch("tabs.vocab_tab.LOG")
    def test_handle_vocab(self, mock_log):
        self.tab.vocab_agent.chat_with_history.return_value = "Nice try!"
        response = self.tab.handle_vocab("word", [], "session1")

        self.assertEqual(response, "Nice try!")
        self.tab.vocab_agent.chat_with_history.assert_called_once_with("word", "session1")
        mock_log.info.assert_called_once()


if __name__ == "__main__":
    unittest.main()
