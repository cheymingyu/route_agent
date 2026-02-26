from langgraph.graph import StateGraph
from .state import AgentState
from .nodes import (
    intent_node,
    place_resolve_node,
    geocoding_node,
    primary_route_node,
    restaurant_search_node,
    scoring_node,
    feedback_node,
    select_candidate_node,
    final_response_node,
)


graph = StateGraph(AgentState)

# 노드 등록
graph.add_node('intent', intent_node)
graph.add_node('place_resolve', place_resolve_node)
graph.add_node('geocoding', geocoding_node)
graph.add_node('primary_route', primary_route_node)
graph.add_node('restaurant_search', restaurant_search_node)
graph.add_node('scoring', scoring_node)
graph.add_node('select_candidate', select_candidate_node)
graph.add_node('final_response', final_response_node)


# 엣지 추가
graph.add_edge('intent', 'place_resolve')
graph.add_edge('place_resolve', 'geocoding')
graph.add_edge('geocoding', 'primary_route')
graph.add_edge('primary_route', 'restaurant_search')
graph.add_edge('restaurant_search', 'scoring')
graph.add_edge('scoring', 'select_candidate')
graph.add_edge('select_candidate', 'final_response')


# 진입 지점 설정
graph.set_entry_point('intent')

# 컴파일된 Agent
agent = graph.compile()


feedback_graph = StateGraph(AgentState)
feedback_graph.add_node("feedback", feedback_node)
feedback_graph.add_node("select_candidate", select_candidate_node)
feedback_graph.add_node("final_response", final_response_node)
feedback_graph.add_edge("feedback", "select_candidate")
feedback_graph.add_edge("select_candidate", "final_response")
feedback_graph.set_entry_point("feedback")

# 후속 피드백(next) 처리 전용 Agent
feedback_agent = feedback_graph.compile()
