import json
import time
import urllib.request
from places import PLACES
import os


GRAPH_PATH = os.path.join(os.path.dirname(__file__), "OUTPUT", "tsp_graph.json")
print(GRAPH_PATH)

OSRM_URL = (
    "http://router.project-osrm.org/route/v1/driving/"
    "{lon1},{lat1};{lon2},{lat2}?overview=false"
)


def road_distance(a, b):

    lat1, lon1 = PLACES[a]
    lat2, lon2 = PLACES[b]

    url = OSRM_URL.format(
        lon1=lon1,
        lat1=lat1,
        lon2=lon2,
        lat2=lat2
    )

    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read())

    route = data["routes"][0]

    km = round(route["distance"] / 1000, 2)
    mins = round(route["duration"] / 60, 1)

    return km, mins


def build_tsp_graph():

    cities = list(PLACES.keys())

    graph = {
        city: {}
        for city in cities
    }

    total_pairs = len(cities) * (len(cities) - 1) // 2

    pair_number = 0

    for i in range(len(cities)):

        for j in range(i + 1, len(cities)):

            a = cities[i]
            b = cities[j]

            pair_number += 1

            print(
                f"[{pair_number}/{total_pairs}] "
                f"{a} <-> {b}"
            )

            km, mins = road_distance(a, b)

            graph[a][b] = {
                "km": km,
                "min": mins
            }

            graph[b][a] = {
                "km": km,
                "min": mins
            }

            print(
                f"    {km} km ({mins} min)"
            )

            # Don't hammer public OSRM server
            time.sleep(1)

    os.makedirs(os.path.dirname(GRAPH_PATH), exist_ok=True)

    with open(GRAPH_PATH, "w") as f:
        json.dump(graph, f, indent=2)

    print("\nTSP graph saved to tsp_graph.json")

   

if __name__ == '__main__':
    if os.path.exists(GRAPH_PATH):
        print(
            "The graph has already been created, delete "
            "OUTPUT/tsp_graph.json first to recreate graph."
        )
    else:
        print("Building the graph...")
        build_tsp_graph()