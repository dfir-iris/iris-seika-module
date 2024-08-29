import requests


def send_api_request(api_endpoint: str, api_key: str):
    """
    Sends a GET request to the specified API endpoint with the API key in the X-API-Key header.

    :param api_endpoint: The API endpoint URL
    :param api_key: The API key for authentication
    :return: The response from the API
    """
    headers = {
        'X-API-Key': api_key
    }

    try:

        response = requests.get(api_endpoint, headers=headers)
        response.raise_for_status()
        return response

    except requests.exceptions.RequestException as e:
        if response.status_code == 404:
            return response

        return None
