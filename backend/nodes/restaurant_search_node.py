from typing import Dict, List, Set, Tuple

from backend.state import AgentState
from backend.apis.naver_search import search_local_restaurants
from backend.utils.spot_search_points import build_restaurant_search_spots


def _restaurant_key(item: Dict) -> Tuple:
    '''
    음식점 중복 제거 기준 생성
    이름 + 좌표
    '''
    return(
        item.get('name'),
        round(item.get('x', 0), 6),
        round(item.get('y', 0), 6)
    )


def restaurant_search_node(state: AgentState) -> dict:
    '''
    경로 상의 음식점 탐색
    사용자에게 추천할 음식점 후보 리스트를 반환
    '''

    if not state['primary_route_points']:
        raise ValueError('primary_route_points가 없습니다.')
    
    # 1. 음식점 탐색할 스팟 생성
    search_spots = build_restaurant_search_spots(
        route_points=state['primary_route_points'],
        interval=3,
    )

    candidates: List[Dict] = []
    seen: Set[Tuple] = set()

    # print(search_spots)

    # 2. 각 스팟에서 음식점 탐색
    for spot in search_spots:
        station_name = spot.get('stationName')
        if not station_name:
            continue

        query = f"{station_name} 주변 {state['restaurant_type'] or '음식점'}"

        results = search_local_restaurants(
            query=query,
            size=5,
        )

        for r in results:
            candidate = {
                'name': r.get('name'),
                'x': r.get('x'),
                'y': r.get('y'),
            }

            key = _restaurant_key(candidate)
            if key in seen:
                continue

            seen.add(key)
            candidates.append(candidate)
    

    return {
        'candidates': candidates,
    }