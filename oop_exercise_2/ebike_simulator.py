from battery_base import BatteryBase
from lifepo4_battery import LiFePO4BatteryPack

from motor import Motor as Motor

from plotting_utils import plot_power_profile, plot_current_profile, plot_voltage_profile, plot_voltage_and_current_profile


class EBikeSimluator:
    """Simple simulator for a battery pack. The simulator applies a current profile to the battery pack and records the voltage profile."""

    def __init__(self, battery: BatteryBase, motor: Motor) -> None:
        self.battery = battery
        self.motor = motor

        self.voltage_profile = []
        self.current_profile = []

    def simulate(self, power_profile: list[float], duration_profile: list[float]) -> None:
        self.voltage_profile = []
        self.current_profile = []
        
        self.voltage_profile.append(self.battery.voltage())

        for p, t in zip(power_profile, duration_profile):
            unloaded_voltage = self.battery.voltage()
            current_draw = self.motor.get_current_draw(power=p, voltage=unloaded_voltage)

            self.current_profile.append(current_draw)

            self.battery.apply_current(current=current_draw, duration=t)
            self.voltage_profile.append(self.battery.voltage(current=current_draw))


if __name__ == "__main__":
    power_profile_W = [115, 420, 150, -60, 38, 300, 0.0, 435, -75, 111]
    duration_s = [300.0, 240.0, 90.0, 150.0, 120.0, 300.0, 60.0, 30.0, 120.0, 180.0]

    plot_power_profile(power_profile=power_profile_W, duration_profile=duration_s)

    params = {"capacity_nom_Ah": 10.0, "initial_soc": 0.7, "Vmin": 32.0, "Vmax": 42.0}
    battery = LiFePO4BatteryPack(**params)
    
    motor = Motor()

    sim = EBikeSimluator(battery, motor)
    sim.simulate(power_profile_W, duration_s)
    print(battery)

    plot_voltage_profile(voltage_profile=sim.voltage_profile, duration_profile=duration_s)
    plot_current_profile(current_profile=sim.current_profile, duration_profile=duration_s)

    plot_voltage_and_current_profile(sim.voltage_profile, sim.current_profile, duration_s)

    input("Press Enter to exit...")
