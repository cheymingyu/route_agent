from ..state import AgentState
from ..apis.odsay import fetch_pubtrans_route

def _select_fastest_path(response: dict) -> dict:
    # 응답에서 전체 시간 제일 짧은 경로 선택

    try:
        paths = response['result']['path']
    except KeyError:
        raise ValueError("path 정보가 반환되지 않았습니다.")

    if not paths:
        raise ValueError("경로 검색 결과가 없습니다.")
    
    try:
        fastest_path = min(
            paths,
            key=lambda x: x['info']['totalTime']
        )
    except KeyError:
        raise ValueError("totalTime 정보가 반환되지 않았습니다.")
    
    return fastest_path


def _extract_route_points(path: dict) -> list[dict]:

    route_points: list[dict] = []

    for sub_path in path.get('subPath', []):
        traffic_type = sub_path.get('trafficType')


        # 도보
        if traffic_type == 3:
            pass

        # 버스 or 지하철
        elif traffic_type in (1, 2):
            pass_stop_list = sub_path.get('passStopList')
            if not pass_stop_list:
                continue

            for station in pass_stop_list.get('stations', []):
                route_points.append({
                    'x': float(station['x']),
                    'y': float(station['y']),
                    'stationID': station.get('stationID'),
                    'stationName': station.get('stationName'),
                    'trafficType': traffic_type,
                })
    

    return route_points


def primary_route_node(state: AgentState) -> dict:

    if not state['origin_coord'] or not state['dest_coord']:
        raise ValueError("origin_coord 또는 dest_coord가 없습니다.")
    
    odsay_response = fetch_pubtrans_route(
        state['origin_coord'],
        state['dest_coord'],
    )

    fastest_path = _select_fastest_path(odsay_response)

    total_time = fastest_path['info']['totalTime']
    route_points = _extract_route_points(fastest_path)


    return {
        'primary_route_time_min': total_time,
        'primary_route_points': route_points,
    }

