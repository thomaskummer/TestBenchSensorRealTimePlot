import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib

import time
import csv
import pickle
import threading
import socket
from datetime import datetime

def move_figure(f, x, y):
    """Move figure's upper left corner to pixel (x, y)"""
	# move figure to upper screen
    backend = matplotlib.get_backend()
    if backend == 'TkAgg':
        f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    elif backend == 'WXAgg':
        f.canvas.manager.window.SetPosition((x, y))
    else:
        # This works for QT and GTK
        # You can also use window.setGeometry
        f.canvas.manager.window.move(x, y)


class animate():
    """ Class for live plotting the sensor output"""

    def __init__(self, fig, ax, host, port):

        self.host = host
        self.port = port
        self.start = time.time()
        self.volume_left = 140
        self.volume_right = 140

        self.T_end = 10 # t-axis length
        self.fig = fig # make public
        self.P_max = 150
        self.global_counter = 0
        self.global_time = []
        self.start_save = 0
        self.save_counter = 0

	# Only create empty plots/axes
        # Plot 1
        self.ax0 = ax[0, 0]
        self.ax0.set_title("Left Ventricle", fontsize=15)
        self.ax0.set_xlim([0, self.T_end+0.5])
        self.ax0.set_ylim([-2, self.P_max])
        self.ax0.set_ylabel("pressure [mmhg]", fontsize=15)
        self.ax0.set_xlabel("time [s]", fontsize=15)

        # 2
        self.ax1 = ax[0, 1]
        self.ax1.set_title("Right Ventricle", fontsize=15)
        self.ax1.set_xlim([0, self.T_end+0.5])
        self.ax1.set_ylim([-2, 150])
        self.ax1.set_ylabel("pressure [mmhg]", fontsize=15)
        self.ax1.set_xlabel("time [s]", fontsize=15)

        # 3
        self.ax2 = ax[0, 2]
        self.ax2.set_title("Patch vacuum",fontsize=15)
        self.ax2.set_xlim([0, self.T_end+0.5])
        self.ax2.set_ylim([-1, 0.1])
        self.ax2.set_ylabel("pressure [bar]", fontsize=15)
        self.ax2.set_xlabel("time [s]", fontsize=15)

        # 4
        self.ax3 = ax[1, 0]
        self.ax3.set_xlim([0, self.T_end+0.5])
        self.ax3.set_ylim([-200, 800])
        self.ax3.set_ylabel("flow rate [ml/s]", fontsize=15)
        self.ax3.set_xlabel("time [s]", fontsize=15)

        # 5
        self.ax4 = ax[1, 1]
        self.ax4.set_xlim([0, self.T_end+0.5])
        self.ax4.set_ylim([-200, 800])
        self.ax4.set_ylabel("flow rate [ml/s]", fontsize=15)
        self.ax4.set_xlabel("time [s]", fontsize=15)

        # 6
        self.ax5 = ax[1, 2]
        self.ax5.set_title("Volume", fontsize=15)
        self.ax5.set_xlim([0, 10])
        self.ax5.set_ylim([0, 200])
        self.ax5.set_ylabel("Volume [ml]", fontsize=15)
        self.ax5.set_xlabel("time [s]", fontsize=15)

	# Plug in empty data into plots
        # 1
        self.line, = self.ax0.plot([], [], label="lv", c='black', lw=2)
        #self.line1, = self.ax0.plot([], [], label="Test", c='blue', lw=2)
        self.line2, = self.ax0.plot([], [], label="pulm. vein", c="green", lw=2)
        self.line3, = self.ax0.plot([], [], label="compl. cha. air", c='red', lw=2)
        self.line4, = self.ax0.plot([], [], label="aorta", lw=2)
        # 2
        #self.line5, = self.ax1.plot([], [], label="Test", c='blue', lw=2)
        self.line6, = self.ax1.plot([], [], label="rv", c='black', lw=2)
        self.line7, = self.ax1.plot([], [], label="vena cava", c='green', lw=2)
        self.line8, = self.ax1.plot([], [], label="compl. cha. air", c='red', lw=2)
        self.line9, = self.ax1.plot([], [], label="pulm. art.", lw=2)
        # 3
        self.line10, = self.ax2.plot([], [], label="patch 1", c='blue', lw=2)
        self.line11, = self.ax2.plot([], [], label="patch 2", c='black', lw=2)
        # 4
        self.line12, = self.ax3.plot([], [], label="aortic valve", c="green", lw=2)
        self.line13, = self.ax3.plot([], [], label="mitral valve", c='blue', lw=2)
        # 5
        self.line14, = self.ax4.plot([], [], label="pulm. valve", c='black', lw=2)
        self.line15, = self.ax4.plot([], [], label="tricusp. valve", c='green', lw=2)
        # 6
        self.line16, = self.ax5.plot([], [],label="lv", c='black', lw=2)
        self.line17, = self.ax5.plot([], [], label="rv", c='green', lw=2)
