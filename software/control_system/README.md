# VERSION 0.1 BETA RELEASE
## 9/11/20 (never forget)


## Init New State:
check clock, current, pressure while transition conditions are not met
set time elapsed to 0
start clock
measure, write pressure as indicated in screen
continuously check for alarm conditions

## Volume Control:
goto init new state
query user for IE, BPM, TV
goto Initial Homing Phase
inspiratory phase:
goto init new state
store pressure reading 
store p_curr - p_prev
if time elapsed >= inspiratory time
continue
drive stepper motor
inspiratory pause:
goto init new state
stop driving stepper motor
hold stepper motor
store peak pressure reading
if time elapsed >= inspiratory hold time
continue
expiratory phase:
goto init new state
store plateau pressure
drive stepper motor back to stored offset position
if time elapsed >= expiratory time
expiratory pause:
goto init new state
if time elapsed >= expiratory hold time && no rehoming
goto Inspiratory Phase
if time elapsed >= expiratory hold time && 60 seconds since rehoming
goto Rehoming


## Initial Homing Phase:
drive stepper motor until abs limit switch 1
store max rotation value
drive stepper motor until con limit switch 1
 if in initial homing phase
query user for confirmation
store offset b/w abs and con
store diameter of bag
return


## Rehoming:
drive stepper motor until con limit switch 0
drive stepper motor until con limit switch 1
store offset b/w abs and con
store diameter of bag
goto inspiratory phase