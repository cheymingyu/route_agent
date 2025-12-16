import requests
import os

from dotenv import load_dotenv
load_dotenv()

NAVER_MAPS_ID = os.getenv("NAVER_MAPS_CLIENT_ID")
NAVER_MAPS_SECRET = os.getenv("NAVER_MAPS_CLIENT_SECRET")

def geocode(query: str):
    url = "https://maps.apigw.ntruss.com/map-geocode/v2/geocode"
    params = {'query': query}

    headers = {
        'x-ncp-apigw-api-key-id': NAVER_MAPS_ID,
        'x-ncp-apigw-api-key': NAVER_MAPS_SECRET,
        'Accept': "application/json",
    }

    res = requests.get(url, params=params, headers=headers)
    data = res.json()

    if not data["addresses"]:
        return None
    
    x = float(data['addresses'][0]['x'])
    y = float(data['addresses'][0]['y'])

    return {"x": x, "y": y}
