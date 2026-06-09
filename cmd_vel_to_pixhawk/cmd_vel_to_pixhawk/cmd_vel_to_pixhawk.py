import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from pymavlink import mavutil

class CmdVelToPixhawk(Node):
    def __init__(self):
        super().__init__('cmd_vel_to_pixhawk')
        self.cmd_vel_sub = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            10
        )
        self.joy_sub = self.create_subscription(
            Joy,
            '/joy',
            self.joy_callback,
            10
        )

        self.master = mavutil.mavlink_connection('/dev/ttyACM0')
        self.master.wait_heartbeat()
        self.get_logger().info("Heartbeat received")
        self.master.arducopter_arm()
        self.master.motors_armed_wait()
        self.get_logger().info("ARMED")

    def cmd_vel_callback(self, msg):
        linear = msg.linear.x
        angular = -msg.angular.z

        throttle = int(1500 + linear * 500)
        steering = int(1500 + angular * 500)

        throttle = max(1000, min(2000, throttle))
        steering = max(1000, min(2000, steering))

        self.master.mav.rc_channels_override_send(
            self.master.target_system,
            self.master.target_component,

            steering,   # CH1 steering
            65535,      # CH2 上書きしない
            throttle,   # CH3 throttle
            65535,      # CH4 上書きしない

            65535,65535,65535,65535
        )

    def joy_callback(self, msg):

        # ARM化とDISARM化もできるように
        if msg.buttons[2]: # ○
            self.master.arducopter_arm()
            self.master.motors_armed_wait()
            self.get_logger().info("ARMED")

        if msg.buttons[1]: # X
            self.master.arducopter_disarm()
            self.master.motors_disarmed_wait()
            self.get_logger().info("DISARMED")

        throttle_axis = msg.axes[1]
        steering_axis = msg.axes[0]

        # throttle = int(1500 + throttle_axis * 500)
        # steering = int(1500 + steering_axis * 500)

        # self.master.mav.rc_channels_override_send(
        #     self.master.target_system,
        #     self.master.target_component,

        #     steering,
        #     65535,
        #     throttle,
        #     65535,

        #     65535,
        #     65535,
        #     65535,
        #     65535
        # )

    def stop_and_disarm(self):
        self.get_logger().info("Stopping rover...")

        self.master.mav.rc_channels_override_send(
            self.master.target_system,
            self.master.target_component,

            1500,   # CH1 steering センター
            65535,  # CH2 上書きしない
            1500,   # CH3 throttle センター
            65535,  # CH4 上書きしない

            65535,65535,65535,65535
        )

        self.master.arducopter_disarm()
        self.master.motors_disarmed_wait()

        self.get_logger().info("DISARMED")


    # def destroy_node(self):
    #     self.master.mav.rc_channels_override_send(
    #         self.master.target_system,
    #         self.master.target_component,

    #         0,      # CH1 steering 上書き解除
    #         65535,  # CH2 上書きしない
    #         0,      # CH3 throttle 上書き解除
    #         65535,  # CH4 上書きしない

    #         65535,65535,65535,65535
    #     )

    #     self.master.arducopter_disarm()
    #     self.master.motors_disarmed_wait()

    #     self.get_logger().info("DISARMED")
    #     super().destroy_node()


def main(args=None):

    rclpy.init(args=args)
    node = CmdVelToPixhawk()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally: 
        node.stop_and_disarm()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

