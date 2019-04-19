#!/usr/bin/python
# TCA9548A I2C multiplexer
# I2C Address: 70 through 77
# Channel: 0 - 7
 
import smbus
import time
 
class I2C_SW(object):
    """
    Class for switching between the channels of the SparkFun Qwiic Mux Breakout - 8 Channel (TCA9548A)

    Args:
        name: Name of the I2C switch
        address: Address of the Qwiic Mux Breakout, default 0x70
        bus_nr: Bus number , default 1
        address_sensor: I2C address of the sensors
    """

    def __init__(self, name, address, bus_nr, address_sensor):
        self.name = name
        self.address = address
        self.bus_nr = bus_nr
        self.bus = smbus.SMBus(bus_nr)
        self.address_sensor = address_sensor
 
    def chn(self, channel):
        """Change to i2c channel 0..7"""
        self.bus.write_byte(self.address,2**channel)
 
    def _rst(self):
        """Block all channels read only the main I2c (on which is the address SW)"""
        self.bus.write_byte(self.address,0)

    def _all(self):
        """Read all 8 channels"""
        self.bus.write_byte(self.address,0Xff)

    def get_data(self):
        """Get the raw data of the Sensor"""
        # sends i2c address & read bit, returns two 8 bit bytes as lsb, msb
        ans=self.bus.read_word_data(self.address_sensor,0x01) 
        # byte swap 'em because abp sends msb, lsb                                      
        output=(((ans & 0x00FF) << 8) + ((ans & 0xFF00) >> 8))
        return output

    def get_mmhg(self, output):
        """"Transfers the raw data from get_data into mmHg"""
        # These calculations are from the datasheet of honeywell pressure sensors
        output_min = 1638.0
        output_max = 14746.0
        pressure_max = 5.0 #psi
        pressure_min = 0.0 #psi
        psi = (output-output_min)*(pressure_max-pressure_min)/(output_max-output_min) + pressure_min
        mmhg = psi*51.71493256
        return mmhg


if __name__ == '__main__':
    # How long does it take to read out all sensors once?
    SW = I2C_SW('I2C switch 0', 0X70, 1, 0x28)
    nb_sensors = 6
    pressure_list = []

    start = time.time()
    for i in range(nb_sensors):
        SW.chn(i)
        output = SW.get_data()
        pressure_list.append(SW.get_mmhg(output))

    time_ = time.time() - start
    print("Successfully read every sensor")
    print(time)
