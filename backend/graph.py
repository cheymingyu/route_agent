from langgraph.graph import StateGraph
from .state import AgentState
from .nodes import (
    intent_node,
    place_resolve_node,
    geocoding_node,
    primary_route_node,
    restaurant_search_node,
)


graph = StateGraph(AgentState)

# 노드 등록
graph.add_node('intent', intent_node)
graph.add_node('place_resolve', place_resolve_node)
graph.add_node('geocoding', geocoding_node)
graph.add_node('primary_route', primary_route_node)
graph.add_node('restaurant_search', restaurant_search_node)


# 엣지 추가
graph.add_edge('intent', 'place_resolve')
graph.add_edge('place_resolve', 'geocoding')
graph.add_edge('geocoding', 'primary_route')
graph.add_edge('primary_route', 'restaurant_search')


# 진입 지점 설정
graph.set_entry_point('intent')

# 컴파일된 Agent
agent = graph.compile()
