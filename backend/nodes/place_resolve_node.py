from state import AgentState
from apis.naver_address_search import search_place

def place_resolve_node(state: AgentState):
    if state['origin']:
        place = search_place(state['origin'])
        if place:
            origin_address = place['address']
        else:
            origin_address = state['origin']
    

    if state['destination']:
        place = search_place(state['destination'])
        if place:
            dest_address = place['address']
        else:
            dest_address = state['destination']

    return {'origin_address': origin_address, 'dest_address': dest_address}
