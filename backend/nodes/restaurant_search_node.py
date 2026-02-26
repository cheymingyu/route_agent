from typing import Dict, List, Set, Tuple

from backend.state import AgentState
from backend.apis.naver_search import search_local_restaurants
from backend.apis.naver_map import reverse_geocode
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


def _build_query_with_region(spot: Dict, restaurant_type: str) -> str:
    station_name = spot.get('stationName')
    if not station_name:
        return ""

    query_prefix = ""
    x = spot.get("x")
    y = spot.get("y")

    if x is not None and y is not None:
        try:
            region = reverse_geocode(float(x), float(y))
            if region:
                query_prefix = region.get("area2") or region.get("area1") or ""
        except Exception:
            query_prefix = ""

    if query_prefix:
        return f"{query_prefix} {station_name} 주변 {restaurant_type}"
    return f"{station_name} 주변 {restaurant_type}"


def restaurant_search_node(state: AgentState) -> dict:
    '''
    경로 상의 음식점 탐색
    사용자에게 추천할 음식점 후보 리스트를 반환
    '''

    # 이미 후보가 있으면 재검색하지 않음
    existing = state.get('candidates') or []
    if existing:
        return {
            'candidates': existing,
        }

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

        query = _build_query_with_region(
            spot=spot,
            restaurant_type=state['restaurant_type'] or '음식점',
        )
        if not query:
            continue

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
