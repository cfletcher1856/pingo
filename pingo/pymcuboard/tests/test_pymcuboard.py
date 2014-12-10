import unittest

import pingo
from pingo.test import level0
from pingo.detect import has_module, check_board

running_on_pymcu = check_board(pingo.pymcuboard.Pymcuboard)


class PymcuTest(unittest.TestCase):

    def setUp(self):
        self.board = pingo.pymcuboard.Pymcuboard()

        self.vdd_pin_number = 0
        self.digital_output_pin_number = 13
        self.digital_input_pin_number = 8
        self.total_pins = 26

    def tearDown(self):
        self.board.cleanup()


@unittest.skipIf(not running_on_pymcu, "pyMcu not detected")
@unittest.skipIf(
    not has_module('pymcu'), "pingo.pymcuboard requires pymcu installed")
class PymcuBasics(PymcuTest, level0.BoardBasics):
    pass


@unittest.skipIf(not running_on_pymcu, "pyMcu not detected")
@unittest.skipIf(
    not has_module('pymcu'), "pingo.pymcuboard requires pymcu installed")
class PymcuExceptions(PymcuTest, level0.BoardExceptions):
    pass


if __name__ == '__main__':
    unittest.main()
