"""
Berechnung einer empfohlenen Akkukapazität mit Sicherheitsreserve.
"""

class BatteryRecommendation:

    def __init__(self, route_data):
        self.route_data = route_data

    def calculate(self):
        positive_power = self.route_data["power_w"].clip(lower=0)
        delta_time = self.route_data["delta_time_s"]

        energy_wh = (positive_power * delta_time).sum() / 3600

        reserve_factor = 1.2
        recommended_energy_wh = energy_wh * reserve_factor

        nominal_voltage = 37.0
        recommended_capacity_ah = recommended_energy_wh / nominal_voltage

        result = {
            "energy_wh": energy_wh,
            "recommended_energy_wh": recommended_energy_wh,
            "recommended_capacity_ah": recommended_capacity_ah
        }

        return result
    


