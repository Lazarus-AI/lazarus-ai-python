""" Integration testing the RikAI class """

import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(parent_dir)

from src import LazarusAuth, RikAI

def get_b64_test_file(path: str):
    with open(os.path.join(os.path.abspath(""), path)) as f:
        return f.read()


ORG_ID = os.environ.get("ORG_ID")
AUTH_KEY = os.environ.get("AUTH_KEY")
AUTH = LazarusAuth(ORG_ID, AUTH_KEY)

FILE_PATH = "tests/resources/sample_form.pdf"
INPUT_URL = "https://firebasestorage.googleapis.com/v0/b/lazarus-apis-testing.appspot.com/o/examples%2FSample%20Form.pdf?alt=media&token=5b537052-ea54-4be4-9d36-9620ee994c1c"
BASE64 = get_b64_test_file("tests/resources/sample_b64.txt")


class TestRikAI():
    """ Integration tests for RikAI class """

    def test_ask_question_file_path_ok(self) -> None:
        """ Test successful call to ask_question with FILE_PATH input type """
        rikai = RikAI(AUTH)
        kwargs = {"return_ocr": False, "language": "JA"}
        resp = rikai.ask_question("FILE_PATH", FILE_PATH, ["What is the name of the person?"], **kwargs)

        assert resp["status"] == "SUCCESS"
        assert resp["data"][0]["answer"]
        assert resp["data"][0]["translated"]
        assert resp["ocrResults"]


    def test_ask_question_url_ok(self) -> None:
        """ Test successful call to ask_question with URL input type """
        rikai = RikAI(AUTH)
        kwargs = {"return_ocr": True, "language": "JA"}
        resp = rikai.ask_question("URL", INPUT_URL, ["What is the name of the person?"], **kwargs)

        assert resp["status"] == "SUCCESS"
        assert resp["data"][0]["answer"]
        assert resp["data"][0]["translated"]
        assert resp["ocrResults"]


    def test_ask_question_base64_ok(self) -> None:
        """ Test successful call to ask_question with BASE64 input type """
        rikai = RikAI(AUTH)
        kwargs = {"return_ocr": True, "language": "JA"}
        resp = rikai.ask_question("BASE64", BASE64, ["What is the name of the person?"], **kwargs)

        assert resp["status"] == "SUCCESS"
        assert resp["data"][0]["answer"]
        assert resp["data"][0]["translated"]
        assert resp["ocrResults"]


    def test_ask_question_multiple_questions_ok(self) -> None:
        """ Test standard successful call to ask_question """
        rikai = RikAI(AUTH)
        resp = rikai.ask_question("URL", INPUT_URL, ["What is the name of the person?", "What is the document about?", "What is the patient's DOB?"])

        assert resp["status"] == "SUCCESS"
        assert resp["data"][0]["answer"]
        assert resp["data"][1]["answer"]


    def test_ask_question_custom_ok(self) -> None:
        """ Test successful custom RikAI call to ask_question """
        rikai = RikAI(AUTH, "Riky")
        resp = rikai.ask_question("URL", INPUT_URL, ["What is the name of the person?"])

        assert resp["status"] == "SUCCESS"
        assert resp["data"][0]["answer"]


    def test_ask_question_custom_multiple_questions_ok(self) -> None:
        """ Test successful custom RikAI call to ask_question with more than one question"""
        rikai = RikAI(AUTH, "Riky2")
        questions = [["When was the Onset Date of Disease/Injury of section a? Example: 7/29/2021","Return only the dates, without additional context. Example: 7/29/2021"],
                    ["When was the onset date of '\\''cause of the above'\\''? Example: 7/29/2021","Return only the dates, without additional context. Example: 7/29/2021"]]
        resp = rikai.ask_question("URL", INPUT_URL, questions)

        assert resp["status"] == "SUCCESS"
        assert resp["data"][0]["answer"]
        assert resp["data"][1]["answer"]


    def test_summarize_url_ok(self) -> None:
        """ Test successful call to summarize, URL input type """
        rikai = RikAI(AUTH)
        fields = {"document_type": "Medical form", "summary_description": "List all patient personal information such as DOB and address"}
        resp = rikai.summarize("URL", INPUT_URL, fields)

        assert resp["status"] == "SUCCESS"
        assert resp["data"]["summary"]


    def test_summarize_base64_ok(self) -> None:
        """ Test successful call to summarize, BASE64 input type """
        rikai = RikAI(AUTH)
        fields = {"document_type": "Medical form", "summary_description": "List all patient personal information such as DOB and address"}
        resp = rikai.summarize("BASE64", BASE64, fields)

        assert resp["status"] == "SUCCESS"
        assert resp["data"]["summary"]


    def test_summarize_all_fields_ok(self) -> None:
        """ Test successful call to summarize with optional fields, URL input type """
        rikai = RikAI(AUTH)
        fields = {
            "document_type": "Medical form",
            "summary_description": "List all patient personal information such as DOB and address",
            "secondary_description": "Any information related to the health of the patient",
            "json_format": "{\"Patient Name\":\"john smith\",\"Patient Address\":\"1234 Home Drive, Boston, MA 02112\"}"
        }
        resp = rikai.summarize("URL", INPUT_URL, fields)

        assert resp["status"] == "SUCCESS"
        assert resp["data"]["summary"]
