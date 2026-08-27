
from simulated_annealing import simulated_annealing
from draw_map import draw_tsp_map
from build_graph import GRAPH_PATH, build_tsp_graph
import os 


def main():

    start = "Kupondole"
    
    if os.path.exists(GRAPH_PATH):
            print(
                "The graph has already been created, delete "
                "OUTPUT/tsp_graph.json first if you want to recreate graph."
            )
    else:
            print("Building the graph...")
            build_tsp_graph()
            

    print("\nStarting SA...")

    best_route, best_distance, history = simulated_annealing(
        start=start,
        initial_temperature=100,
        cooling_rate=0.995,
        minimum_temperature=0.001,
        iterations_per_temperature=100
    )

    print("SA finished.")

    print("\nBest route:")
    print(" → ".join(best_route))

    print(f"Total distance: {best_distance:.2f} km")

    print("\nDrawing map...")

    draw_tsp_map(best_route, best_distance)

    print("Map finished.")


if __name__ == "__main__":
    main()