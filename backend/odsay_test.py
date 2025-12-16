import os
import requests
from urllib.parse import urlencode

from dotenv import load_dotenv
load_dotenv()

# 환경변수에서 API 키 읽기
ODSAY_API_KEY = '+2rtnbOSX6ODEwPMZ5dN0oMyra7/+PPnkxehONcph+8'

def test_odsay_route():
    params = {
        "SX": 126.9027279,
        "SY": 37.5349277,
        "EX": 126.9145430,
        "EY": 37.5499421,
        "apiKey": ODSAY_API_KEY
    }

    url = "https://api.odsay.com/v1/api/searchPubTransPathT?" + urlencode(params)

    response = requests.get(url)

    print(url)

    print("Status:", response.status_code)
    print("Response JSON:")
    print(response.json())

if __name__ == "__main__":
    test_odsay_route()
