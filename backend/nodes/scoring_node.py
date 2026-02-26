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


def _min_distance_to_route(candidate: Dict, route_points: List[Dict]) -> Tuple[float, Optional[Dict]]:
    min_distance = float("inf")
    nearest_station: Optional[Dict] = None

    for point in route_points:
        if point.get("x") is None or point.get("y") is None:
            continue
        d = _euclidean_distance_m(candidate, point)
        if d < min_distance:
            min_distance = d
            nearest_station = point
    return min_distance, nearest_station


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
    distance_m, nearest_station = _min_distance_to_route(candidate, route_points)
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
            "nearest_station_name": (nearest_station or {}).get("stationName"),
            "nearest_station_id": (nearest_station or {}).get("stationID"),
            "nearest_station_coord": {
                "x": (nearest_station or {}).get("x"),
                "y": (nearest_station or {}).get("y"),
            } if nearest_station else None,
            "nearest_station_distance_m": round(distance_m, 1) if distance_m != float("inf") else None,
            "estimated_walk_min": walk_min,
            "distance_score": round(distance_score, 2),
            "type_score": round(type_score, 2),
            "walk_penalty": round(walk_penalty, 2),
            "total_score": round(total_score, 2),
        }
    )
    return scored


def scoring_node(state: AgentState) -> Dict:
    """
    후보 음식점을 점수 계산 후 정렬만 수행합니다.

    반환:
    - candidates: 점수 포함 후보 리스트(내림차순)
    - route_details: 점수 포함 후보 리스트(디버깅/로깅용)
    - candidate_cursor: 첫 추천 인덱스(0)
    """
    candidates = state.get("candidates") or []
    route_points = state.get("primary_route_points") or []

    if not candidates:
        return {
            "candidates": [],
            "route_details": [],
            "candidate_cursor": 0,
        }

    if not route_points:
        fallback_scored = []
        for c in candidates:
            t_score = _type_score(c.get("name", ""), state.get("restaurant_type"))
            scored = dict(c)
            scored.update(
                {
                    "distance_m": None,
                    "nearest_station_name": None,
                    "nearest_station_id": None,
                    "nearest_station_coord": None,
                    "nearest_station_distance_m": None,
                    "estimated_walk_min": None,
                    "distance_score": 0.0,
                    "type_score": round(t_score, 2),
                    "walk_penalty": 0.0,
                    "total_score": round(t_score, 2),
                }
            )
            fallback_scored.append(scored)

        fallback_scored.sort(key=lambda x: x["total_score"], reverse=True)
        return {
            "candidates": fallback_scored,
            "route_details": fallback_scored,
            "candidate_cursor": 0,
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

    return {
        "candidates": scored_candidates,
        "route_details": scored_candidates,
        "candidate_cursor": 0,
    }
