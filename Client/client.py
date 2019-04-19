#!/usr/bin/env python3
import pickle
from switch import I2C_SW
import socket
import time


class Client(object):
    """This class describes the client running on the raspberry pi """

    def __init__(self, address_mp, address_sensor, nb_sensors, host, port, i2c_sw):
        self.address_mp = address_mp
        self.address_sensor = address_sensor
        self.nb_sensors = nb_sensors
        self.host = host
        self.port = port
        self.i2c_sw = i2c_sw

    def client(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            start = time.time()
            while True:
                data = []
                t = time.time() - start
                data.append(t)
                if t >= 20.0:
                    start = time.time()
                    t = time.time() - start
                data.append(t)

                for i in range(self.nb_sensors):
                    self.i2c_sw.chn(i)
                    sensor = self.i2c_sw.get_mmhg(self.i2c_sw.get_data())
                    data.append(sensor)
                    time.sleep(0.001)
                    s.sendall(pickle.dumps(data))


if __name__ == '__main__':

    address_muliplexer = 0x70
    address_sensor = 0x28
    i2c_switch = I2C_SW("I2C switch 0", address_muliplexer, 1, address_sensor)
    HOST = '169.254.115.231'  # The server's hostname or IP address
    PORT = 6677

    C = Client(address_muliplexer,address_sensor,6,HOST,PORT,i2c_switch)
    C.client()
