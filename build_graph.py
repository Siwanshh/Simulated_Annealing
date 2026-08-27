import json
import os
import urllib.parse
import urllib.request

from places import PLACES


GRAPH_PATH = os.path.join(
    os.path.dirname(__file__),
    "OUTPUT",
    "tsp_graph.json"
)

OSRM_TABLE_URL = (
    "https://router.project-osrm.org/table/v1/driving/"
    "{coordinates}?annotations=distance,duration"
)


def build_tsp_graph():
    cities = list(PLACES.keys())

    # OSRM expects: lon,lat;lon,lat;...
    coordinates = ";".join(
        f"{lon},{lat}"
        for lat, lon in PLACES.values()
    )

    url = OSRM_TABLE_URL.format(
        coordinates=urllib.parse.quote(coordinates, safe=",;")
    )

    print("Requesting OSRM distance matrix...")
    print(f"Locations: {len(cities)}")

    with urllib.request.urlopen(url, timeout=30) as response:
        data = json.loads(response.read())

    if data.get("code") != "Ok":
        raise RuntimeError(
            f"OSRM request failed: {data.get('message', data.get('code'))}"
        )

    distances = data["distances"]
    durations = data["durations"]

    graph = {
        city: {}
        for city in cities
    }

    for i, city_a in enumerate(cities):
        for j, city_b in enumerate(cities):

            if i == j:
                continue

            distance_km = round(
                distances[i][j] / 1000,
                2
            )

            duration_min = round(
                durations[i][j] / 60,
                1
            )

            graph[city_a][city_b] = {
                "km": distance_km,
                "min": duration_min
            }

    os.makedirs(
        os.path.dirname(GRAPH_PATH),
        exist_ok=True
    )

    with open(GRAPH_PATH, "w") as f:
        json.dump(
            graph,
            f,
            indent=2
        )

    print(
        f"\nTSP graph saved to:\n{GRAPH_PATH}"
    )

    print(
        f"Created directed matrix: "
        f"{len(cities)} × {len(cities)}"
    )


if __name__ == "__main__":

    if os.path.exists(GRAPH_PATH):

        print(
            "The graph has already been created."
        )
        print(
            "Delete OUTPUT/tsp_graph.json "
            "first to recreate it."
        )

    else:

        print("Building TSP graph...")
        build_tsp_graph()