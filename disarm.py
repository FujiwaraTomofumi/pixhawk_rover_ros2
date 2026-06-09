from pymavlink import mavutil

master = mavutil.mavlink_connection('/dev/ttyACM0')

master.wait_heartbeat()

master.arducopter_disarm()

master.motors_disarmed_wait()

print("DISARMED")


