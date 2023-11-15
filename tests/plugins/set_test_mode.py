import os


def pytest_configure():
    """
    Set TEST_MODE to True before unit tests run.
    """
    os.environ['TEST_MODE'] = 'True'


def pytest_unconfigure():
    """
    Set TEST_MODE to False after unit tests run.
    """
    os.environ['TEST_MODE'] = 'False'
