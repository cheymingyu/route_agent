from __future__ import annotations

from typing import Dict, List

from backend.state import AgentState


def _candidate_id(candidate: Dict) -> str:
    """후보 식당 식별자 생성/보정"""
    candidate_id = candidate.get("candidate_id")
    if candidate_id:
        return str(candidate_id)

    name = candidate.get("name") or "unknown"
    x = candidate.get("x")
    y = candidate.get("y")
    return f"{name}:{x}:{y}"


def select_candidate_node(state: AgentState) -> Dict:
    candidates: List[Dict] = list(state.get("candidates") or [])
    rejected_ids = set(state.get("rejected_candidate_ids") or [])
    cursor = int(state.get("candidate_cursor") or 0)

    if not candidates:
        return {
            "selected_restaurant": None,
            "candidate_cursor": 0,
            "remaining_candidates": 0,
        }

    # 후보마다 식별자를 보정해 이후 재선택/거절 추적 기준으로 사용
    for candidate in candidates:
        candidate["candidate_id"] = _candidate_id(candidate)

    selected = None
    selected_index = None

    for idx in range(max(cursor, 0), len(candidates)):
        candidate = candidates[idx]
        if candidate["candidate_id"] in rejected_ids:
            continue
        selected = candidate
        selected_index = idx
        break

    if selected is None:
        return {
            "candidates": candidates,
            "selected_restaurant": None,
            "remaining_candidates": 0,
        }

    remaining = 0
    for idx in range(selected_index + 1, len(candidates)):
        if candidates[idx]["candidate_id"] not in rejected_ids:
            remaining += 1

    return {
        "candidates": candidates,
        "selected_restaurant": selected,
        "candidate_cursor": selected_index,
        "remaining_candidates": remaining,
    }
