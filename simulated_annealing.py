import math
import random
import time

from tsp import random_route, route_distance, swap_two_cities


def simulated_annealing(
    graph,
    start,
    initial_temperature=100.0,
    cooling_rate=0.995,
    minimum_temperature=0.001,
    iterations_per_temperature=100,
    seed=None,
):
    rng = random.Random(seed)
    started_at = time.perf_counter()

    current_route = random_route(graph, start, rng)
    current_distance = route_distance(graph, current_route)

    best_route = list(current_route)
    best_distance = current_distance

    temperature = initial_temperature
    iteration = 0
    history = []

    while temperature > minimum_temperature:

        for _ in range(iterations_per_temperature):

            new_route = swap_two_cities(current_route, rng)
            new_distance = route_distance(graph, new_route)

            delta = new_distance - current_distance

            if delta < 0:
                current_route = new_route
                current_distance = new_distance
            else:
                probability = math.exp(-delta / temperature)

                if rng.random() < probability:
                    current_route = new_route
                    current_distance = new_distance

            if current_distance < best_distance:
                best_route = list(current_route)
                best_distance = current_distance

            iteration += 1

        history.append((iteration, current_distance, best_distance))

        temperature *= cooling_rate

    return {
        "name": "Simulated Annealing",
        "route": best_route,
        "distance": best_distance,
        "time": time.perf_counter() - started_at,
        "iterations": iteration,
        "seed": seed,
        "history": history,
    }


def run_many(graph, start, runs=30, base_seed=1, **settings):
    results = []

    for number in range(runs):
        results.append(simulated_annealing(graph, start, seed=base_seed + number, **settings))

    return results
