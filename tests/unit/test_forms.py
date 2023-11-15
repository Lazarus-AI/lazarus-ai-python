""" Unit testing the Forms class """

import sys
import os
import pytest
import requests_mock

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(parent_dir)

from src import LazarusAuth, Forms
from errors import ValidationError

BASE_URL = os.environ.get("BASE_URL")
INPUT_URL = "https://firebasestorage.googleapis.com/v0/b/lazarus-apis-testing.appspot.com/o/examples%2FSample%20Form.pdf?alt=media&token=5b537052-ea54-4be4-9d36-9620ee994c1c"

ORG_ID = os.environ.get("ORG_ID")
AUTH_KEY = os.environ.get("AUTH_KEY")
AUTH = LazarusAuth(ORG_ID, AUTH_KEY)


class TestForms():
    """ Unit tests for Forms class """

    def test_run_ocr_ok(self, requests_mock):
        """ Test standard successful call to run_ocr """
        forms = Forms(AUTH)
        mock_response = {"status": "SUCCESS"}
        requests_mock.post(f"{BASE_URL}/api/forms/generic", headers=forms.headers, json=mock_response)

        resp = forms.run_ocr("URL", INPUT_URL)

        assert resp == mock_response


    def test_run_ocr_kwargs_ok(self, requests_mock):
        """ Test successful call to run_ocr with kwargs """
        forms = Forms(AUTH)

        mock_response = {"status": "SUCCESS", "documentId": "file_id", "metadata": {}, "webhook": "url"}
        requests_mock.post(f"{BASE_URL}/api/forms/generic", headers=forms.headers, json=mock_response)

        kwargs = {"file_id": "file_id", "metadata": {}, "webhook": "url"}
        resp = forms.run_ocr("URL", INPUT_URL, **kwargs)

        assert resp == mock_response


    def test_run_ocr_kwargs_bad(self, requests_mock):
        """ Test call to run_ocr with bad kwargs """
        forms = Forms(AUTH)

        kwargs = {"badKwarg": "bad"}
        post_mock = requests_mock.post(f"{BASE_URL}/api/forms/generic")

        with pytest.raises(ValidationError):
            forms.run_ocr("URL", INPUT_URL, **kwargs)

        assert not post_mock.called
