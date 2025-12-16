from state import AgentState
from apis.naver_address_search import search_place

def place_resolve_node(state: AgentState):
    if state.origin:
        place = search_place(state.origin)
        if place:
            state.origin_address = place['address']
        else:
            state.origin_address = state.origin
    

    if state.destination:
        place = search_place(state.destination)
        if place:
            state.dest_address = place['address']
        else:
            state.dest_address = state.destination

    return state