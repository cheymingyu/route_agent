from typing import List, Dict


def extract_transfer_points(
        route_points: List[Dict]
) -> List[Dict]:
    # 환승구역 추출

    transfer_points: List[Dict] = []

    prev_type = None

    for point in route_points:
        current_type = point.get('trafficType')

        if current_type == 3:
            pass
        elif prev_type is not None and current_type != prev_type:
            transfer_points.append({
                'x': point['x'],
                'y': point['y'],
                'stationID': point.get('stationID'),
                'stationName': point.get('stationName'),
                'spot': 'transfer',
            })
        
        prev_type = current_type

    return transfer_points


def extract_interval_points(
        route_points: List[Dict],
        interval: int = 3,
) -> List[Dict]:
    # 전체 경로에서 interval마다 지점 추출

    interval_points: List[Dict] = []

    station_points = [
        p for p in route_points
        if p.get('stationID') is not None
    ]

    for idx in range(0, len(station_points), interval):
        point = station_points[idx]
        interval_points.append({
            'x': point['x'],
            'y': point['y'],
            'stationID': point.get('stationID'),
            'stationName': point.get('stationName'),
            'spot': 'interval',
        })

    # 마지막 지점 추가
    last = station_points[-1]
    if interval_points:
        last_added = interval_points[-1]
        if last_added['stationID'] != last.get('stationID'):
            interval_points.pop()
            interval_points.append({
            'x': point['x'],
            'y': point['y'],
            'stationID': point.get('stationID'),
            'stationName': point.get('stationName'),
            'spot': 'interval',
        })

    return interval_points


def build_restaurant_search_spots(
        route_points: List[Dict],
        interval: int = 3,
) -> List[Dict]:
    
    transfer_spots = extract_transfer_points(route_points)
    interval_spots = extract_interval_points(route_points, interval)

    merged = transfer_spots + interval_spots

    unique = {}
    for p in merged:
        key = (round(p['x'], 6), round(p['y'], 6))
        unique[key] = p

    return list(unique.values())