# 1) add here line 18

	# legend location
        self.ax0.legend(loc='upper right')
        self.ax1.legend(loc='upper right')
        self.ax2.legend(loc='upper right')
        self.ax3.legend(loc='upper right')
        self.ax4.legend(loc='upper right')
        self.ax5.legend(loc='upper right')

	# create empty lists for data from raspi
        self.x = []
        self.y0 = []
        self.y1 = []
        self.y2 = []
        self.data_array = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.data_list = []
        self.y3 = []
        self.y4 = []
        self.y5 = []
        self.y6 = []
        self.y7 = []
        self.y8 = []
        self.y9 = []
        self.y10 = []
        self.y11 = []
        self.y12 = []
        self.y13 = []
        self.y14 = []
        self.y15 = []
        self.y16 = []
        self.y17 = []
        self.y18 = []
        self.y19 = []
        
        self.p = []
# 2) add here e.g. self.y14

        self.time = []
        self.start = time.time()

        self.j = 0

    # 
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
		    # reading data dumped by sendall function of client
                    self.data_array = pickle.loads(data)

    # initialization function: plot the background of each frame
    # no constructor
    # emtpy lines for animation class
    def init(self):
        self.line.set_data([], [])
        #self.line1.set_data([], [])
        self.line2.set_data([], [])
        self.line3.set_data([], [])
        self.line4.set_data([], [])
        #self.line5.set_data([], [])
        self.line6.set_data([], [])
        self.line7.set_data([], [])
        self.line8.set_data([], [])
        self.line9.set_data([], [])
        self.line10.set_data([], [])
        self.line11.set_data([], [])
        self.line12.set_data([], [])
        self.line13.set_data([], [])
        self.line14.set_data([], [])
        self.line15.set_data([], [])
        self.line16.set_data([], [])
        self.line17.set_data([], [])
# 3) add self.line18...

        return self.line, self.line2, self.line3, self.line4, self.line6, self.line7, self.line8, self.line9, self.line10, self.line11, self.line12, self.line13, self.line14, self.line15, self.line16, self.line17, 
# 4) return line 18

    def get_data(self, i):
        if (time.time()-self.start)>self.T_end:
        #if self.data_array[0]>= self.T_end:
            self.global_counter += 1

            self.x.pop(0)
            self.y0.pop(0)
            self.y1.pop(0)
            self.y2.pop(0)
            self.y3.pop(0)
            self.y4.pop(0)
            self.y5.pop(0)
            self.y6.pop(0)
            self.y7.pop(0)
            self.y8.pop(0)
            self.y9.pop(0)
            self.y10.pop(0)
            self.y11.pop(0)
            self.y12.pop(0)
            self.y13.pop(0)
            self.y14.pop(0)
            self.y15.pop(0)
            self.y16.pop(0)
            self.y17.pop(0)
            self.y18.pop(0)
            self.y19.pop(0)
