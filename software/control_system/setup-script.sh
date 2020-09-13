#!/bin/bash

printf "Setting Up VentCU Device\n"
if ! pgrep -x "pigpiod" > /dev/null
then
	sudo pigpiod	
fi

sudo apt-get update
sudo pip3 install --upgrade pip
sudo pip3 install Adafruit-Blinka                  
sudo pip3 install adafruit-circuitpython-ads1x15        
sudo pip3 install adafruit-circuitpython-busdevice      
sudo pip3 install adafruit-circuitpython-mcp3xxx        
sudo pip3 install Adafruit-PlatformDetect               
sudo pip3 install Adafruit-PureIO                          
sudo pip3 install envirophat                            
sudo pip3 install ExplorerHAT                           
sudo pip3 install gpiozero                              
sudo pip3 install numpy                                   
sudo pip3 install pigpio                                
sudo pip3 install PyQt5                            
sudo pip3 install pyqtgraph                             
sudo pip3 install pyserial                                 
sudo pip3 install RPi.GPIO                              
sudo pip3 install smbus2                             
