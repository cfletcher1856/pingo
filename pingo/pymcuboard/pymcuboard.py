import os
import pingo
from pingo.board import Board, AnalogInputCapable, PwmOutputCapable, DigitalPin, AnalogPin, PwmPin


PIN_STATES = {
    False: 0,
    True: 1,
    0: 0,
    1: 1,
    pingo.LOW: 0,
    pingo.HIGH: 1,
}

PIN_MODES = {
    pingo.IN: 0,
    pingo.OUT: 1,
}

class Pymcuboard(Board, AnalogInputCapable, PwmOutputCapable):
    def __init__(self):
        try:
            import pymcu
        except ImportError:
            raise ImportError('pingo.pymcuboard.Pymcuboard requires pymcu installed')

        super(Pymcuboard, self).__init__()
        self.board = pymcu.mcuModule()

        self._add_pins(
            [DigitalPin(self, location)
                for location in range(1, 20)] +
            [AnalogPin(self, 'A%s' % location, resolution=10)
                for location in range(1, 7)] +
            [PwmPin(self, location)
                for location in range(1, 6)
            ]
        )

    def cleanup(self):
        if hasattr(self, 'board'):
            try:
                self.board.close()
            except AttributeError:
                pass

    def __repr__(self):
        cls_name = self.__class__.__name__
        return '<{cls_name} {self.port!r}>'.format(**locals())

    @property
    def port(self):
        if 'ttyUSB0' in os.listdir('/dev/'):
            return os.path.join(os.path.sep, 'dev', 'ttyUSB0')

    def info(self):
        print self.board.mcuInfo()

    def version(self):
        print self.board.mcuVersion()

    def _set_pin_mode(self, pin, mode):
        if isinstance(pin, DigitalPin):
            print pin.__dict__
            self.board.digitalState(
                pin.location,
                PIN_MODES[mode]
            )

    def _get_pin_state(self, pin):
        return pin._state

    def _set_pin_state(self, pin, state):
        if isinstance(pin, DigitalPin):
            if state == pingo.HIGH:
                self.board.pinHigh(
                    pin.location
                )
            else:
                self.board.pinLow(
                    pin.location
                )

    def _set_analog_mode(self, pin, mode):
        # Cannot do this on pyMcu
        pass

    def _get_pin_value(self, pin):
        pin_id = int(pin.location[1:])
        return self.board.analog_read(pin_id)

    def _set_pwm_mode(self, pin):
        pass

    def _get_pwm_duty_cycle(self, pin):
        pass

    def _set_pwm_duty_cycle(self, pin, value):
        pass

# Available Digital Pins  : 1 - 19
# Available Analog Pins   : 1 - 6
# Analog Value Range      : 0 - 1023
# PWM Pins                : 1 - 5
# PWM Duty Cycle Range    : 0 - 1023
