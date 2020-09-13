#!/bin/bash

mkdir Workspace
git clone https://github.com/VentCU/bbwtb.git

# https://stackoverflow.com/questions/4880290/how-do-i-create-a-crontab-through-a-script/9625233#9625233
# https://askubuntu.com/questions/1152704/run-sudo-vulkaninfo-at-startup-all-users
(crontab -l 2>/dev/null; echo "@reboot $HOME/Workspace/bbwtb/software/control_system/start-script") | crontab -

sudo apt-get update
sudo pip3 install --upgrade pip
sudo pip3 install Adafruit-Blinka
sudo apt install realvnc-vnc-server realvnc-vnc-viewer                  
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