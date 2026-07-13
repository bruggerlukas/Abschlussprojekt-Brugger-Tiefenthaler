from battery_base import BatteryBase
from lifepo4_battery import LiFePO4BatteryPack

from plotting_utils import plot_current_profile, plot_voltage_profile, plot_voltage_and_current_profile




class BatterySimulator:
    """Simple simulator for a battery pack. The simulator applies a current profile to the battery pack and records the voltage profile."""

    def __init__(self, battery: BatteryBase) -> None:
        self.battery = battery
        self.voltage_profile = []

    def simulate(self, current_profile: list[float], duration_profile: list[float]) -> None:
        self.voltage_profile = []
        self.voltage_profile.append(self.battery.voltage())

        for i, t in zip(current_profile, duration_profile):
            self.battery.apply_current(current=i, duration=t)
            self.voltage_profile.append(self.battery.voltage(current=i))


if __name__ == "__main__":
    load_current = [3.0, 11.0, 4.0, -1.5, 1.0]
    load_durations = [300.0, 240.0, 90.0, 150.0, 120.0]

    plot_current_profile(current_profile=load_current, duration_profile=load_durations)

    params = {"capacity_nom_Ah": 10.0, "initial_soc": 0.7, "Vmin": 32.0, "Vmax": 42.0}
    battery = LiFePO4BatteryPack(**params)

    sim = BatterySimulator(battery)
    sim.simulate(load_current, load_durations)
    print(battery)

    plot_voltage_profile(voltage_profile=sim.voltage_profile, duration_profile=load_durations)
    plot_voltage_and_current_profile(sim.voltage_profile, load_current, load_durations)

    input("Press Enter to continue...")
