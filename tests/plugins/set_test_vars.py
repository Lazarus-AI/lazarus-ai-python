import os


def pytest_configure():
    """ Sets environment variables for entire session.

    If pytest is running in Github actions, the environment variables
    will be set already. Replace the '...' with Lazarus credentials to
    run locally.
    """
    if not os.environ.get('FROM_WORKFLOW'):
        os.environ['BASE_URL'] = '...'
        os.environ['ORG_ID'] = '...'
        os.environ['AUTH_KEY'] = '...'
