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


def reverse_geocode(x: float, y: float):
    '''
    좌표를 행정구역 주소로 변환
    '''
    url = "https://maps.apigw.ntruss.com/map-reversegeocode/v2/gc"
    params = {
        "coords": f"{x},{y}",
        "output": "json",
        "orders": "roadaddr,addr",
    }

    headers = {
        'x-ncp-apigw-api-key-id': NAVER_MAPS_ID,
        'x-ncp-apigw-api-key': NAVER_MAPS_SECRET,
        'Accept': "application/json",
    }

    res = requests.get(url, params=params, headers=headers, timeout=5)
    res.raise_for_status()
    data = res.json()

    results = data.get("results", [])
    if not results:
        return None

    region = results[0].get("region", {})
    area1 = (region.get("area1") or {}).get("name")
    area2 = (region.get("area2") or {}).get("name")
    area3 = (region.get("area3") or {}).get("name")

    parts = [p for p in [area1, area2, area3] if p]
    return {
        "area1": area1,
        "area2": area2,
        "area3": area3,
        "address": " ".join(parts),
    }
