""" Record library metrics """
import os
import requests


BASE_URL = os.environ.get("BASE_URL", "https://api.lazarusforms.com/")


def _record_metrics(endpoint: str, headers, model_id=None, response=None):
    """ Record metrics on successful and failed API requests using forms-python

    Args:
        endpoint (str): String indicating the endpoint in use
                Should be either "rikai", "forms", or "rikai/summarizer"
        headers: Authenticated header
        model_id (optional): Custom model ID. Defaults to None.
        response (optional): API response of successful requests. Defaults to None.
    """
    # Do not want to record metrics when running tests
    if os.getenv('TEST_MODE') == 'True':
        return

    metrics_url = f"{BASE_URL}/api/library-metrics/forms-python"
    if model_id:
        metrics_url += f"/{model_id}"

    data = {"endpoint": endpoint, "response": response}
    requests.post(metrics_url, headers=headers, json=data)
