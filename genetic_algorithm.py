import random
import time

from tsp import random_route, route_distance, swap_two_cities


def tournament_selection(population, distances, rng, tournament_size):
    best = rng.randrange(len(population))

    for _ in range(tournament_size - 1):
        challenger = rng.randrange(len(population))

        if distances[challenger] < distances[best]:
            best = challenger

    return population[best]


def order_crossover(parent_one, parent_two, rng):
    start = parent_one[0]
    middle_one = parent_one[1:-1]
    middle_two = parent_two[1:-1]
    size = len(middle_one)

    left, right = sorted(rng.sample(range(size), 2))

    child_middle = [None] * size
    child_middle[left:right + 1] = middle_one[left:right + 1]

    taken = set(middle_one[left:right + 1])
    position = (right + 1) % size

    for offset in range(size):
        city = middle_two[(right + 1 + offset) % size]

        if city not in taken:
            child_middle[position] = city
            position = (position + 1) % size

    return [start] + child_middle + [start]


def genetic_algorithm(
    graph,
    start,
    population_size=40,
    generations=200,
    mutation_rate=0.1,
    tournament_size=3,
    seed=None,
):
    rng = random.Random(seed)
    started_at = time.perf_counter()

    population = [random_route(graph, start, rng) for _ in range(population_size)]
    distances = [route_distance(graph, route) for route in population]

    best_index = min(range(population_size), key=lambda index: distances[index])
    best_route = list(population[best_index])
    best_distance = distances[best_index]

    history = [best_distance]

    for _ in range(generations):

        new_population = [list(best_route)]

        while len(new_population) < population_size:
            parent_one = tournament_selection(population, distances, rng, tournament_size)
            parent_two = tournament_selection(population, distances, rng, tournament_size)

            child = order_crossover(parent_one, parent_two, rng)

            if rng.random() < mutation_rate:
                child = swap_two_cities(child, rng)

            new_population.append(child)

        population = new_population
        distances = [route_distance(graph, route) for route in population]

        best_index = min(range(population_size), key=lambda index: distances[index])

        if distances[best_index] < best_distance:
            best_route = list(population[best_index])
            best_distance = distances[best_index]

        history.append(best_distance)

    return {
        "name": "Genetic Algorithm",
        "route": best_route,
        "distance": best_distance,
        "time": time.perf_counter() - started_at,
        "generations": generations,
        "seed": seed,
        "history": history,
    }
