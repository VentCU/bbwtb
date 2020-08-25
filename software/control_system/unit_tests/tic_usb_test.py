import sys
sys.path.append('/home/pi/Workspace/bbwtb/software/control_system')
from actuators.tic_usb import *
import time

if __name__ == '__main__':
    
    ticdev = TicDevice()
    ticdev.open(vendor=0x1ffb, product_id=0x00CB)
    
    start = time.time()
    ticdev.set_target_position(-12800)
    v = ticdev.get_variables()
    log.debug(ticdev.variables['current_position'])
    
    ticdev.wait_for_move_complete()
    print(time.time() - start)
    #ticdev.set_target_position(0)
