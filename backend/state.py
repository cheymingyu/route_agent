from typing import TypedDict, Optional, List, Dict


class AgentState(TypedDict):
    # 유저 입력
    user_query: str

    # 세션/사용자 액션
    session_id: Optional[str]
    last_user_action: Optional[str]

    # 파라미터 정보 (IntentNode가 채움)
    origin: Optional[str]
    destination: Optional[str]
    restaurant_type: Optional[str]
    walk_limit_min: Optional[int]

    # 좌표 정보
    origin_address: Optional[str]
    dest_address: Optional[str]
    origin_coord: Optional[Dict]
    dest_coord: Optional[Dict]

    # PrimaryRouteNode 결과
    primary_route_time_min: Optional[int]
    primary_route_points: Optional[List[Dict]]

    # 검색된 음식점 후보 리스트(스코어 정렬 반영)
    candidates: Optional[List[Dict]]
    candidate_cursor: Optional[int]
    rejected_candidate_ids: Optional[List[str]]
    remaining_candidates: Optional[int]

    # 각 음식점 후보의 경로 분석 결과
    route_details: Optional[List[Dict]]

    # 현재 선택된 식당
    selected_restaurant: Optional[Dict]

    # 최종 LLM 응답
    final_output: Optional[str]
