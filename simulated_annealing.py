

import json
import random
import math
import os
from build_graph import GRAPH_PATH, build_tsp_graph


if not os.path.exists(GRAPH_PATH):
    build_tsp_graph()

with open(GRAPH_PATH, "r") as f:
    graph = json.load(f)


cities = list(graph.keys())


def route_distance(route):
    total = 0.0

    for i in range(len(route) - 1):
        total += graph[route[i]][route[i + 1]]["km"]

    return total


def create_initial_route(start):
    remaining = [city for city in cities if city != start]
    random.shuffle(remaining)

    return [start] + remaining + [start]


def create_neighbor(route):
    new_route = route.copy()

    i, j = random.sample(
        range(1, len(route) - 1),
        2
    )

    new_route[i], new_route[j] = (
        new_route[j],
        new_route[i]
    )

    return new_route


def simulated_annealing(
    start,
    initial_temperature=100,
    cooling_rate=0.995,
    minimum_temperature=0.001,
    iterations_per_temperature=100
):

    current_route = create_initial_route(start)
    current_distance = route_distance(current_route)

    best_route = current_route.copy()
    best_distance = current_distance

    temperature = initial_temperature
    history = []

    while temperature > minimum_temperature:

        for _ in range(iterations_per_temperature):

            new_route = create_neighbor(current_route)
            new_distance = route_distance(new_route)

            delta = new_distance - current_distance

            if delta < 0:
                current_route = new_route
                current_distance = new_distance

            else:
                probability = math.exp(
                    -delta / temperature
                )

                if random.random() < probability:
                    current_route = new_route
                    current_distance = new_distance

            if current_distance < best_distance:
                best_route = current_route.copy()
                best_distance = current_distance

            history.append(best_distance)

        temperature *= cooling_rate

    return best_route, best_distance, history