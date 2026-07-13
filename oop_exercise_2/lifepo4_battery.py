from battery_pack import BatteryPack


class LiFePO4BatteryPack(BatteryPack):
    def voltage(self, current=0.0):
        open_circuit_voltage = self.Vmin + (self.soc**0.3) * (self.Vmax - self.Vmin)
        return open_circuit_voltage - self.R_int * current
