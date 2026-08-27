# Simulated Annealing for the Travelling Salesman Problem

This project uses simulated annealing to find a good round trip through a set
of places in Kathmandu. The route starts at `Kupondole`, visits every other
place once, and returns to `Kupondole`.

The goal is the familiar Travelling Salesman Problem: find the shortest route
that visits every location exactly once. Finding the perfect route becomes
expensive as the number of locations grows, so this project uses a practical
search method that usually finds a very good route without checking every
possible order.

## What the program does

When you run the program, it:

1. Gets driving distances and travel times for the locations from the public
	OSRM routing service.
2. Saves that distance matrix in `OUTPUT/tsp_graph.json`.
3. Runs simulated annealing 30 times, starting with a different random route
	each time.
4. Keeps the best route found across all runs.
5. Saves the results from every run in `OUTPUT/sa_runs.json`.
6. Creates an interactive HTML map at `OUTPUT/tsp_map.html`.

The graph is created only when `OUTPUT/tsp_graph.json` is missing. Delete that
file if you change the locations in `places.py` and want to request a new
distance matrix.

## Project files

| File | Purpose |
| --- | --- |
| `main.py` | Runs the complete process |
| `build_graph.py` | Builds the driving-distance graph using OSRM |
| `simulated_annealing.py` | Contains the simulated annealing algorithm |
| `draw_map.py` | Draws the final route on an interactive map |
| `places.py` | Stores the place names and coordinates |
| `simpe_simuated_annealing.ipynb` | Notebook with an introductory example and experiments |
| `OUTPUT/` | Generated graph, run results, and map |

## Setup

Use Python 3 and install the packages used by the project:

```bash
pip install -r requirements.txt
```

The main program also needs internet access because OSRM is used to obtain
driving distances and route geometry.

## Run it

From this directory, run:

```bash
python3 main.py
```

The terminal prints the result of each annealing run and the best route found.
Open `OUTPUT/tsp_map.html` in a browser to see the route on a map.

## How simulated annealing works here

The algorithm begins with a random route. It then creates a nearby route by
swapping two places. A shorter route is accepted immediately. A longer route
can also be accepted early in the search, which helps the algorithm move away
from a locally good but globally poor route.

As the temperature cools, accepting longer routes becomes less likely. The
search gradually settles on a short route. Because the process is random, the
answer can vary slightly between runs; running it 30 times gives the program
more chances to find a strong result.

## Changing the locations

Edit the `PLACES` dictionary in `places.py`. Each entry has the form:

```python
"Place name": (latitude, longitude)
```

After changing it, remove the old graph and run the program again:

```bash
rm OUTPUT/tsp_graph.json
python3 main.py
```

The locations should be close enough for OSRM to return driving routes between
them.
