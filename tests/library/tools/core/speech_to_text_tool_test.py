import sys, os, pytest

sys.path.insert(0, os.path.abspath("."))
from main.library.di_container import Container
from main.library.tools.core.log_tool import LogTool
from main.library.utils.core.settings_helper import load_environment
from main.library.utils.core.path_helper import get_root_dir

import pytest
from unittest import mock
from main.library.tools.core.speech_to_text_tool import SpeechToTextTool

container = Container()
log_tool = container.log_tool()


@pytest.fixture
def speech_to_text_tool():
    load_environment("dev")
    speech_to_text_tool = container.speech_to_text_tool()
    return speech_to_text_tool


def test_should_issue_token(speech_to_text_tool):
    expected_token = "mocked_token"
    expected_response = mock.Mock()
    expected_response.status = 200
    expected_response.read.return_value = expected_token.encode("utf-8")
    conn_mock = mock.Mock()
    conn_mock.getresponse.return_value = expected_response
    http_client_mock = mock.Mock()
    http_client_mock.HTTPSConnection.return_value = conn_mock
    with mock.patch(
        "main.library.tools.core.speech_to_text_tool.http.client", http_client_mock
    ):
        speech_to_text_tool.issue_token()
        assert speech_to_text_tool._SpeechToTextTool__token == expected_token


def test_should_convert(speech_to_text_tool):
    expected_text = "mocked_text"
    expected_response = mock.Mock()
    expected_response.status = 200
    expected_response.read.return_value = '{"DisplayText": "mocked_text"}'.encode(
        "utf-8"
    )
    conn_mock = mock.Mock()
    conn_mock.getresponse.return_value = expected_response
    http_client_mock = mock.Mock()
    http_client_mock.HTTPSConnection.return_value = conn_mock
    speech_to_text_tool._SpeechToTextTool__token = "mocked_token"
    with mock.patch(
        "main.library.tools.core.speech_to_text_tool.http.client", http_client_mock
    ):
        root_dir = get_root_dir()
        audio_content = "mocked_audio_content"
        text = speech_to_text_tool.convert(audio_content)
        log_tool.info(f"Text: {text}")
        assert text == expected_text
