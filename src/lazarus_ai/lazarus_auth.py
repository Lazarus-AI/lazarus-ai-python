"""Class: LazarusAuth

LazarusAuth holds and authenticates a user's Lazarus login credentials.
The Forms and RikAI classes must be initialized with a valid LazarusAuth
instance.

If the auth information provided is not valid, an InvalidAuthError
will be raised on initialization.
"""

import os
import sys
import requests

parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir)

from errors import InvalidAuthError

BASE_URL = os.environ.get("BASE_URL", "https://api.lazarusforms.com/")


class LazarusAuth:
    """A class to validate and store Lazarus auth credentials."""

    def __init__(self, org_id: str, auth_key: str):
        """Initialize a LazarusAuth() object.

        Org ID and Auth Key are authenticated on initialization.
        Initializing with invalid credentials will raise an error.

        Args:
            org_id (str): Lazarus organization ID
            auth_key (str): Lazarus authentication key
        """
        if not org_id or not auth_key:
            raise ValueError("Cannot initialize with an empty string.")
        self.headers = {"orgId": org_id, "authKey": auth_key}
        self.authenticate()


    def authenticate(self):
        """Authenticates Org ID and Auth Key.

        Posts a request to an API endpoint with no body. If the response
        is an AUTH_FAILURE with status code 403, we raise an error. Users
        will not be charged for this call as no pages are processed.

        Raises:
            InvalidAuthError
        """
        res = requests.post(f"{BASE_URL}/api/forms/generic", headers=self.headers)

        if res.status_code == 403:
            raise InvalidAuthError("Invalid org ID or auth key. Authentication failed.")


# LazarusAuth class usage examples
if __name__ == "__main__":
    org_id = os.environ.get("LAZARUS_ORG_ID")
    auth_key = os.environ.get("LAZARUS_AUTH_KEY")
    auth = LazarusAuth(org_id, auth_key)
