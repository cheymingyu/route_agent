from ..state import AgentState
from ..apis.naver_map import geocode

def geocoding_node(state: AgentState):
    if state['origin']:
        origin_coord = geocode(state['origin_address'])

    if state['destination']:
        dest_coord = geocode(state['dest_address'])

    return {
        'origin_coord': origin_coord,
        'dest_coord': dest_coord,
    }
