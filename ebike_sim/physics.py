"""
Rechnungen aus GPS Daten und physikalische Berechnungen
"""

import logging
import math


class RoutePhysicsCalculator:

    def __init__(self, data, bike_config):
        self.data = data.copy()
        self.bike_config = bike_config
        self.logger = logging.getLogger(__name__)

    def calculate(self):
        self.logger.info("Fahrdaten werden berechnet.")

        distances = []
        total_distances = []
        delta_times = []
        velocities = []
        accelerations = []
        height_differences = []
        slopes_percent = []
        slopes_rad = []

        total_distance = 0.0
        last_velocity = 0.0

        for i in range(len(self.data)):
            if i == 0:
                distance = 0.0
                delta_time = 0.0
                velocity = 0.0
                acceleration = 0.0
                height_difference = 0.0
                slope_percent = 0.0
                slope_rad = 0.0
            else:
                lat1 = self.data.loc[i - 1, "lat"]
                lon1 = self.data.loc[i - 1, "lon"]
                lat2 = self.data.loc[i, "lat"]
                lon2 = self.data.loc[i, "lon"]

                distance = self.calculate_distance(lat1, lon1, lat2, lon2)
                total_distance = total_distance + distance

                time1 = self.data.loc[i - 1, "time"]
                time2 = self.data.loc[i, "time"]
                delta_time = (time2 - time1).total_seconds()

                if delta_time > 0:
                    velocity = distance / delta_time
                    acceleration = (velocity - last_velocity) / delta_time
                else:
                    velocity = 0.0
                    acceleration = 0.0

                height1 = self.data.loc[i - 1, "ele"]
                height2 = self.data.loc[i, "ele"]
                height_difference = height2 - height1

                if distance > 0:
                    slope = height_difference / distance
                    slope_percent = slope * 100
                    slope_rad = math.atan(slope)
                else:
                    slope_percent = 0.0
                    slope_rad = 0.0

                last_velocity = velocity

            distances.append(distance)
            total_distances.append(total_distance)
            delta_times.append(delta_time)
            velocities.append(velocity)
            accelerations.append(acceleration)
            height_differences.append(height_difference)
            slopes_percent.append(slope_percent)
            slopes_rad.append(slope_rad)

        self.data["distance_m"] = distances
        self.data["distance_total_m"] = total_distances
        self.data["delta_time_s"] = delta_times
        self.data["velocity_m_s"] = velocities
        self.data["velocity_km_h"] = self.data["velocity_m_s"] * 3.6
        self.data["acceleration_m_s2"] = accelerations
        self.data["height_difference_m"] = height_differences
        self.data["slope_percent"] = slopes_percent
        self.data["slope_rad"] = slopes_rad

        self.calculate_motor_values()

        self.logger.info("Fahrdaten wurden erfolgreich berechnet.")

        return self.data

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        earth_radius = 6371000

        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        delta_lat = lat2_rad - lat1_rad
        delta_lon = lon2_rad - lon1_rad

        a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return earth_radius * c

    def calculate_motor_values(self):
        forces = []
        powers = []
        torques = []
        currents = []

        for i in range(len(self.data)):
            velocity = self.data.loc[i, "velocity_m_s"]
            acceleration = self.data.loc[i, "acceleration_m_s2"]
            slope_rad = self.data.loc[i, "slope_rad"]

            force_acceleration = self.bike_config.total_mass_kg * acceleration
            force_slope = self.bike_config.total_mass_kg * self.bike_config.gravity * math.sin(slope_rad)
            force_roll = self.bike_config.total_mass_kg * self.bike_config.gravity * self.bike_config.roll_resistance_coefficient * math.cos(slope_rad)
            force_air = 0.5 * self.bike_config.air_density * self.bike_config.cw_a * velocity ** 2

            force_total = force_acceleration + force_slope + force_roll + force_air
            power = force_total * velocity
            torque = force_total * self.bike_config.wheel_radius_m
            current = torque / self.bike_config.motor_constant_nm_per_a

            forces.append(force_total)
            powers.append(power)
            torques.append(torque)
            currents.append(current)

        self.data["force_total_n"] = forces
        self.data["power_w"] = powers
        self.data["torque_nm"] = torques
        self.data["motor_current_a"] = currents