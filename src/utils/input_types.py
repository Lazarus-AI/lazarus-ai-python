"""Helper functions used to map input types to requests and responses."""

import os
import sys

parent_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(parent_dir)

# Mapping file extensions to their MIME types
FILE_EXTENSIONS = {
    '.pdf': 'application/pdf',
    '.png': 'image/png',
    '.jpeg': 'image/jpg',
    '.jpg': 'image/jpg',
    '.tif': 'image/tiff',
    '.tiff': 'image/tiff',
    '.webp': 'image/webp'
}


def _get_typed_headers(input_type: str) -> dict:
    """Maps input_type to request headers.

    Args:
        input_type (str): Type of input expected [FILE_PATH, URL, BASE64]
    Returns:
        dict: Content type key-value pair
    """
    match input_type:
        case "FILE_PATH":
            return {}
        case "URL" | "BASE64":
            return {"Content-Type": "application/json"}
        case _:
            raise ValueError("Expected one of: \"FILE_PATH\", \"URL\", \"BASE64\"")


def _get_typed_body(input_type: str, input_str: str):
    """Maps input_type and input_str to request body fields.

    Args:
        input_type (str): Type of input expected [FILE_PATH, URL, BASE64]
        input_str (str): A path to a file, url or a base64 encoded string
    Returns:
        dict: Request body key-value pairs
    """
    match input_type:
        case "FILE_PATH":
            return {"file": _get_multipart_data(input_str)}
        case "URL":
            return {"inputUrl": input_str}
        case "BASE64":
            return {"base64": input_str}
        case _:
            raise ValueError("Expected one of: \"FILE_PATH\", \"URL\", \"BASE64\"")


def _get_multipart_data(path: str) -> tuple:
    """Converts a file path into Multipart Encoded data.

    Extracts necessary info from the path, extends it to an absolute
    path, and creates a tuple holding file information that can be passed
    to a request in the data parameter. This function will raise a 
    FileNotFoundError if the path supplied is invalid.

    Args:
        path (str): File path
    Returns:
        tuple: Corresponds to (file name, read file object, MIME type)
    """
    filename = os.path.basename(path)
    _, ext = os.path.splitext(filename)
    path = os.path.join(os.path.abspath(""), path)

    if ext not in FILE_EXTENSIONS:
        raise ValueError(f"File must be one of: {FILE_EXTENSIONS.keys()}")

    return (filename, open(path, 'rb'), FILE_EXTENSIONS[ext])
