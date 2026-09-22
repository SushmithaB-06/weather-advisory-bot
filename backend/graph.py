from langgraph.graph import StateGraph, START, END

from backend.state import WeatherBotState

from backend.nodes.location import extract_location_and_activity
from backend.nodes.weather import fetch_weather
from backend.nodes.weather_period import select_weather_period
from backend.nodes.sop_matcher import match_sop

from backend.nodes.response import (
    error_response,
    no_sop_response,
    advisory_response,
)


def route_after_intent(state: WeatherBotState):

    if state.get("error"):
        return "error"

    if not state.get("location"):
        return "error"

    return "weather"


def route_after_weather(state: WeatherBotState):

    if state.get("error"):
        return "error"

    if not state.get("weather"):
        return "error"

    return "select_period"


def route_after_sop(state: WeatherBotState):

    if state.get("error"):
        return "error"

    if not state.get("matched_sop"):
        return "no_sop"

    return "advisory"


def build_graph():

    graph = StateGraph(WeatherBotState)

    # -------------------------
    # Nodes
    # -------------------------

    graph.add_node(
        "extract_intent",
        extract_location_and_activity,
    )

    graph.add_node(
        "fetch_weather",
        fetch_weather,
    )

    graph.add_node(
        "select_weather_period",
        select_weather_period,
    )

    graph.add_node(
        "match_sop",
        match_sop,
    )

    graph.add_node(
        "error_response",
        error_response,
    )

    graph.add_node(
        "no_sop_response",
        no_sop_response,
    )

    graph.add_node(
        "advisory_response",
        advisory_response,
    )

    # -------------------------
    # Start
    # -------------------------

    graph.add_edge(
        START,
        "extract_intent",
    )

    # -------------------------
    # Intent routing
    # -------------------------

    graph.add_conditional_edges(
        "extract_intent",
        route_after_intent,
        {
            "error": "error_response",
            "weather": "fetch_weather",
        },
    )

    # -------------------------
    # Weather routing
    # -------------------------

    graph.add_conditional_edges(
        "fetch_weather",
        route_after_weather,
        {
            "error": "error_response",
            "select_period": "select_weather_period",
        },
    )

    # -------------------------
    # Weather period
    # -------------------------

    graph.add_edge(
        "select_weather_period",
        "match_sop",
    )

    # -------------------------
    # SOP routing
    # -------------------------

    graph.add_conditional_edges(
        "match_sop",
        route_after_sop,
        {
            "error": "error_response",
            "no_sop": "no_sop_response",
            "advisory": "advisory_response",
        },
    )

    # -------------------------
    # End nodes
    # -------------------------

    graph.add_edge(
        "error_response",
        END,
    )

    graph.add_edge(
        "no_sop_response",
        END,
    )

    graph.add_edge(
        "advisory_response",
        END,
    )

    return graph.compile()


weather_graph = build_graph()