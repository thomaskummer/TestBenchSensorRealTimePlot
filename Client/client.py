#!/usr/bin/env python3
import pickle
from switch import I2C_SW
import socket
import time


class Client(object):
    """This class describes the client running on the raspberry pi """

    def __init__(self, address_mp, address_sensor, nb_sensors, host, port, i2c_sw,i2c_switch2,i2c_switch3):
        self.address_mp = address_mp
        self.address_sensor = address_sensor
        self.nb_sensors = nb_sensors
        self.host = host
        self.port = port
        self.i2c_sw = i2c_sw
        self.i2c_sw2 = i2c_switch2
        self.i2c_sw3 = i2c_switch3

    def client(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            start = time.time()
            while True:
                data = []
                t = time.time() - start
                if t >= 100:
                    start = time.time()
                    t = time.time() - start
                data.append(t)

                for i in range(0,8):
                    self.i2c_sw.chn(i)
                    sensor = self.i2c_sw.get_mmhg(self.i2c_sw.get_data())
                    data.append(sensor)
                   # time.sleep(0.005)
                self.i2c_sw._rst()
                for i in range(4):
                    self.i2c_sw2.chn(i)
                    sensor2 = self.i2c_sw2.get_mmhg(self.i2c_sw2.get_data())
                    data.append(sensor2)
                   # time.sleep(0.005)
                self.i2c_sw2._rst()
                for i in range(6,8):
                    self.i2c_sw3.chn(i)
                    sensor3 = self.i2c_sw3.get_mmhg_underpressure(self.i2c_sw3.get_data())
                    data.append(sensor3)
                self.i2c_sw3._rst()
                s.sendall(pickle.dumps(data))


if __name__ == '__main__':
    time.sleep(5)
    address_multiplexer = 0x70
    address_multiplexer2 = 0x71
    address_multiplexer3 = 0x72
    address_sensor = 0x28
    address_sensor2 = 0x68
    i2c_switch = I2C_SW("I2C switch 0", address_multiplexer, 1, address_sensor)
    i2c_switch2 = I2C_SW("I2C switch 1", address_multiplexer2,1,address_sensor)
    i2c_switch3 = I2C_SW("I2C switch 2",address_multiplexer3,1,address_sensor2)
    HOST = '169.254.115.231'  # The server's hostname or IP address
    PORT = 6676

    C = Client(address_multiplexer,address_sensor,6,HOST,PORT,i2c_switch,i2c_switch2,i2c_switch3)
    C.client()
