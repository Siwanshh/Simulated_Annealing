# Simulated Annealing for the Travelling Salesman Problem

This project uses **Simulated Annealing** to find a short round trip through 20
real locations in Kathmandu. You choose the starting location, the route visits
every other location exactly once, and it returns to where it started.

Distances are **real driving distances** taken from the public OSRM routing
service, not straight-line distances. The matrix is directed, so the drive from
A to B is usually not the same length as the drive from B to A, and the cost of
a route always follows the direction of travel.

Simulated annealing is the main algorithm of the project. Three simpler methods
are included only as benchmarks: greedy nearest neighbour, random search and a
small genetic algorithm.

## Project files

| File | Purpose |
| --- | --- |
| `places.py` | The 20 Kathmandu locations and their coordinates |
| `build_graph.py` | Requests the driving-distance matrix from OSRM and saves it |
| `tsp.py` | Shared route helpers: load the graph, route distance, random route, swap, validity, run statistics |
| `simulated_annealing.py` | The simulated annealing algorithm and the multi-run helper |
| `baselines.py` | Greedy nearest neighbour and random search |
| `genetic_algorithm.py` | A small genetic algorithm (tournament selection, order crossover, swap mutation, elitism) |
| `plots.py` | The matplotlib figures |
| `draw_map.py` | Draws the best route on an interactive map using real road geometry |
| `main.py` | The main program: simulated annealing only |
| `comparison.py` | Compares simulated annealing with the other three algorithms |
| `simpe_simuated_annealing.ipynb` | Introductory notebook: simulated annealing on a one-dimensional function |
| `OUTPUT/` | The saved distance matrix, the locations it was built from, and the generated map |

## Setup

```bash
pip install -r requirements.txt
python main.py
```

There are two programs, and both start by asking for a starting location:

- `python main.py` is the project itself. It runs simulated annealing only:
  30 runs, the statistics, the best route, the map and the two SA figures.
- `python comparison.py` is only for comparing simulated annealing against
  greedy nearest neighbour, random search and the genetic algorithm. It also
  offers to run the cooling-rate experiment.

Internet access is needed the first time, because the distance matrix comes from
OSRM. After that `OUTPUT/tsp_graph.json` is reused, and the matrix is only
requested again if the locations in `places.py` change. Drawing the map also
uses OSRM; if that request fails the program says so and carries on.

The OSRM requests verify the certificate against the `certifi` bundle, because
the certificate store that Python uses by default is out of date on some
machines and the request then fails with `CERTIFICATE_VERIFY_FAILED`.

## How simulated annealing works here

A route is a list of locations that starts and ends at the chosen location and
contains every other location exactly once.

1. Start from a random route.
2. Measure its total driving distance.
3. Make a neighbouring route by swapping two locations.
4. If the new route is shorter, accept it.
5. If it is longer, accept it anyway with probability `P = exp(-delta / T)`,
   where `delta` is the extra distance and `T` is the temperature.
6. After every 100 candidate routes, cool down: `T = T * cooling_rate`.
7. Stop when the temperature falls below 0.001.
8. Repeat the whole run 30 times with different random seeds.
9. Keep the best route found.

Accepting a worse route is the important part. Early in the search the
temperature is high, so most worse routes are accepted and the search explores
freely. As the temperature falls, worse routes are rejected more and more often
and the search settles down. Without this, the search would stop at the first
local optimum it reached.

The best route is stored separately from the current route, so accepting a worse
route can never lose the best one found so far.

Default settings: initial temperature 100, cooling rate 0.995, minimum
temperature 0.001, 100 iterations per temperature.

## The comparison algorithms

All four algorithms use the same locations, the same OSRM distance matrix, the
same starting location and the same route rules, so the comparison is fair.

**Greedy (nearest neighbour)** starts at the chosen location and repeatedly
moves to the nearest location it has not visited yet, then returns to the start.
It is extremely fast, but it only ever looks one step ahead, so the last few
legs of the route are usually long and the complete route is poor.

**Random search** keeps the start fixed, shuffles the other locations, measures
the route, and keeps the best of 1000 random routes. It shows what happens
without any search strategy at all.

**Genetic algorithm** keeps a population of 40 routes for 200 generations. Each
route is a chromosome, fitness is the total distance, parents are chosen by
tournament selection, children are made with order crossover (which is safe for
the TSP because it never repeats or drops a location), mutation swaps two
locations with probability 0.1, and the best route of each generation is carried
forward unchanged (elitism).

Simulated annealing and the genetic algorithm are both run several times,
because they are random and give a different answer each time. Greedy is
deterministic, so one run is enough.

None of these methods guarantees the shortest possible route. They are
heuristics: they look for a good route in reasonable time, which is the point of
using them on a problem where checking every possible order is impractical.

## The cooling-rate experiment

`comparison.py` offers to run simulated annealing with cooling rates 0.95, 0.99,
0.995 and 0.999 and prints the average distance for each. A cooling rate closer to 1
means the temperature falls more slowly, which gives more iterations, a better
route and a longer run time.

## Visualisations

`main.py` displays:

1. The best simulated annealing route on the map coordinates, numbered, with the
   start marked and the distance in the title.
2. The convergence of the best run: the current route distance and the
   best-so-far distance against the iteration number.

It also writes `OUTPUT/tsp_map.html`, an interactive map that shows the route
following the actual roads.

`comparison.py` displays:

1. A comparison of the four algorithms: route distance, and run time below it.
2. The best distance per generation of the genetic algorithm.
3. The average distance for each cooling rate, if that experiment was run.

## Changing the locations

Edit the `PLACES` dictionary in `places.py`:

```python
"Place name": (latitude, longitude)
```

The program saves the locations it used in `OUTPUT/tsp_places.json` alongside the
matrix, so if you change a name or move a coordinate it notices and requests a
new distance matrix automatically the next time it runs.

If a coordinate is placed away from a road, OSRM has to snap it to the nearest
road before measuring, and the distances get worse. A quick way to check a new
location is the OSRM nearest service, which reports how far the point is from
the road it snapped to:

```
https://router.project-osrm.org/nearest/v1/driving/<longitude>,<latitude>
```
