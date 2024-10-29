# pypepper/api_request.py
import requests


def fetch_data(url, params=None):
    """Fetch data from a URL with optional parameters."""
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def post_data(url, data):
    """Send a POST request with JSON data."""
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()
