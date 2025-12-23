from typing import Dict, List
import requests
import os

from dotenv import load_dotenv
load_dotenv()

NAVER_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_SECRET = os.getenv("NAVER_CLIENT_SECRET")

def search_address(query: str):
    '''
    특정 장소가 입력되면 그 장소의 주소 반환
    '''
    url = "https://openapi.naver.com/v1/search/local.json"
    params = {"query": query}

    headers = {
        "X-Naver-Client-Id": NAVER_ID,
        "X-Naver-Client-Secret": NAVER_SECRET,
    }

    res = requests.get(url, params=params, headers=headers)
    data = res.json()

    if data["total"] == 0:
        return None

    item = data["items"][0]
    return {
        "title": item["title"],
        "address": item["address"],
        "roadAddress": item.get("roadAddress"),
    }


def search_local_restaurants(
    query: str,
    size: int = 5,
) -> List[Dict]:
    '''
    네이버 Local Search API를 사용해 주변의 음식점 검색
    '''

    url = 'https://openapi.naver.com/v1/search/local.json'

    headers = {
        "X-Naver-Client-Id": NAVER_ID,
        "X-Naver-Client-Secret": NAVER_SECRET,
    }

    params = {
        'query': query,
        'display': size,
        'sort': 'random',
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=5,
    )
    response.raise_for_status()

    data = response.json()

    results: List[Dict] = []

    for item in data.get('items', []):
        try:
            results.append({
                # 검색어 강조 표시 제거
                'name': item.get('title','').replace('<b>','').replace('</b>',''),
                'x': float(item.get('mapx')) / 1e7,
                'y': float(item.get('mapy')) / 1e7,
            })
        except (TypeError, ValueError):
            continue

    return results
