import os
import pandas as pd

from ebike_sim.config import BikeConfig
from ebike_sim.physics import RoutePhysicsCalculator


class ParameterStudy:

    def __init__(self, route_data):
        self.route_data = route_data[["lat", "lon", "ele", "time"]].copy()

    def run(self):
        results = []

        self.add_mass_cases(results)
        self.add_air_resistance_cases(results)
        self.add_roll_resistance_cases(results)
        self.add_wheel_cases(results)

        return pd.DataFrame(results)

    def add_mass_cases(self, results):
        masses = [60, 70, 80, 90, 100]

        for mass in masses:
            bike_config = BikeConfig()
            bike_config.mass_driver_kg = mass
            bike_config.total_mass_kg = bike_config.mass_driver_kg + bike_config.mass_bike_kg

            result = self.calculate_case("Fahrergewicht " + str(mass) + " kg", bike_config)
            results.append(result)

    def add_air_resistance_cases(self, results):
        cw_values = [0.45, 0.5625, 0.70]

        for cw in cw_values:
            bike_config = BikeConfig()
            bike_config.cw_a = cw

            result = self.calculate_case("cwA " + str(cw), bike_config)
            results.append(result)

    def add_roll_resistance_cases(self, results):
        roll_values = [0.004, 0.008, 0.012]

        for roll_value in roll_values:
            bike_config = BikeConfig()
            bike_config.roll_resistance_coefficient = roll_value

            result = self.calculate_case("Rollwiderstand " + str(roll_value), bike_config)
            results.append(result)

    def add_wheel_cases(self, results):
        wheel_values = [26, 27, 29]

        for wheel in wheel_values:
            bike_config = BikeConfig()
            bike_config.wheel_diameter_inch = wheel
            bike_config.wheel_diameter_m = bike_config.wheel_diameter_inch * 0.0254
            bike_config.wheel_radius_m = bike_config.wheel_diameter_m / 2.0

            result = self.calculate_case("Raddurchmesser " + str(wheel) + " Zoll", bike_config)
            results.append(result)

    def calculate_case(self, name, bike_config):
        calculator = RoutePhysicsCalculator(self.route_data, bike_config)
        route_data = calculator.calculate()

        positive_power = route_data["power_w"].clip(lower=0)
        energy_wh = (positive_power * route_data["delta_time_s"]).sum() / 3600

        result = {
            "fall": name,
            "fahrergewicht_kg": bike_config.mass_driver_kg,
            "cw_a": bike_config.cw_a,
            "rollwiderstand": bike_config.roll_resistance_coefficient,
            "raddurchmesser_zoll": bike_config.wheel_diameter_inch,
            "energiebedarf_wh": energy_wh,
            "max_leistung_w": route_data["power_w"].max(),
            "durchschnittsleistung_w": positive_power.mean(),
            "max_motorstrom_a": route_data["motor_current_a"].max()
        }

        return result

    def save_results(self, results):
        if not os.path.exists("output/results"):
            os.makedirs("output/results")

        file_path = "output/results/parameter_study.csv"
        results.to_csv(file_path, index=False)

        return file_path