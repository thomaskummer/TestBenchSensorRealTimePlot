#!/bin/bash 
ssh pi@169.254.230.24 python3 /home/pi/Desktop/digital_sensor_read_out/Client/client.py &

python3 Server/server.py

