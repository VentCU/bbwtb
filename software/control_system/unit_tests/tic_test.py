from actuators.tic_usb import *
import time

if __name__ == '__main__':
    
    ticdev = TicDevice()
    ticdev.open(vendor=0x1ffb, product_id=0x00CB)
    
    start = time.time()
    ticdev.set_target_position(1000)
    v = ticdev.get_variables()
    log.debug(ticdev.variables['current_position'])
    
    print(time.time() - start)