import pyuarm
import time

arm = pyuarm.uArm()

if not arm.is_connected():
	raise SystemExit()


#fetch card position, at the table
fetchCard = [-0.71, -9.72, 8.7] 

#home position
home = [-1.49, -10.03, 18.9]
time_spend=5

arm. move_to(home[0], home[1], home[2], None, pyuarm.ABSOLUTE, time_spend, pyuarm.PATH_LINEAR, pyuarm.INTERP_EASE_INOUT_CUBIC)

#INTERP_EASE_INOUT_CUBIC, INTERP_LINEAR, INTERP_EASE_INOUT, INTERP_EASE_IN, INTERP_EASE_OUT
arm. move_to(fetchCard[0], fetchCard[1], fetchCard[2], None, pyuarm.ABSOLUTE, time_spend, pyuarm.PATH_LINEAR, pyuarm.INTERP_EASE_INOUT_CUBIC)
#time.sleep(0.1)
arm.pump_control(1)
arm. move_to(home[0], home[1], home[2], None, pyuarm.ABSOLUTE, time_spend, pyuarm.PATH_LINEAR, pyuarm.INTERP_EASE_INOUT_CUBIC)
arm.pump_control(0)
