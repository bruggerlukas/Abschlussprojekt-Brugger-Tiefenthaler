"""
Steuerung des gesamten Simulationsablaufs.
"""

import logging

from ebike_sim.config import BikeConfig, SimulationConfig, create_output_folders
from ebike_sim.data_loader import GPSDataLoader
from ebike_sim.physics import RoutePhysicsCalculator
from ebike_sim.battery import create_lipo_battery, create_nmc_battery


class EBikeSimulator:

    def __init__(self):
        self.bike_config = BikeConfig()
        self.simulation_config = SimulationConfig()
        self.logger = logging.getLogger(__name__)

    def run(self):
        create_output_folders()

        self.logger.info("Simulation wird gestartet.")

        gps_loader = GPSDataLoader(self.simulation_config.input_file)
        gps_data = gps_loader.load_data()

        route_calculator = RoutePhysicsCalculator(gps_data, self.bike_config)
        route_data = route_calculator.calculate()

        lipo_battery = create_lipo_battery(self.simulation_config)
        nmc_battery = create_nmc_battery(self.simulation_config)

        lipo_soc = []
        lipo_voltage = []
        lipo_current = []

        nmc_soc = []
        nmc_voltage = []
        nmc_current = []

        for i in range(len(route_data)):
            power = route_data.loc[i, "power_w"]
            delta_time = route_data.loc[i, "delta_time_s"]

            lipo_result = lipo_battery.apply_power(power, delta_time)
            nmc_result = nmc_battery.apply_power(power, delta_time)

            lipo_soc.append(lipo_result.soc)
            lipo_voltage.append(lipo_result.voltage_v)
            lipo_current.append(lipo_result.current_a)

            nmc_soc.append(nmc_result.soc)
            nmc_voltage.append(nmc_result.voltage_v)
            nmc_current.append(nmc_result.current_a)

        route_data["lipo_soc"] = lipo_soc
        route_data["lipo_voltage_v"] = lipo_voltage
        route_data["lipo_battery_current_a"] = lipo_current

        route_data["nmc_soc"] = nmc_soc
        route_data["nmc_voltage_v"] = nmc_voltage
        route_data["nmc_battery_current_a"] = nmc_current

        self.logger.info("Simulation wurde erfolgreich beendet.")

        return route_data