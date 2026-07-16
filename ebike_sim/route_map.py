import os
import folium


class RouteMapCreator:

    def __init__(self, route_data):
        self.route_data = route_data

    def create_map(self):
        if not os.path.exists("output/maps"):
            os.makedirs("output/maps")

        map_file = "output/maps/route_map.html"

        center_lat = self.route_data["lat"].mean()
        center_lon = self.route_data["lon"].mean()

        route_map = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=11,
            control_scale=True
        )

        coordinates = []

        for i in range(len(self.route_data)):
            lat = float(self.route_data.loc[i, "lat"])
            lon = float(self.route_data.loc[i, "lon"])
            coordinates.append([lat, lon])

        folium.PolyLine(
            coordinates,
            weight=4,
            tooltip="GPS-Route"
        ).add_to(route_map)

        folium.Marker(
            coordinates[0],
            tooltip="Start",
            popup="Start der Fahrt"
        ).add_to(route_map)

        folium.Marker(
            coordinates[-1],
            tooltip="Ziel",
            popup="Ende der Fahrt"
        ).add_to(route_map)

        total_distance_m = self.route_data["distance_total_m"].iloc[-1]
        total_distance_km = int(total_distance_m / 1000)

        for kilometer in range(10, total_distance_km + 1, 10):
            distance_m = kilometer * 1000
            index = (self.route_data["distance_total_m"] - distance_m).abs().idxmin()

            lat = float(self.route_data.loc[index, "lat"])
            lon = float(self.route_data.loc[index, "lon"])
            height = float(self.route_data.loc[index, "ele"])

            folium.CircleMarker(
                location=[lat, lon],
                radius=4,
                popup=str(kilometer) + " km, Höhe: " + str(round(height, 1)) + " m"
            ).add_to(route_map)

        route_map.save(map_file)

        return map_file
    

    