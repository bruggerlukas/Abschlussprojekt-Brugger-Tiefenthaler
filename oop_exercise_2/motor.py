class MotorMVP:
    def get_current_draw(self, power: float, voltage: float) -> float:
        """
        Minimal viable product for the Motor class.
        Always returns a constant current draw of 5 amps, regardless of the input power and voltage.
        """
        return 5


class Motor:
    def __init__(self, efficiency: float = 0.9):
        self.efficiency = max(0.0, min(efficiency, 1.0))

    def get_current_draw(self, power: float, voltage: float) -> float:
        """
        Calculate the current draw of the motor based on the power and voltage.

        :param power: Power in watts
        :param voltage: Voltage in volts
        :return: Current draw in amps
        """
        if voltage <= 0:
            return 0.0

        return power / (voltage * self.efficiency)
