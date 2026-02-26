from __future__ import annotations

from typing import Dict

from backend.llm import llm
from backend.state import AgentState


def final_response_node(state: AgentState) -> Dict:
    """
    현재 선택된 추천 식당(selected_restaurant)을 기준으로 최종 응답을 생성합니다.
    """
    selected_restaurant = state.get("selected_restaurant") or {}
    nearest_station_name = selected_restaurant.get("nearest_station_name")
    nearest_station_distance_m = selected_restaurant.get("nearest_station_distance_m")
    estimated_walk_min = selected_restaurant.get("estimated_walk_min")

    if not selected_restaurant:
        return {
            "final_output": "추천 가능한 음식점 후보를 찾지 못했습니다. 조건을 바꿔 다시 요청해 주세요."
        }

    prompt = f"""
        너는 대중교통 경로 + 음식점 추천 비서다.
        아래 정보를 바탕으로 한국어로 최종 답변을 작성하라.
        정보가 비어 있으면 모른다고 솔직히 말하라.

        [입력 정보]
        - 출발지: {state.get('origin')}
        - 도착지: {state.get('destination')}
        - 선호 음식 종류: {state.get('restaurant_type')}
        - 도보 허용 시간(분): {state.get('walk_limit_min')}
        - 주 경로 예상 시간(분): {state.get('primary_route_time_min')}
        - 추천 음식점(현재): {selected_restaurant}
        - 추천 식당 기준 최단 도보 정거장: {nearest_station_name}
        - 정거장 기준 식당까지 거리(m): {nearest_station_distance_m}
        - 정거장 기준 식당까지 도보(분): {estimated_walk_min}

        [출력 규칙]
        1) 3~5문장으로 간결하게 작성
        2) 추천 음식점 이름 1개만 포함
        3) 추천 식당 이름, 이동 시간(있으면), 추천 이유를 반드시 포함
        4) "어느 정거장 기준으로 도보 몇 분인지"를 반드시 1문장으로 명시
        5) 정거장 정보가 없으면 "정거장 정보는 확인되지 않았습니다"라고 명시
    """

    try:
        response = llm.invoke(prompt)
        final_output = (response.content or "").strip()
        if not final_output:
            final_output = "추천 결과를 생성하지 못했습니다. 잠시 후 다시 시도해 주세요."
    except Exception as exc:
        final_output = f"최종 응답 생성 중 오류가 발생했습니다: {exc}"

    final_output = f"{final_output.rstrip()} 원하시면 다른 후보도 보여드릴게요."

    return {"final_output": final_output}
