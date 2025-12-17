from typing import TypedDict, Optional, List, Dict


class AgentState(TypedDict):
    # 유저 입력
    user_query: str

    # 파라미터 정보 (IntentNode가 채움)
    origin: Optional[str] = None
    destination: Optional[str] = None
    restaurant_type: Optional[str] = None
    walk_limit_min: Optional[int] = None

    # 좌표 정보
    origin_address: Optional[str] = None
    dest_address: Optional[str] = None
    origin_coord: Optional[Dict] = None
    dest_coord: Optional[Dict] = None

    # PrimaryRouteNode 결과
    primary_route_time_min: Optional[int] = None
    primary_route_points: Optional[List[Dict]] = None

    # 검색된 음식점 후보 리스트
    candidates: Optional[List[Dict]] = None

    # 각 음식점 후보의 경로 분석 결과
    route_details: Optional[List[Dict]] = None

    # 스코어 계산 후 최종 선택된 식당
    selected_restaurant: Optional[Dict] = None

    # 최종 LLM 응답
    final_output: Optional[str] = None