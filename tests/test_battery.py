from ebike_sim.battery import create_lipo_battery, create_nmc_battery
from ebike_sim.config import SimulationConfig


def test_lipo_discharge_reduces_soc():
    battery = create_lipo_battery(SimulationConfig(parallel_cells=2), initial_soc=1.0)
    start = battery.soc
    battery.apply_current(10.0, 60.0)
    assert battery.soc < start


def test_nmc_charge_increases_soc_and_clamps():
    battery = create_nmc_battery(SimulationConfig(parallel_cells=2), initial_soc=0.99)
    battery.apply_current(-40.0, 600.0)
    assert 0.0 <= battery.soc <= 1.0
    assert battery.soc == 1.0


def test_current_for_positive_power_is_positive():
    battery = create_lipo_battery(initial_soc=0.8)
    current = battery.current_for_power(500.0)
    assert current > 0


def test_current_for_negative_power_is_negative():
    battery = create_lipo_battery(initial_soc=0.8)
    current = battery.current_for_power(-100.0)
    assert current < 0
