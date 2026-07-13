"""
In diesem ersten Schritt werden die Konfiguration geladen,
die Ausgabeordner erstellt und das Logging gestartet.
"""

import logging

from ebike_sim.config import BikeConfig, SimulationConfig, create_output_folders
from ebike_sim.logging_config import setup_logging


def main():
    """
    Startet das Programm.
    """

    setup_logging()
    create_output_folders()

    bike_config = BikeConfig()
    simulation_config = SimulationConfig()

    logging.info("Programm wurde gestartet.")
    logging.info("Konfiguration wurde geladen.")

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
    print("Ausgabeordner:", simulation_config.output_folder)

    logging.info("Programm wurde ohne Fehler beendet.")


if __name__ == "__main__":
    main()