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

        lipo_battery = create_lipo_battery(self.simulation_config.start_soc)
        nmc_battery = create_nmc_battery(self.simulation_config.start_soc)

        route_data = lipo_battery.simulate(route_data)
        route_data = nmc_battery.simulate(route_data)

        self.logger.info("Simulation wurde erfolgreich beendet.")

        return route_data