import json
import math
import os
import random

from places import PLACES

GRAPH_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "OUTPUT", "tsp_graph.json")

PLACES_PATH = os.path.join(os.path.dirname(GRAPH_PATH), "tsp_places.json")

DEFAULT_START = "Kupondole"


def read_graph():
    if not os.path.exists(GRAPH_PATH):
        return None

    with open(GRAPH_PATH) as f:
        return json.load(f)


def read_saved_places():
    if not os.path.exists(PLACES_PATH):
        return None

    with open(PLACES_PATH) as f:
        return json.load(f)


def load_graph():
    graph = read_graph()
    used_places = {name: list(point) for name, point in PLACES.items()}

    if graph is None or read_saved_places() != used_places:
        from build_graph import build_tsp_graph

        print("The locations changed, requesting a new distance matrix...")
        build_tsp_graph()
        graph = read_graph()

    return graph


def route_distance(graph, route):
    total = 0.0

    for i in range(len(route) - 1):
        total += graph[route[i]][route[i + 1]]["km"]

    return total


def random_route(graph, start, rng):
    others = [city for city in graph if city != start]
    rng.shuffle(others)

    return [start] + others + [start]


def swap_two_cities(route, rng):
    new_route = list(route)
    i, j = rng.sample(range(1, len(route) - 1), 2)
    new_route[i], new_route[j] = new_route[j], new_route[i]

    return new_route


def is_valid_route(graph, route, start):
    if route[0] != start or route[-1] != start:
        return False

    return sorted(route[:-1]) == sorted(graph.keys())


def summarise_runs(results):
    distances = [result["distance"] for result in results]
    average = sum(distances) / len(distances)
    variance = sum((distance - average) ** 2 for distance in distances) / len(distances)

    return {
        "runs": len(results),
        "best": min(distances),
        "average": average,
        "worst": max(distances),
        "std": math.sqrt(variance),
        "average_time": sum(result["time"] for result in results) / len(results),
        "best_result": min(results, key=lambda result: result["distance"]),
    }


def choose_start(cities):
    print("Available locations:\n")

    for number, city in enumerate(cities, start=1):
        print("{:2}. {}".format(number, city))

    while True:
        try:
            answer = input("\nEnter starting location: ").strip()
        except EOFError:
            return DEFAULT_START

        if not answer:
            return DEFAULT_START

        if answer.isdigit() and 1 <= int(answer) <= len(cities):
            return cities[int(answer) - 1]

        for city in cities:
            if city.lower() == answer.lower():
                return city

        print("'{}' is not in the list, please try again.".format(answer))
