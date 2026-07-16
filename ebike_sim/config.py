"""
Konfiguration und Grundparameter für die Simulation.
"""

import os


class BikeConfig:


    def __init__(self):
        # Werte aus der Aufgabenstellung
        self.mass_driver_kg = 70.0
        self.mass_bike_kg = 10.0

        # Gesamtmasse von Fahrer und Fahrrad
        self.total_mass_kg = self.mass_driver_kg + self.mass_bike_kg

        # Produkt aus Luftwiderstandsbeiwert und Stirnfläche
        self.cw_a = 0.5625

        # Raddurchmesser in Zoll
        self.wheel_diameter_inch = 27.0

        # Umrechnung von Zoll auf Meter
        self.wheel_diameter_m = self.wheel_diameter_inch * 0.0254
        self.wheel_radius_m = self.wheel_diameter_m / 2.0

        # Motorkonstante aus der Aufgabenstellung
        self.motor_constant_nm_per_a = 1.5

        # Annahmen für die Simulation
        self.gravity = 9.81
        self.air_density = 1.225
        self.roll_resistance_coefficient = 0.008


class SimulationConfig:


    def __init__(
        self,
        initial_soc=1.0,
        cell_capacity_ah=3.0,
        parallel_cells=8,
        series_cells=10
    ):
        # Eingabedatei
        self.input_file = "data/final_project_input_data.csv"

        # Ausgabeordner
        self.output_folder = "output"
        self.plot_folder = "output/plots"
        self.map_folder = "output/maps"
        self.result_folder = "output/results"
        self.report_folder = "output/reports"
        self.log_folder = "logs"

        # Einstellungen für den Akku
        self.initial_soc = initial_soc
        self.cell_capacity_ah = cell_capacity_ah
        self.parallel_cells = parallel_cells
        self.series_cells = series_cells

        # Temperatur für die Akku-Simulation
        self.temperature_c = 20.0


def create_output_folders():

    folders = [
        "output",
        "output/plots",
        "output/maps",
        "output/results",
        "output/reports",
        "logs"
    ]

    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)