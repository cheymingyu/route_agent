from __future__ import annotations

from typing import Dict, List

from backend.state import AgentState


def feedback_node(state: AgentState) -> Dict:
    """
    사용자 피드백(next/accept 등)에 따라 후보 선택 상태를 갱신합니다.
    현재는 next 액션만 처리합니다.
    """
    action = state.get("last_user_action")
    if action != "next":
        return {}

    selected = state.get("selected_restaurant") or {}
    selected_candidate_id = selected.get("candidate_id")

    rejected: List[str] = list(state.get("rejected_candidate_ids") or [])
    if selected_candidate_id and selected_candidate_id not in rejected:
        rejected.append(selected_candidate_id)

    current_cursor = int(state.get("candidate_cursor") or 0)
    return {
        "rejected_candidate_ids": rejected,
        "candidate_cursor": current_cursor + 1,
    }

