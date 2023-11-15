""" Lazarus Forms API Errors

Reformats API responses from failed requests into useful
error messages.
"""


class APIError(Exception):
    """Base class for errors returned from the API

    Attributes:
        status (str): Status of the API request
        message (str): Error message reported in the API request
        code (int): Response code from the API Request
        api_output (dict): Entire response from the API
    """

    def __init__(self, status, message, code, api_output=None):
        self.status = status
        self.message = message
        self.code = code
        self.api_output = api_output

    def __str__(self):
        """ Prints helpful message for user after traceback """
        error_string = ""
        if self.status is not None:
            error_string += f"\n\nSTATUS: {self.status}"
        if self.message is not None:
            error_string += f"\nMESSAGE: {self.message}"
        if self.code is not None:
            error_string += f"\nERROR CODE: {self.code}"
        if self.api_output is not None:
            error_string += f"\nAPI OUTPUT: {self.api_output}"

        return error_string


class AuthError(APIError):
    """Raised when API encounters an Authentication Failure """
