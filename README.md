# Live Plotting of Multiple Sensors


This repo is about reading of multiple digital sensors with the same i2c address and their live 
plotting. 

## What you need:
In brackets i list what i used. 
1. Raspberry pi (model 3B+) with experimental box, external keyboard, mouse and display for pi-setup
2. Digital Sensors with I2C output (Honeywell pressure Sensor ABPDRRT005PG2A5)
3. Multiplexer (SparkFun Qwiic Mux Breakout - 8 Channel (TCA9548A))
4. SparkFun Qwiic HAT for Raspberry Pi
5. Network switch  
6. Laptop 

## Step 1: Set up the Raspberry 
There are several sources available on the internet explaining how to set up 
the Raspberry pi correctly. [Here](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up)
is an example. Important do not forget [to enable](https://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi/)
the I2C interface.

Copy the client folder on the raspberry.

## Step 2: Connect Sensors to Raspberry
To communicate with multiple sensors of the same address i used a mulhttps://gitlab.ethz.ch/projects/newtiplexer, to
switch between the different channels. Follow these steps to connect the sensors over
the Multiplexer to the Raspberry. 

TODO: Put here images

1. Connect SparkFun Qwiic HAT to Raspberry 
2. Connect Multiplexer to SparkFun Qwiic HAT
3. Connect Sensors to Multiplexer SCL to SCL and SDL to SDL. If you are using sensors which 
need more than 3.3 Voltage, you have to either connect them to a external voltage source 
or in the case of 5V you can get it from the Raspberry.

## Step 3: Set up Python 
I would recommend to use a virtual environment e.g [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
with python 3.6.
 
Open Terminal on you laptop and generate virtual env with the name sensor:
```bat
conda create -n sensor python=3.6
```
Source the sensor env:
```bat
source activate sensor
```
Install the required libraries:
```bat
pip install -r req.txt
```

Do the same steps on the Raspberry pi. You can delete the matplotlib line 
in the req.txt file since we do not need it on the Raspberry. 

At this point you should be able to test the sensors if they are working correctly. 
On the raspberry open a terminal and run the switch.py file.

```bat
source activate sensor
cd client
python switch.py
```

The output should be: "Successfully read every sensor" and a time. If you got an error 
check all connection. Proceed only if the sensors are working.

## Connect your laptop and the Raspberry
Connect the Raspberry over ethernet to the Network switch and the Network switch 
to your laptop. 

Figure out the ip address and the Mac address of the Raspberry. Therefore type the following command on the 
Raspberry's terminal. 
```bat
ifconfig
```

TODO add screen shot

On your laptop open Network settings and add a new wired connection. Copy the mac address
and the ip address to the corresponding places and change the last number of the ip address.
 

## Sensor readout and live plot

1. On the Raspberry open the client.py file and change the HOST name to the ip address of your local 
computer (the same as the ip address of the Raspberry except the last number, which you changed 
before).

2. On your local computer open the server.py file and change the HOST name to the HOST name you 
used in the step before.

3. On your laptop start the server:
```bat
python server.py
```

4. On the Raspberry start the client:
```bat
python client.py
```

You should now see the live plots of the sensors you connected. 

## Saving data

If you want to store data, just type a 1 in the terminal where the server is running. 
By typing a 2 you stop the saving and the data is stored in an csv file. 