# 5) y14.pop
            self.p.pop(0)

	# 1 for start save
        if int(self.start_save) == 1:
            self.data_list.append(self.data_array)
            self.save_counter = 0

	# 2 for end save
        if int(self.start_save) == 2 and self.save_counter == 0:
            self.dump()
            self.data_list = []
            self.save_counter += 1
        d1 = 0.020
        d2 = 0.010
        constant = (np.pi**2/(8.0*1000.0))/(1.0/d2**4-1.0/d1**4)
	# append new data from sensors
        self.y0.append(self.data_array[1])
        self.y1.append(self.data_array[2])
        self.y2.append(self.data_array[3])
        self.y3.append(self.data_array[4])
        self.y4.append(self.data_array[12])

        self.y5.append(self.data_array[11])
        self.y6.append(self.data_array[5])
        self.y7.append(self.data_array[6])
        self.y12.append(self.data_array[13]) 
        self.y13.append(self.data_array[14])

        R = 287.1
        T = 298.0
        h = 0.18
        d = 0.12
        h_2 = 0.07
        d_2 = 0.095
        v = d**2/4*np.pi*h
        v_2 = d_2**2/4*np.pi*h_2
        m_luft = (v-v_2)*1.18
        
        if time.time() - self.start > 15:

            p1_l = max(self.y3[-1],0.0001) * 133.1
            p2_l = max(self.y3[-3],0.0001) * 133.1
            p1_l_right = max(self.y12[-1],0.0001) * 133.1
            p2_l_right = max(self.y12[-3],0.0001) * 133.1

            delta_t = max(self.x[-1]-self.x[-3],0.08)

            flow = (self.y8[-7]+self.y8[-5]+self.y8[-3]+self.y8[-1]+((-1/p1_l+1/p2_l)*100000.0/delta_t*R*T*m_luft))/5
            self.y8.append(flow)
            if flow > 0:
                self.y14.append(flow)
                self.y15.append(0)
            else:
                self.y15.append(flow*-1.0)
                self.y14.append(0)
            flow2 = (self.y9[-7]+self.y9[-5]+self.y9[-3]+self.y9[-1]+((-1/p1_l_right+1/p2_l_right)*100000.0/delta_t*R*T*m_luft))/5
            self.y9.append(flow2)

            if flow2 > 0:
                self.y16.append(flow2)
                self.y17.append(0)
            else:
                self.y17.append(flow2*-1.0)
                self.y16.append(0)

            self.volume_left -= flow*delta_t*0.1
            self.volume_right -= flow2*delta_t*0.1
            self.y18.append(self.volume_left)
            self.y19.append(self.volume_right) 
        else:
            self.y8.append(0)
            self.y9.append(0)
            self.y14.append(0)
            self.y15.append(0)
            self.y16.append(0)
            self.y17.append(0)
            self.y18.append(self.volume_left)
            self.y19.append(self.volume_right)
     

        #self.y9.append(self.data_array[10])
        self.y10.append(self.data_array[15])
        self.y11.append(self.data_array[16])
        #print((self.y8[-1])*60/1000)
        #print(self.data_array[9])



# 6) self.y14...

	# random data for p-v-loop
        self.p.append(np.random.sample(1)*10.0)
        
        #self.x.append(time.time()-self.start)
	# x=time
        self.x.append(self.data_array[0])

	# axes limits, change with moving time
        if self.global_counter > 1:
            self.ax0.set_xlim([self.x[0],self.x[-1]+0.5])
            self.ax1.set_xlim([self.x[0],self.x[-1]+0.5])
            self.ax2.set_xlim([self.x[0],self.x[-1]+0.5])
            self.ax3.set_xlim([self.x[0],self.x[-1]+0.5])
            self.ax4.set_xlim([self.x[0],self.x[-1]+0.5])
            self.ax5.set_xlim([self.x[0],self.x[-1]+0.5])

	# copy to other variables, returning into emtpy lines
        x = self.x
        y0 = self.y0
        y1 = self.y1
        y2 = self.y2
        y3 = self.y3
        y4 = self.y4
        y5 = self.y5
        y6 = self.y6
        y7 = self.y7
        y8 = self.y8
        y9 = self.y9
        y10 = self.y10
        y11 = self.y11
        y12 = self.y12
        y13 = self.y13
        y14 = self.y14
        y15 = self.y15
        y16 = self.y16
        y17 = self.y17
        y18 = self.y18
        y19 = self.y19
