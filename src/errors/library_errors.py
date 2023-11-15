""" Lazarus Forms Library Errors

Common errors that arise in using the library. Designed to prevent
hard to trace API Errors.
"""


class ValidationError(Exception):
    """Raised when Library encounters validation error"""


class InvalidAuthError(Exception):
    """Raised when initializing LazarusAuth encounters invalid auth info"""
