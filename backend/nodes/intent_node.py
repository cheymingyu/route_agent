from schemas import IntentSchema
from state import AgentState
from llm import llm
from parsers import parser, format_instructions


def intent_node(state: AgentState):
    user_input = state['user_query']

    prompt = f"""
        반드시 아래 JSON 스키마 형식 그대로 출력하세요:

         - 출발지(origin)
         - 도착지(destination)
         - 식당 종류(restaurant_type)
         - 도보 허용 시간(walk_limit_min)

        {format_instructions}

        사용자 입력:
        {user_input}

    """

    response = llm.invoke(prompt)

    try:
        parsed = parser.parse(response.content)
    except Exception as e:
        print(f"Parsing error: {e}")
        parsed = IntentSchema()

    state['origin'] = parsed.origin
    state['destination'] = parsed.destination
    state['restaurant_type'] = parsed.restaurant_type
    state['walk_limit_min'] = parsed.walk_limit_min

    return {
        'origin': state['origin'],
        'destination': state['destination'],
        'restaurant_type': state['restaurant_type'],
        'walk_limit_min': state['walk_limit_min'],
    }
