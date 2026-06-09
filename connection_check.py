from pymavlink import mavutil

master = mavutil.mavlink_connection('/dev/ttyACM0')

master.wait_heartbeat()

print("connected")
print(master.target_system)

