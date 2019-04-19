#!/usr/bin/env python3
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import time
import csv
import pickle
import threading
import socket
from datetime import datetime


class animate():
    """ Class for live plotting the sensor output"""

    def __init__(self, fig, ax, host, port):

        self.host = host
        self.port = port

        self.T_end = 5
        self.fig = fig
        self.P_max = 150
        self.global_counter = 0
        self.global_time = []
        self.start_save = 0
        self.save_counter = 0

        self.ax0 = ax[0, 0]
        self.ax0.set_title("Left Ventricle", fontsize=15)
        self.ax0.set_xlim([0, self.T_end+0.5])
        self.ax0.set_ylim([-2, self.P_max])
        self.ax0.set_ylabel("Pressure [mmhg]", fontsize=15)
        self.ax0.set_xlabel("Time [s]", fontsize=15)

        self.ax1 = ax[0, 1]
        self.ax1.set_title("Right Ventricle", fontsize=15)
        self.ax1.set_xlim([0, self.T_end+0.5])
        self.ax1.set_ylim([-2, self.P_max])
        self.ax1.set_ylabel("Pressure [mmhg]", fontsize=15)
        self.ax1.set_xlabel("Time [s]", fontsize=15)

        self.ax2 = ax[1, 0]
        self.ax2.set_title("Right Ventricle",fontsize=15)
        self.ax2.set_xlim([0, self.T_end+0.5])
        self.ax2.set_ylim([-2, self.P_max])
        self.ax2.set_ylabel("Pressure [mmhg]", fontsize=15)
        self.ax2.set_xlabel("Time [s]", fontsize=15)

        self.ax3 = ax[1, 1]
        self.ax3.set_title("Right Ventricle", fontsize=15)
        self.ax3.set_xlim([0, self.T_end+0.5])
        self.ax3.set_ylim([-2, self.P_max])
        self.ax3.set_ylabel("Pressure [mmhg]", fontsize=15)
        self.ax3.set_xlabel("Time [s]", fontsize=15)

        self.line, = self.ax0.plot([], [], label="Pressure 0", c='blue', lw=2)
        self.line1, = self.ax1.plot([], [], label="Pressure 1", c='black', lw=2)
        self.line2, = self.ax2.plot([], [], label="Pressure 2", c="green", lw=2)
        self.line3, = self.ax3.plot([], [], label="Pressure 3", c='blue', lw=2)
        self.line4, = self.ax1.plot([], [], label="Pressure 4", c='black', lw=2)
        self.line5, = self.ax1.plot([], [], label="Pressure 5", c='green', lw=2)
        #self.ax1.legend(loc='upper right')
        #self.ax0.legend(loc='upper right')

        self.x = []
        self.y0 = []
        self.y1 = []
        self.y2 = []
        self.data_array = np.array([0,0,0,0,0,0,0])
        self.data_list = []
        self.y3 = []
        self.y4 = []
        self.y5 = []

        self.time = []
        self.start = time.time()

        self.j = 0

    def data_stream(self):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by ', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    self.data_array = pickle.loads(data)

    # initialization function: plot the background of each frame
    def init(self):
        self.line.set_data([], [])
        self.line1.set_data([], [])
        self.line2.set_data([], [])
        self.line3.set_data([], [])
        self.line4.set_data([], [])
        self.line5.set_data([], [])
        return self.line, self.line1, self.line2, self.line3, self.line4, self.line5,

    def get_data(self, i):
        if (time.time()-self.start)>self.T_end:
            self.global_counter += 1

            self.x.pop(0)
            self.y0.pop(0)
            self.y1.pop(0)
            self.y2.pop(0)
            self.y3.pop(0)
            self.y4.pop(0)
            self.y5.pop(0)

        if int(self.start_save) == 1:
            self.data_list.append(self.data_array)
            self.save_counter = 0
        if int(self.start_save) == 2 and self.save_counter == 0:
            self.dump()
            self.data_list = []
            self.save_counter += 1

        self.y0.append(self.data_array[1])
        self.y1.append(self.data_array[2])
        self.y2.append(self.data_array[3])
        self.y3.append(self.data_array[4])
        self.y4.append(self.data_array[5])
        self.y5.append(self.data_array[6])
        
        self.x.append(time.time()-self.start)
        if self.global_counter > 1:
            self.ax0.set_xlim([self.x[0],self.x[-1]+0.5])

        x = self.x
        y0 = self.y0
        y1 = self.y1
        y2 = self.y2
        y3 = self.y3
        y4 = self.y4
        y5 = self.y5

        return x, y0, y1, y2, y3, y4, y5,
    
    def animate(self, i):
        x, y0, y1, y2, y3, y4, y5 = self.get_data(i)
        self.line.set_data(x, y0)
        self.line1.set_data(x, y1)
        self.line2.set_data(x, y2)
        self.line3.set_data(x, y3)
        self.line4.set_data(x, y4)
        self.line5.set_data(x, y5)

        return self.line, self.line1,self.line2, self.line3,self.line4,self.line5,
    
    def dump(self):
        date = "output_{}.csv".format(datetime.now().strftime('%Y%b%d_%H%M%S'))
        with open(date, 'w') as outcsv: #change 'w' to 'a' if we just want to append
            #configure writer to write standard csv file
            writer = csv.writer(outcsv, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Time', 'Sensor0', 'Sensor1','Sensor2','Sensor3','Sensor4','Sensor5'])
                
            for item in self.data_list:
                #Write item to outcsv
                writer.writerow([item[0],item[1],item[2],item[3],item[4],item[5],item[6]])
        print("Data saved to {}!".format(date))

    def save(self):
        while True:
            self.start_save = input()


if __name__ == '__main__':

    #HOST = '169.254.115.231'
    HOST = '127.0.0.1'
    PORT = 6677

    fig, ax0 = plt.subplots(2, 2, sharex=True, sharey=False, figsize=(10, 10))
    fig.set_tight_layout(True)
    a = animate(fig, ax0, HOST, PORT)
    thread = threading.Thread(target=a.data_stream)
    thread.deamon = False
    thread.start()

    thread2 = threading.Thread(target=a.save)
    thread2.deamon = False
    thread2.start()

    print("Start client")
    anim = animation.FuncAnimation(fig, a.animate, init_func=a.init, interval=10, blit=True)
    plt.show()
