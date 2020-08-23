'''
# max accel: 1000000 pulses/s^2
# max speed: 50000 pulses/s
# 1/64 step
# pos target: +/- 12800
# 0.87s ttt (time to target) on pid_tuning.py
# mv_enc_pos_test: ttt: 1s true: 0.4s
# performance increase: 2.5x

PID_P_GAIN = 2300000
PID_I_GAIN = 0
PID_D_GAIN = 0

PID_TIME_SCALE_FACTOR = 0.01555
'''
# max accel: 1000000 pulses/s^2
# max speed: 30000 pulses/s
# 1/64 step

PID_P_GAIN = 1070000
PID_I_GAIN = 0
PID_D_GAIN = 0 # 100000

# PID_TIME_SCALE_FACTOR = 0.01555 # for 100 ticks (half rotation)
PID_TIME_SCALE_FACTOR = 0.00725 # for 250 ticks 
# PID_TIME_SCALE_FACTOR = 0.00615 # for 300 ticks
# PID_TIME_SCALE_FACTOR = 0.00415 # for 500 ticks
# PID_TIME_SCALE_FACTOR = 0.0035 # for 650 ticks

# PID_P_GAIN = 5200000
# PID_I_GAIN = 0
# PID_D_GAIN = 0 # 100000
