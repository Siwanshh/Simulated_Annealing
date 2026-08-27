import json
import os
import urllib.parse
import urllib.request

import folium

from places import PLACES


OSRM_URL = (
    "https://router.project-osrm.org/"
    "route/v1/driving/{coordinates}"
    "?overview=full&geometries=geojson"
)


def draw_tsp_map(route, distance):

    start = route[0]

    # Coordinates in the order found by SA
    coordinates = ";".join(
        f"{PLACES[city][1]},{PLACES[city][0]}"
        for city in route
    )

    url = OSRM_URL.format(
        coordinates=urllib.parse.quote(
            coordinates,
            safe=",;"
        )
    )

    # Get actual road geometry from OSRM
    with urllib.request.urlopen(
        url,
        timeout=30
    ) as response:
        data = json.loads(response.read())

    if data["code"] != "Ok":
        raise RuntimeError(
            f"OSRM routing failed: {data.get('code')}"
        )

    geometry = data["routes"][0]["geometry"]

    # Create map
    m = folium.Map(
        location=PLACES[start],
        zoom_start=13
    )

    # Draw actual road route
    folium.GeoJson(
        geometry,
        name="SA Route",
        style_function=lambda x: {
            "color": "red",
            "weight": 5,
            "opacity": 0.8
        },
        tooltip=f"SA distance: {distance:.2f} km"
    ).add_to(m)

    # Add numbered locations
    for i, city in enumerate(route[:-1], start=1):

        lat, lon = PLACES[city]

        folium.Marker(
            location=(lat, lon),
            popup=f"{i}. {city}",
            tooltip=city,
            icon=folium.DivIcon(
                html=f"""
                <div style="
                    background:white;
                    border:2px solid black;
                    border-radius:50%;
                    width:24px;
                    height:24px;
                    text-align:center;
                    line-height:24px;
                    font-weight:bold;
                ">
                    {i}
                </div>
                """
            )
        ).add_to(m)

    # Mark starting point
    folium.Marker(
        location=PLACES[start],
        popup=f"START: {start}",
        tooltip="Start",
        icon=folium.Icon(color="green")
    ).add_to(m)

    os.makedirs(
        "OUTPUT",
        exist_ok=True
    )

    m.save(
        "OUTPUT/tsp_map.html"
    )