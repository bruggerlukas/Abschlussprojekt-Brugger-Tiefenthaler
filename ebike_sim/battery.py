"""Einfache Akkumodelle für LiPo und NMC."""

import logging
from math import sqrt
import numpy as np

from .config import SimulationConfig

LOGGER = logging.getLogger(__name__)

LIPO_SOC = np.array([0.00, 0.04, 0.09, 0.13, 0.17, 0.21, 0.26, 0.30, 0.40, 0.52, 0.64, 0.76, 0.88, 1.00])
LIPO_OCV = np.array([32.00, 35.87, 36.85, 37.56, 37.87, 38.28, 38.81, 39.05, 39.55, 40.27, 40.70, 41.16, 41.65, 42.00])
NMC_SOC = np.array([0.00, 0.04, 0.09, 0.13, 0.17, 0.21, 0.26, 0.30, 0.40, 0.52, 0.64, 0.76, 0.88, 1.00])
NMC_OCV = np.array([32.00, 32.61, 33.17, 33.85, 34.24, 34.66, 35.39, 35.65, 36.65, 37.64, 38.91, 40.14, 41.08, 42.00])


class BatteryStepResult:
    """Speichert das Ergebnis eines Akkuschrittes."""

    def __init__(self, current_a, voltage_v, soc, requested_power_w,
                 effective_power_w, heat_loss_w,
                 brake_resistor_power_w, unmet_power_w):
        self.current_a = current_a
        self.voltage_v = voltage_v
        self.soc = soc
        self.requested_power_w = requested_power_w
        self.effective_power_w = effective_power_w
        self.heat_loss_w = heat_loss_w
        self.brake_resistor_power_w = brake_resistor_power_w
        self.unmet_power_w = unmet_power_w


class BatteryPack:
    """Ein Akkupack mit Kennlinie und Innenwiderstand."""

    def __init__(self, name, capacity_nom_ah, internal_resistance_ohm,
                 soc_curve, ocv_curve_v, initial_soc=1.0,
                 max_discharge_current_a=120.0,
                 max_charge_current_a=40.0,
                 temperature_c=25.0):
        if capacity_nom_ah <= 0:
            raise ValueError("Die Akkukapazität muss größer 0 sein.")
        if internal_resistance_ohm < 0:
            raise ValueError("Der Innenwiderstand darf nicht negativ sein.")

        self.name = name
        self.capacity_nom_ah = capacity_nom_ah
        self.internal_resistance_ohm = internal_resistance_ohm
        self.soc_curve = soc_curve
        self.ocv_curve_v = ocv_curve_v
        self.initial_soc = initial_soc
        self.max_discharge_current_a = max_discharge_current_a
        self.max_charge_current_a = max_charge_current_a
        self.temperature_c = temperature_c
        self.soc = float(np.clip(initial_soc, 0.0, 1.0))

    @property
    def effective_capacity_ah(self):
        if self.temperature_c < 25:
            factor = 1 - 0.005 * (25 - self.temperature_c)
        else:
            factor = 1 - 0.001 * (self.temperature_c - 25)

        factor = float(np.clip(factor, 0.70, 1.05))
        return self.capacity_nom_ah * factor

    @property
    def effective_resistance_ohm(self):
        cold_factor = 1 + 0.02 * max(0, 25 - self.temperature_c)
        warm_factor = 1 + 0.005 * max(0, self.temperature_c - 25)
        return self.internal_resistance_ohm * cold_factor * warm_factor

    def set_temperature(self, temperature_c):
        self.temperature_c = float(temperature_c)