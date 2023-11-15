""" Unit testing the LazarusAuth class """

import sys
import os
import pytest

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(parent_dir)

from src import LazarusAuth
from errors import InvalidAuthError

ORG_ID = os.environ.get('ORG_ID')
AUTH_KEY = os.environ.get('AUTH_KEY')


class TestLazarusAuth:
    """ Unit tests for LazarusAuth class """

    def test_init_ok(self) -> None:
        """ Test whether valid init of LazarusAuth class is successful """
        auth = LazarusAuth(ORG_ID, AUTH_KEY)
        assert auth.headers == {"orgId": ORG_ID, "authKey": AUTH_KEY}


    def test_init_bad(self) -> None:
        """ Test init of LazarusAuth with bad credentials """
        with pytest.raises(InvalidAuthError):
            LazarusAuth("bad_org_id", "bad_auth_key")


    def test_init_empty_bad(self) -> None:
        """ Test whether an empty init of Lazarus class gets caught """
        with pytest.raises(ValueError):
            LazarusAuth("", "")
