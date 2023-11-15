"""Class: RikAI

Posts requests to api/rikai/ endpoints. Requires a valid LazarusAuth
instance on initialization. Including the optional model_id argument
will create a custom RikAI instance, using the model corresponding to
the model_id over the standard RikAI model.
"""

import os
import sys
import requests

from .lazarus_auth import LazarusAuth

parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir)

import utils

BASE_URL = os.environ.get("BASE_URL", "https://api.lazarusforms.com/")


class RikAI:
    """A class to post requests to all rikai/ endpoints."""

    def __init__(self, auth: LazarusAuth, model_id=None):
        """Initialize a RikAI() object.

        Without model_id, creates a RikAI() object that uses the standard
        RikAI model. With model_id, creates a RikAI() object that uses
        the custom model corresponding to the model_id.

        Args:
            auth (LazarusAuth): Holds authenticated header information
            model_id (str, optional): Custom model ID, defaults to None
        """
        self.headers = auth.headers
        self.model_id = model_id


    def ask_question(self, input_type: str, input_str: str, question: list, **kwargs):
        """Posts a request to the relevant rikai/ endpoint.

        If the RikAI instance was not initialized with a model_id, we post to
        the api/rikai endpoint. If a model_id was supplied on init, we post
        to the api/rikai/custom/{model_id} endpoint.

        Args:
            input_type (str): Type of input expected [FILE_PATH, URL, BASE64]
            input_str (str): File to upload, expecting a file path, url, or a base64 encoded string
            question (list): A list of strings containing the question(s) to be asked
            kwargs (dict, optional): Must include at least one of the following fields
                file_id (str): Custom ID for the uploaded document
                metadata (dict): Data to be returned in the response
                webhook (str): Webhook to ping after call to API
                settings (dict): User settings specified in the request, for custom RikAI only
                return_ocr (bool): Set to True to add OCR results to the response, defaults to False
                language (str): A 2 character language code or the name of the language you wish to translate answers into
        """
        url = f"{BASE_URL}/api/rikai"
        possible_kwargs = ["file_id", "metadata", "webhook", "return_ocr", "language"]
        if self.model_id is not None:
            url += f"/custom/{self.model_id}"
            possible_kwargs.append("settings")

        kwargs = utils._validate_args(kwargs, possible_kwargs)

        headers = self.headers | utils._get_typed_headers(input_type)
        body = utils._get_typed_body(input_type, input_str)

        if input_type == "FILE_PATH":
            data = {"question": question} | kwargs
            response = requests.post(url, headers=headers, files=body, data=data)
        else:
            body |= {"question": question} | kwargs
            response = requests.post(url, headers=headers, json=body)

        if response.ok:
            resp = response.json()
            utils._record_metrics("rikai", self.headers, self.model_id, resp)
            return resp

        utils._record_metrics("rikai", self.headers, self.model_id)
        utils._error_handling(response)


    def summarize(self, input_type: str, input_str: str, fields: dict):
        """Posts a request to the rikai/summarize endpoint.

        Args:
            input_type (str): Type of input expected [URL, BASE64]
            input_str (str): File to upload, expecting a url or a base64 encoded string
            fields (dict): Required fields to prompt the summarizer
                document_type (str): Type of document to summarize
                summary_description (str): Description of what information should be included in the summary
                secondary_description (str, optional): A secondary summary description, including this will return a secondary summary
                json_format (str, optional): Specify a JSON output structure, content will be pulled from the resulting summary description
        """
        if input_type == "FILE_PATH":
            raise ValueError("Summarize only accepts \"URL\" and \"BASE64\" input types")

        url = f"{BASE_URL}/api/rikai/summarize"
        fields = utils._validate_args(fields, ["secondary_description", "json_format"], ["document_type", "summary_description"])

        headers = self.headers | utils._get_typed_headers(input_type)
        body = utils._get_typed_body(input_type, input_str) | {"fields": fields}

        response = requests.post(url, headers=headers, json=body)

        if response.ok:
            resp = response.json()
            utils._record_metrics("rikai/summarizer", self.headers, self.model_id, resp)
            return resp

        utils._record_metrics("rikai/summarizer", self.headers, self.model_id)
        utils._error_handling(response)


# RikAI class usage examples
if __name__ == "__main__":
    # Create a LazarusAuth object with your org ID and auth key
    org_id = os.environ.get("LAZARUS_ORG_ID")
    auth_key = os.environ.get("LAZARUS_AUTH_KEY")
    auth = LazarusAuth(org_id, auth_key)

    # Create a RikAI object
    rikai = RikAI(auth)
    # Create a custom RikAI object, model_id_here is your custom RikAI model ID
    custom_rikai = RikAI(auth, "model_id_here")

    # RikAI Q&A
    questions = ["What is this document about?", "When was this document published?"]
    # Upload a file using a local file path
    response = rikai.ask_question("FILE_PATH", "/path/to/file.pdf", questions)
    # Upload a file using a URL
    response = rikai.ask_question("URL", "https://fileurl.com", questions)
    # Upload a file using a Base64 encoded string
    response = rikai.ask_question("BASE64", "base64_encoded_string", questions)

    # RikAI Summarize
    fields = {
        "document_type": "A medical form",
        "summary_description": "List all patient personal information such as DOB and address",
        "secondary_description": "Any information related to the health of the patient",
        "json_format": "{\"Patient Name\":\"John Smith\",\"Patient Address\":\"1234 Home Drive, Boston, MA 02112\"}"
    }
    # Upload a file using a URL
    response = rikai.summarize("URL", "https://fileurl.com", fields)
    # Upload a file using a Base64 encoded string
    response = rikai.summarize("BASE64", "base64_encoded_string", fields)

    # Upload a file using optional args
    kwargs = {
        "return_ocr": True,
        "language": "Japanese",
        "settings": {
            "verbose": True,
        },
        "file_id": "filename",
        "metadata": {"foo": "bar"},
        "webhook": "https://pingme.com"
    }
    rikai.ask_question("URL", "https://fileurl.com", questions, **kwargs)
    rikai.ask_question("URL", "https://fileurl.com", questions, return_ocr=True, language="Japanese")
