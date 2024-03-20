import json
from main.library.tools.core.log_tool import LogTool
from main.library.utils.core.settings_helper import get

import http.client

from main.library.utils.models.validation_exception import ValidationException


class SpeechToTextTool:

    __token = None

    def __init__(self, logTool: LogTool):
        self.logTool = logTool

    def issue_token(self):
        az_speech_region = get("az_speech_region")
        assert az_speech_region is not None
        az_speech_host = get("az_speech_host")
        assert az_speech_host is not None
        az_speech_api_key = get("az_speech_api_key")
        assert az_speech_api_key is not None
        az_speech_issue_token_uri = get("az_speech_issue_token_uri")
        assert az_speech_issue_token_uri is not None
        conn = http.client.HTTPSConnection(
            f"{az_speech_region}.api.cognitive.{az_speech_host}"
        )
        payload = ""
        headers = {"Ocp-Apim-Subscription-Key": az_speech_api_key}
        conn.request("POST", az_speech_issue_token_uri, payload, headers)
        res = conn.getresponse()
        if res.status != 200:
            raise Exception(
                f"Failed to issue token: {res.status} - {res.reason} - {res.read()}"
            )
        data = res.read()
        token = data.decode("utf-8")
        assert token is not None
        self.__token = token
        self.logTool.info("Token issued successfully")

    def convert(self, audioContent: str, language: str = "pt-BR"):
        assert self.__token is not None
        assert language is not None
        assert audioContent is not None
        az_speech_region = get("az_speech_region")
        assert az_speech_region is not None
        az_speech_host = get("az_speech_host")
        assert az_speech_host is not None
        az_speech_api_key = get("az_speech_api_key")
        assert az_speech_api_key is not None
        az_speech_recognition_uri = get("az_speech_recognition_uri")
        assert az_speech_recognition_uri is not None
        conn = http.client.HTTPSConnection(
            f"{az_speech_region}.stt.speech.{az_speech_host}"
        )
        payload = audioContent
        headers = {
            "Ocp-Apim-Subscription-Key": az_speech_api_key,
            "Authorization": f"Bearer {self.__token}",
            "Content-Type": "audio/wav",
            "Accept": "application/json",
        }
        conn.request(
            "POST",
            az_speech_recognition_uri,
            payload,
            headers,
        )
        res = conn.getresponse()
        if res.status != 200:
            raise Exception(
                f"Failed to convert audio: {res.status} - {res.reason} - {res.read()}"
            )
        data = res.read()
        textJson = data.decode("utf-8")
        text = json.loads(textJson).get("DisplayText")
        self.logTool.info("Audio converted successfully")
        return text
