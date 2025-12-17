import requests
import os

from dotenv import load_dotenv
load_dotenv()

ODSAY_API_KEY = os.getenv("ODSAY_API_KEY")
ODSAY_BASE_URL = "https://api.odsay.com/v1/api/searchPubTransPathT"

def fetch_pubtrans_route(
        origin_coord: dict,
        dest_coord: dict,
) -> dict:

    params = {
        'SX': origin_coord['x'],
        'SY': origin_coord['y'],
        'EX': dest_coord['x'],
        'EY': dest_coord['y'],
        'apiKey': ODSAY_API_KEY
    }

    response = requests.get(ODSAY_BASE_URL, params=params, timeout=5)
    response.raise_for_status()
    return response.json()

