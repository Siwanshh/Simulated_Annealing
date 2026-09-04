import matplotlib.pyplot as plt

from baselines import nearest_neighbour, random_search
from genetic_algorithm import genetic_algorithm
from plots import plot_comparison, plot_cooling_rates, plot_ga_convergence
from simulated_annealing import run_many
from tsp import choose_start, load_graph, summarise_runs

SA_RUNS = 30
GA_RUNS = 10
RANDOM_TRIALS = 1000
COOLING_RATES = [0.95, 0.99, 0.995, 0.999]
COOLING_RUNS = 5


def ask_yes_no(question):
    try:
        answer = input(question).strip().lower()
    except EOFError:
        return False

    return answer in ("y", "yes")


def print_stats(summary):
    print("  best     {:.2f} km".format(summary["best"]))
    print("  average  {:.2f} km".format(summary["average"]))
    print("  worst    {:.2f} km".format(summary["worst"]))
    print("  std dev  {:.2f} km".format(summary["std"]))
    print("  time     {:.4f} sec per run".format(summary["average_time"]))


def print_table(rows):
    print("\n" + "-" * 60)
    print("Comparison")
    print("-" * 60)
    print("{:<28}{:<8}{:<14}{}".format("Algorithm", "Runs", "Distance", "Time per run"))

    for row in rows:
        print("{:<28}{:<8}{:<14}{}".format(
            row["name"],
            row["runs"],
            "{:.2f} km".format(row["distance"]),
            "{:.5f} sec".format(row["time"]),
        ))


def cooling_rate_experiment(graph, start):
    print("\nTesting different cooling rates ({} runs each)...".format(COOLING_RUNS))

    averages = []

    for rate in COOLING_RATES:
        results = run_many(graph, start, runs=COOLING_RUNS, cooling_rate=rate)
        summary = summarise_runs(results)
        averages.append(summary["average"])

        print("  cooling rate {:<7} average {:.2f} km   best {:.2f} km   {:.2f} sec per run".format(
            rate, summary["average"], summary["best"], summary["average_time"]
        ))

    return averages


def main():
    print("=" * 40)
    print("Kathmandu TSP")
    print("Algorithm comparison")
    print("=" * 40)
    print()

    print("Loading Kathmandu road distances...\n")
    graph = load_graph()
    cities = list(graph)

    start = choose_start(cities)
    print("\nStarting location: {}".format(start))
    print("All algorithms use the same locations, the same distance matrix and the same start.\n")

    print("Running Simulated Annealing ({} runs)...".format(SA_RUNS))
    sa_results = run_many(graph, start, runs=SA_RUNS)
    sa = summarise_runs(sa_results)
    print_stats(sa)

    print("\nRunning Greedy Nearest Neighbour...")
    greedy = nearest_neighbour(graph, start)
    print("  distance {:.2f} km".format(greedy["distance"]))

    print("\nRunning Random Search ({} random routes)...".format(RANDOM_TRIALS))
    random_result = random_search(graph, start, trials=RANDOM_TRIALS, seed=1)
    print("  distance {:.2f} km".format(random_result["distance"]))

    print("\nRunning Genetic Algorithm ({} runs)...".format(GA_RUNS))
    ga_results = [genetic_algorithm(graph, start, seed=seed) for seed in range(1, GA_RUNS + 1)]
    ga = summarise_runs(ga_results)
    ga_best = ga["best_result"]
    print_stats(ga)

    print_table([
        {"name": "Simulated Annealing", "runs": SA_RUNS,
         "distance": sa["best"], "time": sa["average_time"]},
        {"name": "Greedy (Nearest Neighbour)", "runs": 1,
         "distance": greedy["distance"], "time": greedy["time"]},
        {"name": "Random Search", "runs": RANDOM_TRIALS,
         "distance": random_result["distance"], "time": random_result["time"]},
        {"name": "Genetic Algorithm", "runs": GA_RUNS,
         "distance": ga["best"], "time": ga["average_time"]},
    ])

    print("\nBest route found by Simulated Annealing:\n")
    print(" -> ".join(sa["best_result"]["route"]))

    cooling_averages = None

    if ask_yes_no("\nAlso run the cooling rate experiment? [y/N]: "):
        cooling_averages = cooling_rate_experiment(graph, start)

    print("\nDisplaying visualizations...")

    plot_comparison([
        {"name": "Simulated Annealing", "distance": sa["best"], "time": sa["average_time"]},
        {"name": "Greedy", "distance": greedy["distance"], "time": greedy["time"]},
        {"name": "Random Search", "distance": random_result["distance"], "time": random_result["time"]},
        {"name": "Genetic Algorithm", "distance": ga["best"], "time": ga["average_time"]},
    ])

    plot_ga_convergence(ga_best["history"])

    if cooling_averages:
        plot_cooling_rates(COOLING_RATES, cooling_averages)

    plt.show()


if __name__ == "__main__":
    main()
