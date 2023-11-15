"""Helper function to convert responses from failed requests to errors."""

import json
from requests import Response

from errors import APIError, AuthError


def _error_handling(response: Response):
    """Processes response with non-200 response code.

    If the response data is JSON serializable, use the data from the response
    in the error message. Otherwise, raises an error with just the status and
    error code.

    Args:
        response (Response): Response from post request
    Raises:
        APIError if response was not successful
        AuthError if org_id or auth_key were invalid
    """
    try:
        resp = response.json()

        # If there's more than just status and message in response,
        # include the response in api output
        api_output = None
        if resp.keys() > {"status", "message"}:
            api_output = resp

        if response.status_code == 403:
            raise AuthError("AUTH_FAILURE", resp["message"], 403, api_output)
        raise APIError("FAILURE", resp["message"], response.status_code, api_output)
    except (json.JSONDecodeError, KeyError):
        pass

    # If the response is not a json, return static info
    if response.status_code == 403:
        raise AuthError("AUTH_FAILURE", "Invalid authentication.", 403)
    raise APIError("FAILURE", None, response.status_code)
