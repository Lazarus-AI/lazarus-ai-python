""" Unit testing the RikAI class """

import sys
import os
import pytest
import requests_mock

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(parent_dir)

from src import LazarusAuth, RikAI
from errors import ValidationError

BASE_URL = os.environ.get("BASE_URL")
INPUT_URL = "https://firebasestorage.googleapis.com/v0/b/lazarus-apis-testing.appspot.com/o/examples%2FSample%20Form.pdf?alt=media&token=5b537052-ea54-4be4-9d36-9620ee994c1c"

ORG_ID = os.environ.get("ORG_ID")
AUTH_KEY = os.environ.get("AUTH_KEY")
AUTH = LazarusAuth(ORG_ID, AUTH_KEY)


class TestRikAI():
    """ Unit tests for RikAI class """

    def test_ask_question_ok(self, requests_mock) -> None:
        """ Test standard successful call to ask_question """
        rikai = RikAI(AUTH)
        mock_response = {"status": "SUCCESS"}
        requests_mock.post(f"{BASE_URL}/api/rikai", headers=rikai.headers, json=mock_response)

        resp = rikai.ask_question("URL", INPUT_URL, "Question")

        assert resp == mock_response


    def test_ask_question_kwargs_ok(self, requests_mock) -> None:
        """ Test successful call to ask_question with kwargs """
        rikai = RikAI(AUTH)

        mock_response = {"status": "SUCCESS", "documentId": "file_id", "metadata": {}, "wehbook": "url"}
        requests_mock.post(f"{BASE_URL}/api/rikai", headers=rikai.headers, json=mock_response)

        kwargs = {"file_id": "file_id", "metadata": {}, "webhook": "url"}
        resp = rikai.ask_question("URL", INPUT_URL, "Question", **kwargs)

        assert resp == mock_response


    def test_ask_question_kwargs_bad(self, requests_mock) -> None:
        """ Test call to ask_question with bad kwargs """
        rikai = RikAI(AUTH)

        kwargs = {"badKwarg": "bad"}
        post_mock = requests_mock.post(f"{BASE_URL}/api/rikai")

        with pytest.raises(ValidationError):
            rikai.ask_question("URL", INPUT_URL, "Question", **kwargs)

        assert not post_mock.called


    def test_ask_question_custom_ok(self, requests_mock) -> None:
        """ Test successful custom RikAI call to ask_question """
        rikai = RikAI(AUTH, "Riky")
        mock_response = {"status": "SUCCESS"}
        requests_mock.post(f"{BASE_URL}/api/rikai/custom/Riky", headers=rikai.headers, json=mock_response)

        resp = rikai.ask_question("URL", INPUT_URL, "Question")

        assert resp == mock_response


    def test_summarize_req_fields_ok(self, requests_mock) -> None:
        """ Test successful call to summarize with required fields"""
        rikai = RikAI(AUTH)
        mock_response = {"status": "SUCCESS"}
        requests_mock.post(f"{BASE_URL}/api/rikai/summarize", headers=rikai.headers, json=mock_response)

        fields = {"document_type": "Medical form", "summary_description": "List all patient personal information such as DOB and address"}
        resp = rikai.summarize("URL", INPUT_URL, fields)

        assert resp == mock_response


    def test_summarize_all_fields_ok(self, requests_mock) -> None:
        """ Test successful call to summarize with required fields"""
        rikai = RikAI(AUTH)
        mock_response = {"status": "SUCCESS"}
        requests_mock.post(f"{BASE_URL}/api/rikai/summarize", headers=rikai.headers, json=mock_response)

        fields = {
            "document_type": "Medical form",
            "summary_description": "List all patient personal information such as DOB and address",
            "secondary_description": "Any information related to the health of the patient",
            "json_format": "{\"Patient Name\":\"john smith\",\"Patient Address\":\"1234 Home Drive, Boston, MA 02112\"}"
        }
        resp = rikai.summarize("URL", INPUT_URL, fields)

        assert resp == mock_response


    def test_summarize_fields_bad(self, requests_mock) -> None:
        """ Test successful call to summarize with required fields"""
        rikai = RikAI(AUTH)
        post_mock = requests_mock.post(f"{BASE_URL}/api/rikai/summarize", headers=rikai.headers)

        fields = {
            "document_type": "Medical form",
            "summary_description": "List all patient personal information such as DOB and address",
            "secondary_description": "Any information related to the health of the patient",
            "json_format": "{\"Patient Name\":\"john smith\",\"Patient Address\":\"1234 Home Drive, Boston, MA 02112\"}", 
            "test": True
        }
        with pytest.raises(ValidationError):
            rikai.summarize("URL", INPUT_URL, fields)

        assert not post_mock.called


    def test_summarize_input_type_bad(self, requests_mock) -> None:
        """ Summarizer endpoint does not accept multipart inputs """
        rikai = RikAI(AUTH)
        post_mock = requests_mock.post(f"{BASE_URL}/api/rikai/summarize", headers=rikai.headers)

        fields = {"document_type": "Medical form", "summary_description": "List all patient personal information such as DOB and address"}

        with pytest.raises(ValueError):
            rikai.summarize("FILE_PATH", "path_to_file", fields)

        assert not post_mock.called
