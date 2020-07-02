#
# Pressure Sensor Class
# Implemented with an analog-digital converter communicating over I2C
#
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from time import sleep
import matplotlib.pyplot as plt
import numpy as np
import logging

plt_logger = logging.getLogger('matplotlib')
plt_logger.setLevel(logging.CRITICAL)


class PressureSensor:

    def __init__(self):

        print("NOT IMPLEMENTED")
        # default i2c port set to 48
        # default i2c communication on pins 3, 5 of pi
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(self.i2c)      

    # Returns raw differential reading from pressure sensor
    # Pressure transducer hard wired to ADC analog pins 0, 1
    def get_raw_value(self):
        chan = AnalogIn(self.ads, ADS.P0, ADS.P1)
        raw_value = chan.value
        return raw_value

    # TODO: Implement
    def get_pressure(self, raw_value):
        # remove raw2data later
        pressure = raw2data(raw_value)
        return pressure

#  

# takes channel data from transducer and coverts to psi
def raw2data(value):
    output_max = 1 #psi
    output_min = -1 #psi
    pressure_max = 1
    pressure_min = -1
    output = (((value - output_min) * 
              (pressure_max - pressure_min))/
              (output_max - output_min)) + pressure_min
    return output

def i2c_test():
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)

    values = []
    ctr = 0
    chan0 = AnalogIn(ads, ADS.P0, ADS.P1)
    chan1 = AnalogIn(ads, ADS.P2, ADS.P3)
#    chan2 = AnalogIn(ads, ADS.P2)
#    chan3 = AnalogIn(ads, ADS.P3)
    while(ctr < 5):
        sleep(0.1)
        pressure = raw2data(chan0.value)
        values.append(pressure)
        ctr += 1
        print("ch0: ", pressure, chan0.voltage)
#        print("ch1: ", chan1.value, chan1.voltage)
#        print("ch2: ", chan2.value, chan2.voltage)
#        print("ch3: ", chan3.value, chan3.voltage)
        
    time = np.arange(ctr)
    # plt.plot(time, np.asarray(values))
    # plt.show()

if __name__ == "__main__":
    # i2c_test()
    i2c_test = PressureSensor()
    values_raw = []
    values_conv = []
    ctr = 0
    while (ctr < 100):
        sleep(0.01)
        raw = i2c_test.get_raw_value()
        conv = i2c_test.get_pressure(raw)
        values_raw.append(raw)
        values_conv.append(conv)
        # print( f"Raw: {raw} Conv: {conv}")
        ctr += 1
    time = np.arange(ctr)
    
    fd = open('unit_tests/ps_log.csv', 'w')   
    header = 'Time (0.01s), Raw, Conv'
    fd.write(header)
    fd.write('\n')
    for time, raw, conv in zip(ctr, values_raw, values_conv):
        line = f"{time}, {raw}, {conv}"
        fd.write(line)
        fd.write('\n')

    plt.plot(time, np.asarray(values_raw))
    plt.plot(time, np.asarray(values_conv))
    plt.show()

