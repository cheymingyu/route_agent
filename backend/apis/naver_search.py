import requests
import os

from dotenv import load_dotenv
load_dotenv()

NAVER_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_SECRET = os.getenv("NAVER_CLIENT_SECRET")

def search_address(query: str):
    '''
    Docstring for search_address
    
    :param query: Description
    :type query: str
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