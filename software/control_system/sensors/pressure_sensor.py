#
# Pressure Sensor Class
#
#

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


class PressureSensor:

    def __init__(self):

        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        cs = digitalio.DigitalInOut(board.D5)
        self.mcp = MCP.MCP3008(spi, cs)

        pass

    # TODO: Test
    def get_raw_value(self):

        channel = AnalogIn(self.mcp, MCP.P0)

        return channel.value, channel.voltage

    def get_pressure(self):

        value, voltage = self.get_raw_value()

        # TODO calculations

        return -1
