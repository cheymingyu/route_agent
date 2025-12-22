from ..state import AgentState
from ..apis.naver_search import search_address

def place_resolve_node(state: AgentState):
    if state['origin']:
        place = search_address(state['origin'])
        if place:
            origin_address = place['address']
        else:
            origin_address = state['origin']
    

    if state['destination']:
        place = search_address(state['destination'])
        if place:
            dest_address = place['address']
        else:
            dest_address = state['destination']

    return {'origin_address': origin_address, 'dest_address': dest_address}
