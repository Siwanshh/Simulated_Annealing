import json
import ssl
import urllib.parse
import urllib.request

import certifi
import matplotlib.pyplot as plt

from places import PLACES

OSRM_ROUTE_URL = (
    "https://router.project-osrm.org/route/v1/driving/{coordinates}"
    "?overview=full&geometries=geojson"
)

SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())

BLUE = "#2a78d6"
ORANGE = "#eb6834"
GREEN = "#1baf7a"


def tidy(axis, xlabel, ylabel, title):
    axis.set_xlabel(xlabel)
    axis.set_ylabel(ylabel)
    axis.set_title(title, loc="left")
    axis.grid(True, color="#e5e4e0")
    axis.set_axisbelow(True)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)


def road_geometry(route):
    coordinates = ";".join("{},{}".format(PLACES[city][1], PLACES[city][0]) for city in route)
    url = OSRM_ROUTE_URL.format(coordinates=urllib.parse.quote(coordinates, safe=",;"))

    try:
        with urllib.request.urlopen(url, timeout=30, context=SSL_CONTEXT) as response:
            data = json.loads(response.read())
    except Exception:
        return None

    if data.get("code") != "Ok":
        return None

    return data["routes"][0]["geometry"]["coordinates"]


def plot_route(route, distance, start):
    figure, axis = plt.subplots(figsize=(9, 8), num="Best SA route")

    longitudes = [PLACES[city][1] for city in route]
    latitudes = [PLACES[city][0] for city in route]

    geometry = road_geometry(route)

    if geometry:
        axis.plot([point[0] for point in geometry], [point[1] for point in geometry],
                  color=BLUE, linewidth=1.8, zorder=1)
    else:
        axis.plot(longitudes, latitudes, color=BLUE, linewidth=1.5, zorder=1)

        for index in range(len(route) - 1):
            axis.annotate(
                "",
                xy=(longitudes[index + 1], latitudes[index + 1]),
                xytext=(longitudes[index], latitudes[index]),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, linewidth=1.2, shrinkA=6, shrinkB=6),
            )

    axis.scatter(longitudes[:-1], latitudes[:-1], color=BLUE, s=45, zorder=2)

    for order, city in enumerate(route[:-1], start=1):
        latitude, longitude = PLACES[city]
        shift = 7 if order % 2 else -13
        axis.annotate(
            "{}. {}".format(order, city),
            xy=(longitude, latitude),
            xytext=(6, shift),
            textcoords="offset points",
            fontsize=8,
        )

    axis.scatter(
        [PLACES[start][1]],
        [PLACES[start][0]],
        color=ORANGE,
        s=180,
        marker="*",
        zorder=3,
        label="Start: " + start,
    )

    tidy(
        axis,
        "Longitude",
        "Latitude",
        "Simulated Annealing best route\nStart: {}   Distance: {:.2f} km".format(start, distance),
    )

    axis.legend(frameon=False)

    return figure


def plot_sa_convergence(history):
    figure, axis = plt.subplots(figsize=(9, 4.5), num="SA convergence")

    iterations = [row[0] for row in history]

    axis.plot(iterations, [row[1] for row in history],
              color=BLUE, linewidth=1.0, label="Current route")
    axis.plot(iterations, [row[2] for row in history],
              color=ORANGE, linewidth=2.0, label="Best route so far")

    tidy(axis, "Iteration", "Route distance (km)", "How simulated annealing improves the route")
    axis.legend(frameon=False)

    return figure


def plot_ga_convergence(history):
    figure, axis = plt.subplots(figsize=(9, 4.5), num="GA convergence")

    axis.plot(range(len(history)), history, color=GREEN, linewidth=2.0)

    tidy(axis, "Generation", "Best route distance (km)", "How the genetic algorithm improves the route")

    return figure


def plot_comparison(results):
    figure, axes = plt.subplots(2, 1, figsize=(9, 7.5), num="Algorithm comparison")

    names = [result["name"].replace(" (", "\n(").replace(" ", "\n", 1) for result in results]
    distances = [result["distance"] for result in results]
    times = [result["time"] for result in results]

    bars = axes[0].bar(names, distances, color=BLUE, width=0.55)
    axes[0].set_ylim(0, max(distances) * 1.2)

    for bar, distance in zip(bars, distances):
        axes[0].annotate(
            "{:.2f}".format(distance),
            xy=(bar.get_x() + bar.get_width() / 2, distance),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            fontsize=9,
        )

    tidy(axes[0], "", "Route distance (km)", "Best route found by each algorithm")

    axes[1].plot(names, times, linestyle="none", marker="o", markersize=9, color=ORANGE)
    axes[1].set_yscale("log")
    axes[1].set_ylim(min(times) / 4, max(times) * 6)

    for name, value in zip(names, times):
        axes[1].annotate(
            "{:.4g} s".format(value),
            xy=(name, value),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            fontsize=9,
        )

    tidy(axes[1], "", "Run time (s, log scale)", "Time taken by each algorithm")

    figure.tight_layout()

    return figure


def plot_cooling_rates(rates, distances):
    figure, axis = plt.subplots(figsize=(9, 4.5), num="Cooling rate")

    labels = [str(rate) for rate in rates]

    axis.plot(labels, distances, linestyle="-", marker="o", markersize=9, color=BLUE)
    axis.margins(y=0.18)

    for label, distance in zip(labels, distances):
        axis.annotate(
            "{:.2f}".format(distance),
            xy=(label, distance),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            fontsize=9,
        )

    tidy(axis, "Cooling rate", "Average route distance (km)", "Effect of the cooling rate")

    return figure
