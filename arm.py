from pymavlink import mavutil

master = mavutil.mavlink_connection('/dev/ttyACM0')

master.wait_heartbeat()

master.arducopter_arm()

master.motors_armed_wait()

print("ARMED")


