"""Class: Forms

Posts requests to forms/ endpoints. Requires a valid LazarusAuth
instance on initialization. Including the optional model_id argument
will create a custom Forms instance, using the model corresponding to
the model_id over the generic Forms model.
"""

import sys
import os
import requests

from .lazarus_auth import LazarusAuth

parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir)

import utils

BASE_URL = os.environ.get("BASE_URL", "https://api.lazarusforms.com/")


class Forms:
    """A class to post requests to all forms/ endpoints."""

    def __init__(self, auth: LazarusAuth, model_id=None):
        """Initialize a Forms() object.

        Without model_id, creates a Forms() object that uses the generic
        forms model. With model_id, creates a Forms() object that uses
        the custom model corresponding to the model_id.

        Args:
            auth (LazarusAuth): Holds authenticated header information
            model_id (str, optional): Custom model ID, defaults to None
        """
        self.headers = auth.headers
        self.model_id = model_id


    def run_ocr(self, input_type, input_str, **kwargs):
        """Posts a request to the relevant forms/ endpoint.

        If the Forms instance was not initialized with a model_id, we post to
        the api/forms/generic endpoint. If a model_id was supplied on init, we
        post to the api/forms/custom/{model_id} endpoint.

        Args:
            input_type (str): Type of input expected [FILE_PATH, URL, BASE64]
            input_str (str): File to upload, expecting a file path, url, or a base64 encoded string
            kwargs (dict, optional): Must include at least one of the following fields
                file_id (str): Custom ID for the uploaded document
                metadata (dict): Data to be returned in the response
                webhook (str): Webhook to ping after call to API
        """
        possible_kwargs = ["file_id", "metadata", "webhook"]
        kwargs = utils._validate_args(kwargs, possible_kwargs)

        if self.model_id is not None:
            url = f"{BASE_URL}/api/forms/custom/{self.model_id}"
        else:
            url = f"{BASE_URL}/api/forms/generic"

        headers = self.headers | utils._get_typed_headers(input_type)
        data = utils._get_typed_body(input_type, input_str)

        if input_type == "FILE_PATH":
            response = requests.post(url, headers=headers, files=data, data=kwargs)
        else:
            response = requests.post(url, headers=headers, json=data | kwargs)

        if response.ok:
            resp = response.json()
            utils._record_metrics("forms", self.headers, self.model_id, resp)
            return resp

        utils._record_metrics("forms", self.headers, self.model_id)
        utils._error_handling(response)


# Forms class usage examples
if __name__ == "__main__":
    # Create a LazarusAuth object with your org ID and auth key
    org_id = os.environ.get("LAZARUS_ORG_ID")
    auth_key = os.environ.get("LAZARUS_AUTH_KEY")
    auth = LazarusAuth(org_id, auth_key)

    # Create a Forms object
    forms = Forms(auth)
    # Create a custom Forms object, model_id is your custom Forms model
    custom_forms = Forms(auth, model_id="MODEL_ID_HERE")

    # Upload a file using a path to a file
    response = forms.run_ocr("FILE_PATH", "/path/to/file.pdf")
    # Upload a file using a URL
    response = forms.run_ocr("URL", "https://fileurl.com")
    # Upload a file using a Base64 encoded string
    response = forms.run_ocr("BASE64", "base64_encoded_string")

    # Upload a file using optional args
    kwargs = {
        "file_id": "filename", 
        "metadata": {"foo": "bar"}, 
        "webhook": "https://pingme.com"
    }
    forms.run_ocr("URL", "https://fileurl.com", **kwargs)
    forms.run_ocr("URL", "https://fileurl.com", file_id="filename", metadata={"foo": "bar"}, webhook="https://pingme.com")
