from fastapi import FastAPI
import requests
import os
from urllib.parse import urlencode
from dotenv import load_dotenv
from state import AgentState
from graph import agent


app = FastAPI()

load_dotenv()
ODSAY_API_KEY = os.getenv("ODSAY_API_KEY")  # .env에 넣어둬도 됨
NAVER_MAPS_ID = os.getenv("NAVER_MAPS_CLIENT_ID")
NAVER_MAPS_SECRET = os.getenv("NAVER_MAPS_CLIENT_SECRET")
NAVER_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_SECRET = os.getenv("NAVER_CLIENT_SECRET")


@app.get("/route-test")
def route_test():
    params = {
        "SX": 126.9027279,
        "SY": 37.5349277,
        "EX": 126.9145430,
        "EY": 37.5499421,
        "apiKey": ODSAY_API_KEY
    }

    url = "https://api.odsay.com/v1/api/searchPubTransPathT?" + urlencode(params)

    response = requests.get(url)
    return response.json()

@app.post("/search-test")
def test_naver(payload: dict):
    keyword = payload['text']
    url = "https://openapi.naver.com/v1/search/local.json"
    
    headers = {
        "X-Naver-Client-Id": NAVER_ID,
        "X-Naver-Client-Secret": NAVER_SECRET
    }

    params = {
        "query": keyword,
        "display": 10,
        "sort": "random" 
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

@app.post("/geo-test")
def naver_test(payload: dict):
    user_input = payload['text']
    url = "https://maps.apigw.ntruss.com/map-geocode/v2/geocode"
    params = {'query': user_input}

    headers = {
        'x-ncp-apigw-api-key-id': NAVER_MAPS_ID,
        'x-ncp-apigw-api-key': NAVER_MAPS_SECRET,
        'Accept': "application/json",
    }

    res = requests.get(url, params=params, headers=headers)
    data = res.json()

    return data


@app.post("/agent-test")
def run_agent(payload: dict):
    user_input = payload['text']
    init_state = AgentState(user_query=user_input)

    # LangGraph 실행
    result: AgentState = agent.invoke(init_state)

    return result