# 7) self.y14

        p = self.p

        return x, y0, y1, y2, y3, y4, y5, y6, y7 , y8 ,y9 ,y10 ,y11 ,y12 ,y13 ,y14,y15,y16,y17,y18,y19,p,
# 8) return y14    

    # get data from above
    def animate(self, i):
        x, y0, y1, y2, y3, y4, y5, y6, y7 , y8 ,y9 ,y10 ,y11 ,y12 ,y13,y14,y15,y16,y17,y18,y19 ,p = self.get_data(i)
# 9) y14

	# eventually write data to plots
        self.line.set_data(x, y0)
        #self.line1.set_data(x, y1)
        self.line2.set_data(x, y2)
        self.line3.set_data(x, y3)
        self.line4.set_data(x, y4)

        #self.line5.set_data(x, y5)
        self.line6.set_data(x, y6)
        self.line7.set_data(x, y7)
        self.line8.set_data(x, y12)
        self.line9.set_data(x, y13)

        self.line10.set_data(x, y10) #(x,y12)
        self.line11.set_data(x, y11) #(x,y13)

        R = 461.4
        T = 293.0
        #flow
 
        self.line12.set_data(x, y14)
        self.line13.set_data(x, y15)

        self.line14.set_data(x, y16)
        self.line15.set_data(x, y17)

        self.line16.set_data(x, y18)
        self.line17.set_data(x, y19)
# 10) self.line18.set_data(x, y14)


        return self.line, self.line2, self.line3, self.line4, self.line6, self.line7, self.line8, self.line9, self.line10, self.line11, self.line12, self.line13, self.line14, self.line15, self.line16, self.line17, 
# 11) line18
    
    # dump file for saving with buttons 1 and 2
    def dump(self):
        date = "output_{}.csv".format(datetime.now().strftime('%Y%b%d_%H%M%S'))
        with open(date, 'w') as outcsv: #change 'w' to 'a' if we just want to append
            #configure writer to write standard csv file
            writer = csv.writer(outcsv, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Time', 'lv', 'Test','pulm. vein','compl. cha.','aorta','Test', 'rv', 'vena cava', 'compl. cha. air', 'pulm. art.', 'patch 1', 'patch 2', 'aortic valve', 'mitral valve'])

# 12) export sensor ...

            for item in self.data_list:
                #Write item to outcsv
                writer.writerow([item[0],item[1],item[2],item[3],item[4],item[12], item[11],item[5],item[6],item[13],item[14], item[15], item[16], 1,1])
        print("Data saved to {}!".format(date))

    def save(self):
        while True:
            self.start_save = input()

# 13) open sensors in client.py


if __name__ == '__main__':

    HOST = '169.254.115.231' #ip raspi
    #HOST = '127.0.0.1'
    PORT = 6676
	
#subplotsh
    fig, ax = plt.subplots(2, 3, sharex=False, sharey=False, figsize=(20, 20))
    fig.set_tight_layout(True)
    move_figure(fig, 0, 0)

# initialize animate object
    a = animate(fig, ax, HOST, PORT)
# thread for plotting and thread for comunicating with raspi
    thread = threading.Thread(target=a.data_stream)
    thread.deamon = False
    thread.start()

# thread raspi
    thread2 = threading.Thread(target=a.save)
    thread2.deamon = False
    thread2.start()

    print("Start client")

# plug animate object a into matplotlib animation object
    anim = animation.FuncAnimation(fig, a.animate, init_func=a.init, interval=20, blit=True)
    plt.show()
