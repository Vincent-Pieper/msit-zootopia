import os

import requests
from dotenv import load_dotenv


load_dotenv()


def fetch_data(animal_name: str) -> list[dict]:
    """Fetch animal data from the API."""
    url = "https://api.api-ninjas.com/v1/animals"
    params = get_params(animal_name)
    headers = get_headers()
    response = requests.get(url, params=params, headers=headers)
    return response.json()


def get_params(animal_name: str) -> dict[str, str]:
    """Return the API query parameters."""
    params = {
        "name": animal_name
    }
    return params


def get_headers() -> dict[str, str | None]:
    """Return the API request headers."""
    api_key = os.getenv("API_NINJAS_KEY")
    headers = {
        "X-Api-Key": api_key
    }
    return headers