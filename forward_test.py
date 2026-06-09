from pymavlink import mavutil
import time

master = mavutil.mavlink_connection('/dev/ttyACM0')

master.wait_heartbeat()

master.arducopter_arm()

master.motors_armed_wait()

print("ARMED")

for i in range(50):

    master.mav.rc_channels_override_send(
        master.target_system,
        master.target_component,

        1500,   # CH1 steering
        65535,  # CH2 上書きしない
        1600,   # CH3 throttle
        65535,  # CH4 上書きしない

        65535,65535,65535,65535
    )

    time.sleep(0.1)

