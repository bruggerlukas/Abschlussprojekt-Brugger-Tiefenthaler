import logging
import os


from ebike_sim.logging_config import setup_logging
from ebike_sim.simulator import EBikeSimulator
from ebike_sim.parameter_study import ParameterStudy
from ebike_sim.route_map import RouteMapCreator
from ebike_sim.battery_recommendation import BatteryRecommendation
from ebike_sim.plotting import (
    plot_elevation,
    plot_power,
    plot_soc_comparison,
    plot_speed,
)

def main():
    setup_logging()

    logging.info("Programm wurde gestartet.")

    simulator = EBikeSimulator()
    route_data = simulator.run()


    battery_recommendation = BatteryRecommendation(route_data)
    battery_recommendation_result = battery_recommendation.calculate()

    map_creator = RouteMapCreator(route_data)
    map_file = map_creator.create_map()

    parameter_study = ParameterStudy(route_data)
    parameter_results = parameter_study.run()
    parameter_file = parameter_study.save_results(parameter_results)

    if not os.path.exists("output/results"):
        os.makedirs("output/results")

    route_data.to_csv("output/results/simulation_results.csv", index=False)

    logging.info("Simulationsergebnisse wurden gespeichert.")

    speed_plot_path = plot_speed(
        route_data,
        "output/plots"
    )

    power_plot_path = plot_power(
        route_data,
        "output/plots"
    )

    elevation_plot_path = plot_elevation(
        route_data,
        "output/plots"
    )

    soc_plot_path = plot_soc_comparison(
        route_data,
        "output/plots"
    )

    logging.info("Alle Pflichtdiagramme wurden gespeichert.")

    total_distance_km = route_data["distance_total_m"].iloc[-1] / 1000

    duration_seconds = route_data["delta_time_s"].sum()
    duration_minutes = duration_seconds / 60
    duration_hours = duration_seconds / 3600

    if duration_hours > 0:
        average_speed_kmh = total_distance_km / duration_hours
    else:
        average_speed_kmh = 0.0

    elevation_gain_m = (
        route_data["height_difference_m"]
        .clip(lower=0)
        .sum()
    )

    elevation_loss_m = -(
        route_data["height_difference_m"]
        .clip(upper=0)
        .sum()
    )

    print("E-Bike-Abschlussprojekt")
    print("-----------------------")
    print("Simulation erfolgreich abgeschlossen.")
    print()
    print("Anzahl GPS-Datenpunkte:", len(route_data))
    print("Strecke:", round(total_distance_km, 2), "km")
    print("Fahrtdauer:", round(duration_minutes, 2), "min")
    print(
        "Durchschnittsgeschwindigkeit:",
        round(average_speed_kmh, 2),
        "km/h"
    )
    print("Höhenmeter Anstieg:", round(elevation_gain_m, 2), "m")
    print("Höhenmeter Abstieg:", round(elevation_loss_m, 2), "m")
    print("Maximale Geschwindigkeit:", round(route_data["velocity_km_h"].max(), 2), "km/h")
    print("Maximale Beschleunigung:", round(route_data["acceleration_m_s2"].max(), 2), "m/s²")
    print("Maximale Steigung:", round(route_data["slope_percent"].max(), 2), "%")
    print("Maximale Leistung:", round(route_data["power_w"].max(), 2), "W")
    print("Maximales Drehmoment:", round(route_data["torque_nm"].max(), 2), "Nm")
    print("Maximaler Motorstrom:", round(route_data["motor_current_a"].max(), 2), "A")
    print()
    print("LiPo Ladezustand am Ende:", round(route_data["lipo_soc"].iloc[-1] * 100, 2), "%")
    print("NMC Ladezustand am Ende:", round(route_data["nmc_soc"].iloc[-1] * 100, 2), "%")


    print()
    print("Geschwindigkeitsdiagramm:", speed_plot_path)
    print("Leistungsdiagramm:", power_plot_path)
    print("Höhenprofil:", elevation_plot_path)
    print("Akkuvergleich:", soc_plot_path)
    print("Parameterstudie gespeichert:", parameter_file)
    print("Karte gespeichert:", map_file)


    print()
    print("Akku-Empfehlung:")
    print("Benötigte Energie:", round(battery_recommendation_result["energy_wh"], 2), "Wh")
    print("Empfohlene Energie mit 20 Prozent Reserve:", round(battery_recommendation_result["recommended_energy_wh"], 2), "Wh")
    print("Empfohlene Akkukapazität:", round(battery_recommendation_result["recommended_capacity_ah"], 2), "Ah bei 37 V")
    
    print()
    logging.info("Programm wurde ohne Fehler beendet.")


if __name__ == "__main__":
    main()