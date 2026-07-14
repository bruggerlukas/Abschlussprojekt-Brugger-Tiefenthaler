import logging

from ebike_sim.logging_config import setup_logging
from ebike_sim.simulator import EBikeSimulator


def main():
    setup_logging()

    logging.info("Programm wurde gestartet.")

    simulator = EBikeSimulator()
    route_data = simulator.run()

    print("E-Bike-Abschlussprojekt")
    print("-----------------------")
    print("Simulation erfolgreich abgeschlossen.")
    print()
    print("Anzahl GPS-Datenpunkte:", len(route_data))
    print("Strecke:", round(route_data["distance_total_m"].iloc[-1] / 1000, 2), "km")
    print("Maximale Geschwindigkeit:", round(route_data["velocity_km_h"].max(), 2), "km/h")
    print("Maximale Beschleunigung:", round(route_data["acceleration_m_s2"].max(), 2), "m/s²")
    print("Maximale Steigung:", round(route_data["slope_percent"].max(), 2), "%")
    print("Maximale Leistung:", round(route_data["power_w"].max(), 2), "W")
    print("Maximales Drehmoment:", round(route_data["torque_nm"].max(), 2), "Nm")
    print("Maximaler Motorstrom:", round(route_data["motor_current_a"].max(), 2), "A")
    print()
    print("LiPo Ladezustand am Ende:", round(route_data["lipo_soc"].iloc[-1] * 100, 2), "%")
    print("NMC Ladezustand am Ende:", round(route_data["nmc_soc"].iloc[-1] * 100, 2), "%")

    logging.info("Programm wurde ohne Fehler beendet.")


if __name__ == "__main__":
    main()