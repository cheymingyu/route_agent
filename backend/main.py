from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from uuid import uuid4
from urllib.parse import urlencode
from dotenv import load_dotenv
from .state import AgentState
from .graph import agent, feedback_agent


app = FastAPI()
SESSION_STORE: dict[str, AgentState] = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
ODSAY_API_KEY = os.getenv("ODSAY_API_KEY")  # .env에 넣어둬도 됨
NAVER_MAPS_ID = os.getenv("NAVER_MAPS_CLIENT_ID")
NAVER_MAPS_SECRET = os.getenv("NAVER_MAPS_CLIENT_SECRET")
NAVER_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_SECRET = os.getenv("NAVER_CLIENT_SECRET")


@app.get("/route-test")
def route_test():
    params = {
        "SX": 127.4330095,
        "SY": 36.3324875,
        "EX": 127.3442841,
        "EY": 36.369606,
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


@app.post("/chat/start")
def chat_start(payload: dict):
    user_input = payload.get("text")
    if not user_input:
        raise HTTPException(status_code=400, detail="text는 필수입니다.")

    session_id = str(uuid4())
    init_state = AgentState(
        user_query=user_input,
        session_id=session_id,
        last_user_action="restart",
        rejected_candidate_ids=[],
        candidate_cursor=0,
    )

    result: AgentState = agent.invoke(init_state)
    SESSION_STORE[session_id] = result

    return {
        "session_id": session_id,
        "final_output": result.get("final_output"),
        "selected_restaurant": result.get("selected_restaurant"),
        "remaining_candidates": result.get("remaining_candidates"),
    }


@app.post("/chat/next")
def chat_next(payload: dict):
    session_id = payload.get("session_id")
    if not session_id:
        raise HTTPException(status_code=400, detail="session_id는 필수입니다.")

    prev_state = SESSION_STORE.get(session_id)
    if not prev_state:
        raise HTTPException(status_code=404, detail="세션이 만료되었거나 존재하지 않습니다.")

    next_input = dict(prev_state)
    next_input["last_user_action"] = "next"
    next_input["session_id"] = session_id

    result: AgentState = feedback_agent.invoke(next_input)
    SESSION_STORE[session_id] = result

    exhausted = result.get("selected_restaurant") is None
    return {
        "session_id": session_id,
        "exhausted": exhausted,
        "final_output": result.get("final_output"),
        "selected_restaurant": result.get("selected_restaurant"),
        "remaining_candidates": result.get("remaining_candidates"),
    }
