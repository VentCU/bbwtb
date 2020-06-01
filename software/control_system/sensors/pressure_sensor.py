#
# Pressure Sensor Class
#
#
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from time import sleep
import matplotlib.pyplot as plt
import numpy as np


class PressureSensor:

    def __init__(self):

        print("NOT IMPLEMENTED")
        pass

    # TODO: Implement
    def get_raw_value(self):

        pass

    # TODO: Implement
    def get_pressure(self):

        pass

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

if __name__ == "__main__":
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
    plt.plot(time, np.asarray(values))
    plt.show()
