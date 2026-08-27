import folium
from places import PLACES

def draw_tsp_map(route, distance):

    start = route[0]

    m = folium.Map(
        location=PLACES[start],
        zoom_start=13
    )

    # Mark locations
    for i, city in enumerate(route[:-1], start=1):

        lat, lon = PLACES[city]

        folium.CircleMarker(
            location=(lat, lon),
            radius=7,
            color="blue",
            fill=True,
            popup=f"{i}. {city}",
            tooltip=city
        ).add_to(m)

    # Draw TSP route
    folium.PolyLine(
        [PLACES[city] for city in route],
        color="red",
        weight=5,
        tooltip=f"TSP distance: {distance:.2f} km"
    ).add_to(m)

    # Mark start
    folium.Marker(
        PLACES[start],
        popup=f"START: {start}",
        tooltip="Start",
        icon=folium.Icon(color="green")
    ).add_to(m)

    # Route numbers
    for i, city in enumerate(route[:-1], start=1):

        lat, lon = PLACES[city]

        folium.Marker(
            location=(lat, lon),
            icon=folium.DivIcon(
                html=f"""
                <div style="
                    font-size: 14px;
                    font-weight: bold;
                    color: black;
                    background-color: white;
                    border: 2px solid black;
                    border-radius: 50%;
                    width: 24px;
                    height: 24px;
                    text-align: center;
                    line-height: 24px;
                ">
                    {i}
                </div>
                """
            )
        ).add_to(m)

    import os

    os.makedirs("OUTPUT", exist_ok=True)
    m.save("OUTPUT/tsp_map.html")


