## Dependencies

`smbus2`

`pySerial`

## Please READ regarding I2C

The example C code below uses the I²C API provided by the Linux kernel to send and receive data from a Tic. It 
demonstrates how to set the target position of the Tic and how to read variables from it. This code only works on Linux.

If you are using a Raspberry Pi, please note that the Raspberry Pi’s hardware I²C module has a bug that causes this 
code to not work reliably. As a workaround, we recommend enabling the i2c-gpio overlay and using the I²C device that 
it provides. To do this, add the line dtoverlay=i2c-gpio to /boot/config.txt and reboot. The overlay documentation has 
information about the parameters you can put on that line, but those parameters are not required. Connect the Tic’s 
SDA line to GPIO23 and connect the Tic’s SCL line to GPIO24. The i2c-gpio overlay creates a new I²C device which is 
usually named /dev/i2c-3, and the code below uses that device. To give your user permission to access I²C busses without 
being root, you might have to add yourself to the i2c group by running sudo usermod -a -G i2c $(whoami) and restarting.

You might notice that the Tic only performs the desired movement for about a second before it stops moving and the red 
LED turns on, indicating an error. This is because of the Tic’s command timeout feature: by default, the Tic’s 
“Command timeout” error will happen if it does not receive certain commands periodically (see Section 5.4 for details), 
causing the motor to stop. You can send a “Reset command timeout” command every second to get around this, or you can 
disable the command timeout feature using the Tic Control Center: uncheck the “Enable command timeout” checkbox in 
the “Serial” box.