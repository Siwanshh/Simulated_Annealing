import random
import time

from tsp import route_distance


def nearest_neighbour(graph, start):
    started_at = time.perf_counter()

    unvisited = [city for city in graph if city != start]
    route = [start]
    current = start

    while unvisited:
        nearest = min(unvisited, key=lambda city: graph[current][city]["km"])
        route.append(nearest)
        unvisited.remove(nearest)
        current = nearest

    route.append(start)

    return {
        "name": "Greedy (Nearest Neighbour)",
        "route": route,
        "distance": route_distance(graph, route),
        "time": time.perf_counter() - started_at,
    }


def random_search(graph, start, trials=1000, seed=None):
    rng = random.Random(seed)
    started_at = time.perf_counter()

    others = [city for city in graph if city != start]

    best_route = None
    best_distance = float("inf")

    for _ in range(trials):
        rng.shuffle(others)
        route = [start] + others + [start]
        distance = route_distance(graph, route)

        if distance < best_distance:
            best_route = route
            best_distance = distance

    return {
        "name": "Random Search",
        "route": best_route,
        "distance": best_distance,
        "time": time.perf_counter() - started_at,
        "trials": trials,
        "seed": seed,
    }
