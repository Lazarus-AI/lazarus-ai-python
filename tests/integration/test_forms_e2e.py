""" Integration testing the Forms class """

import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(parent_dir)

from src import LazarusAuth, Forms


def get_b64_test_file(path: str):
    with open(os.path.join(os.path.abspath(""), path)) as f:
        return f.read()


BASE_URL = os.environ.get("BASE_URL")

ORG_ID = os.environ.get("ORG_ID")
AUTH_KEY = os.environ.get("AUTH_KEY")
AUTH = LazarusAuth(ORG_ID, AUTH_KEY)

FILE_PATH = "tests/resources/sample_form.pdf"
INPUT_URL = "https://firebasestorage.googleapis.com/v0/b/lazarus-apis-testing.appspot.com/o/examples%2FSample%20Form.pdf?alt=media&token=5b537052-ea54-4be4-9d36-9620ee994c1c"
BASE64 = get_b64_test_file("tests/resources/sample_b64.txt")


class TestForms():
    """ Integration tests for Forms class """

    def test_run_ocr_file_path_ok(self) -> None:
        """ Test successful call to run_ocr with kwargs and input type FILE_PATH """
        forms = Forms(AUTH)
        kwargs = {"metadata": {"foo": "bar"}}
        resp = forms.run_ocr("FILE_PATH", FILE_PATH, **kwargs)

        assert resp["status"] == "SUCCESS"
        assert resp["ocrResults"]
        assert resp["keyValuePairs"]


    def test_run_ocr_url_ok(self) -> None:
        """ Test successful call to run_ocr with kwargs and input type URL """
        forms = Forms(AUTH)
        kwargs = {"file_id": "Sample File", "metadata": {"foo": "bar"}}
        resp = forms.run_ocr("URL", INPUT_URL, **kwargs)

        assert resp["status"] == "SUCCESS"
        assert resp["documentId"] == "Sample File"
        assert resp["metadata"] == {"foo": "bar"}


    def test_run_ocr_base64_ok(self) -> None:
        """ Test successful call to run_ocr with kwargs and input type BASE64 """
        forms = Forms(AUTH)
        kwargs = {"file_id": "Sample File", "metadata": {"foo": "bar"}}
        resp = forms.run_ocr("BASE64", BASE64, **kwargs)

        assert resp["status"] == "SUCCESS"
        assert resp["documentId"] == "Sample File"
        assert resp["metadata"] == {"foo": "bar"}


    def test_run_ocr_custom_ok(self) -> None:
        """ Test successful call to custom run_ocr """
        forms = Forms(AUTH, "test")
        resp = forms.run_ocr("URL", INPUT_URL)

        assert resp["status"] == "SUCCESS"
        assert resp["keyValuePairs"]


    def test_run_ocr_custom_kwargs_ok(self) -> None:
        """ Test successful custom Forms call with kwargs to run_ocr """
        forms = Forms(AUTH, "test")
        kwargs = {"file_id": "Sample File", "metadata": {"foo": "bar"}}
        resp = forms.run_ocr("URL", INPUT_URL, **kwargs)

        assert resp["status"] == "SUCCESS"
        assert resp["keyValuePairs"]
        assert resp["documentId"] == "Sample File"
        assert resp["metadata"] == {"foo": "bar"}
