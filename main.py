import matplotlib.pyplot as plt

from draw_map import draw_tsp_map
from plots import plot_route, plot_sa_convergence
from simulated_annealing import run_many
from tsp import choose_start, load_graph, summarise_runs

SA_RUNS = 30
INITIAL_TEMPERATURE = 100.0
COOLING_RATE = 0.995
MINIMUM_TEMPERATURE = 0.001
ITERATIONS_PER_TEMPERATURE = 100


def main():
    print("=" * 40)
    print("Kathmandu TSP")
    print("Simulated Annealing")
    print("=" * 40)
    print()

    print("Loading Kathmandu road distances...\n")
    graph = load_graph()
    cities = list(graph)

    start = choose_start(cities)
    print("\nStarting location: {}\n".format(start))

    print("Simulated Annealing settings")
    print("  initial temperature        {}".format(INITIAL_TEMPERATURE))
    print("  cooling rate               {}".format(COOLING_RATE))
    print("  minimum temperature        {}".format(MINIMUM_TEMPERATURE))
    print("  iterations per temperature {}".format(ITERATIONS_PER_TEMPERATURE))

    print("\nRunning Simulated Annealing ({} runs)...".format(SA_RUNS))

    results = run_many(
        graph,
        start,
        runs=SA_RUNS,
        initial_temperature=INITIAL_TEMPERATURE,
        cooling_rate=COOLING_RATE,
        minimum_temperature=MINIMUM_TEMPERATURE,
        iterations_per_temperature=ITERATIONS_PER_TEMPERATURE,
    )

    summary = summarise_runs(results)
    best = summary["best_result"]

    print("\nResults over {} runs".format(SA_RUNS))
    print("  best       {:.2f} km".format(summary["best"]))
    print("  average    {:.2f} km".format(summary["average"]))
    print("  worst      {:.2f} km".format(summary["worst"]))
    print("  std dev    {:.2f} km".format(summary["std"]))
    print("  iterations {} per run".format(best["iterations"]))
    print("  time       {:.2f} sec per run, {:.2f} sec in total".format(
        summary["average_time"], summary["average_time"] * SA_RUNS
    ))

    print("\nBest SA route (seed {}):\n".format(best["seed"]))
    print(" -> ".join(best["route"]))
    print("\nSA distance: {:.2f} km".format(summary["best"]))

    print("\nDrawing map...")

    try:
        map_path = draw_tsp_map(best["route"], summary["best"])
        print("Map saved to {}".format(map_path))
    except Exception as error:
        print("Map could not be drawn ({}: {})".format(type(error).__name__, error))

    print("\nDisplaying visualizations...")

    plot_route(best["route"], summary["best"], start)
    plot_sa_convergence(best["history"])

    plt.show()

   

if __name__ == "__main__":
    main()
