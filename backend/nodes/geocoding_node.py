from state import AgentState
from apis.naver_map import geocode

def geocoding_node(state: AgentState):
    if state.origin:
        state.origin_coord = geocode(state.origin_address)

    if state.destination:
        state.dest_coord = geocode(state.dest_address)

    return state