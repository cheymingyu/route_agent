from __future__ import annotations

from math import cos, radians, sqrt
from typing import Dict, List, Optional, Tuple

from backend.state import AgentState


def _euclidean_distance_m(p1: Dict, p2: Dict) -> float:
    """
    경도/위도 좌표 간 근사 거리(m)를 계산합니다.
    짧은 거리 비교용으로 충분한 equirectangular 근사 방식입니다.
    """
    x1, y1 = p1.get("x"), p1.get("y")
    x2, y2 = p2.get("x"), p2.get("y")

    if x1 is None or y1 is None or x2 is None or y2 is None:
        return float("inf")

    lat_avg = radians((float(y1) + float(y2)) / 2.0)
    dx = (float(x2) - float(x1)) * 111_320.0 * cos(lat_avg)
    dy = (float(y2) - float(y1)) * 110_540.0
    return sqrt(dx * dx + dy * dy)


def _min_distance_to_route(candidate: Dict, route_points: List[Dict]) -> float:
    min_distance = float("inf")
    for point in route_points:
        if point.get("x") is None or point.get("y") is None:
            continue
        d = _euclidean_distance_m(candidate, point)
        if d < min_distance:
            min_distance = d
    return min_distance


def _distance_score(distance_m: float) -> float:
    """
    거리 점수(0~100): 0m=100, 1000m 이상=0
    """
    if distance_m == float("inf"):
        return 0.0
    return max(0.0, 100.0 - (distance_m / 10.0))


def _type_score(candidate_name: str, restaurant_type: Optional[str]) -> float:
    """
    단순 키워드 포함 기반 타입 점수(0 또는 100)
    """
    if not restaurant_type:
        return 50.0

    if restaurant_type.strip().lower() in candidate_name.lower():
        return 100.0

    return 0.0


def _estimate_walk_minutes(distance_m: float) -> int:
    """
    보행 속도 4.0km/h 기준 대략 도보 시간(분) 추정
    """
    if distance_m == float("inf"):
        return 999
    meters_per_min = 4000 / 60
    return int(round(distance_m / meters_per_min))


def _score_candidate(
    candidate: Dict,
    route_points: List[Dict],
    restaurant_type: Optional[str],
    walk_limit_min: Optional[int],
) -> Dict:
    distance_m = _min_distance_to_route(candidate, route_points)
    distance_score = _distance_score(distance_m)
    type_score = _type_score(candidate.get("name", ""), restaurant_type)

    walk_min = _estimate_walk_minutes(distance_m)
    effective_walk_limit = walk_limit_min if walk_limit_min is not None else 15
    walk_penalty = 0.0 if walk_min <= effective_walk_limit else min(30.0, (walk_min - effective_walk_limit) * 2.0)

    total_score = (distance_score * 0.7) + (type_score * 0.3) - walk_penalty

    scored = dict(candidate)
    scored.update(
        {
            "distance_m": round(distance_m, 1) if distance_m != float("inf") else None,
            "estimated_walk_min": walk_min,
            "distance_score": round(distance_score, 2),
            "type_score": round(type_score, 2),
            "walk_penalty": round(walk_penalty, 2),
            "total_score": round(total_score, 2),
        }
    )
    return scored


def _build_reason(best: Dict, restaurant_type: Optional[str]) -> str:
    name = best.get("name", "알 수 없는 식당")
    distance = best.get("distance_m")
    walk_min = best.get("estimated_walk_min")

    reason_parts = [f"{name}가 경로에서 가장 접근성이 좋았습니다"]
    if distance is not None:
        reason_parts.append(f"(최소 거리 약 {distance}m)")
    if walk_min is not None:
        reason_parts.append(f"도보 약 {walk_min}분")
    if restaurant_type:
        reason_parts.append(f"요청한 '{restaurant_type}' 조건을 우선 반영했습니다")

    return ", ".join(reason_parts) + "."


def scoring_node(state: AgentState) -> Dict:
    """
    후보 음식점 점수 계산 후 최종 추천 1개를 선택합니다.

    반환:
    - route_details: 점수 포함 후보 리스트(내림차순)
    - selected_restaurant: 최고점 후보 1개
    """
    candidates = state.get("candidates") or []
    route_points = state.get("primary_route_points") or []

    if not candidates:
        return {
            "route_details": [],
            "selected_restaurant": None,
        }

    if not route_points:
        # 경로 포인트가 없으면 타입 점수 기반으로만 선택
        fallback_scored = []
        for c in candidates:
            t_score = _type_score(c.get("name", ""), state.get("restaurant_type"))
            scored = dict(c)
            scored.update(
                {
                    "distance_m": None,
                    "estimated_walk_min": None,
                    "distance_score": 0.0,
                    "type_score": round(t_score, 2),
                    "walk_penalty": 0.0,
                    "total_score": round(t_score, 2),
                }
            )
            fallback_scored.append(scored)

        fallback_scored.sort(key=lambda x: x["total_score"], reverse=True)
        best = fallback_scored[0]
        best["score_reason"] = _build_reason(best, state.get("restaurant_type"))

        return {
            "route_details": fallback_scored,
            "selected_restaurant": best,
        }

    scored_candidates: List[Dict] = []
    for candidate in candidates:
        scored_candidates.append(
            _score_candidate(
                candidate=candidate,
                route_points=route_points,
                restaurant_type=state.get("restaurant_type"),
                walk_limit_min=state.get("walk_limit_min"),
            )
        )

    scored_candidates.sort(key=lambda x: x["total_score"], reverse=True)
    best_candidate = scored_candidates[0]
    best_candidate["score_reason"] = _build_reason(best_candidate, state.get("restaurant_type"))

    return {
        "route_details": scored_candidates,
        "selected_restaurant": best_candidate,
    }
