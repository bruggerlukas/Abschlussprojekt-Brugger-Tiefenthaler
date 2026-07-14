import logging

from ebike_sim.config import BikeConfig, SimulationConfig, create_output_folders
from ebike_sim.logging_config import setup_logging
from ebike_sim.data_loader import GPSDataLoader

from ebike_sim.physics import RoutePhysicsCalculator

def main():
    setup_logging()
    create_output_folders()

    bike_config = BikeConfig()
    simulation_config = SimulationConfig()

    logging.info("Programm wurde gestartet.")

    gps_loader = GPSDataLoader(simulation_config.input_file)
    gps_data = gps_loader.load_data()

    route_calculator = RoutePhysicsCalculator(gps_data)
    route_data = route_calculator.calculate()

    print("E-Bike-Abschlussprojekt")
    print("-----------------------")
    print("Programm wurde erfolgreich gestartet.")
    print()
    print("Fahrergewicht:", bike_config.mass_driver_kg, "kg")
    print("Fahrradgewicht:", bike_config.mass_bike_kg, "kg")
    print("Gesamtmasse:", bike_config.total_mass_kg, "kg")
    print("Raddurchmesser:", bike_config.wheel_diameter_inch, "Zoll")
    print("Motorkonstante:", bike_config.motor_constant_nm_per_a, "Nm/A")
    print()
    print("Eingabedatei:", simulation_config.input_file)
    print("Anzahl GPS-Datenpunkte:", len(gps_data))
    print("Erster Zeitpunkt:", gps_data["time"].iloc[0])
    print("Letzter Zeitpunkt:", gps_data["time"].iloc[-1])

    logging.info("Programm wurde ohne Fehler beendet.")


    print("Berechnete Strecke:", round(route_data["distance_total_m"].iloc[-1] / 1000, 2), "km")
    print("Maximale Geschwindigkeit:", round(route_data["velocity_km_h"].max(), 2), "km/h")
    print("Maximale Beschleunigung:", round(route_data["acceleration_m_s2"].max(), 2), "m/s²")
    print("Maximale Steigung:", round(route_data["slope_percent"].max(), 2), "%")


if __name__ == "__main__":
    main()