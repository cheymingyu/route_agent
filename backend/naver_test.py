from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv

load_dotenv()

NAVER_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_SECRET = os.getenv("NAVER_CLIENT_SECRET")

app = FastAPI()

@app.get("/test/naver")
def test_naver(keyword: str = "텐동"):
    url = "https://openapi.naver.com/v1/search/local.json"
    
    headers = {
        "X-Naver-Client-Id": NAVER_ID,
        "X-Naver-Client-Secret": NAVER_SECRET
    }

    params = {
        "query": keyword,
        "display": 10,
        "sort": "comment"   # 리뷰 많은 순
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()