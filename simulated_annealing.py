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
    iterations_per_temperature=100,
    runs=30
):
    overall_best_route = None
    overall_best_distance = float("inf")
    overall_best_history = None

    run_results = []

    for i in range(runs):

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

        # Store this run's result
        run_results.append({
            "run": i + 1,
            "best_route": best_route,
            "best_distance_km": round(best_distance, 2)
        })

        print(
            f"Run {i + 1}/{runs}: "
            f"{best_distance:.2f} km"
        )

        # Keep the best result among all runs
        if best_distance < overall_best_distance:
            overall_best_route = best_route.copy()
            overall_best_distance = best_distance
            overall_best_history = history

    # Save all run results
    output_dir = os.path.join(
        os.path.dirname(GRAPH_PATH)
    )

    os.makedirs(output_dir, exist_ok=True)

    results_path = os.path.join(
        output_dir,
        "sa_runs.json"
    )

    with open(results_path, "w") as f:
        json.dump(
            run_results,
            f,
            indent=2
        )

    print(
        f"\nAll run results saved to: "
        f"{results_path}"
    )

    print(
        f"Overall best distance: "
        f"{overall_best_distance:.2f} km"
    )

    print(
        "Overall best route: "
        + " → ".join(overall_best_route)
    )

    return (
        overall_best_route,
        overall_best_distance,
        overall_best_history
    )