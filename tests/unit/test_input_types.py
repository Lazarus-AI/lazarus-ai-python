import sys
import os
import pytest

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(parent_dir)

import src.utils as utils


FILE_PATH = "tests/resources/sample_form.pdf"


def test_get_typed_headers():
    """ Tests functionality of utils/input_types.py::get_typed_headers() """

    # Test headers for valid input types
    headers = utils._get_typed_headers("FILE_PATH")
    assert not headers

    headers = utils._get_typed_headers("URL")
    assert headers["Content-Type"] == "application/json"

    headers = utils._get_typed_headers("BASE64")
    assert headers["Content-Type"] == "application/json"

    # test headers for invalid input type
    with pytest.raises(ValueError):
        utils._get_typed_headers("INVALID_INPUT_TYPE")


def test_get_typed_body():
    """ Tests functionality of utils/input_types.py::get_typed_body() """

    # Test body for valid input types
    body = utils._get_typed_body("FILE_PATH", FILE_PATH)
    assert body["file"]

    body = utils._get_typed_body("URL", "url")
    assert body["inputUrl"] == "url"

    body = utils._get_typed_body("BASE64", "base64")
    assert body["base64"] == "base64"

    # Test body for invalid input types
    with pytest.raises(ValueError):
        utils._get_typed_body("INVALID_INPUT_TYPE", "str")


def test_get_multipart_data():
    """ Tests functionality of utils/input_types.py::get_multipart_data() """

    # Test file with invalid extension
    with pytest.raises(ValueError):
        utils._get_multipart_data("bad_extension")

    # Test with file that does not exist
    with pytest.raises(FileNotFoundError):
        utils._get_multipart_data("bad_path.pdf")

    # Test with valid file
    assert utils._get_multipart_data(FILE_PATH)
