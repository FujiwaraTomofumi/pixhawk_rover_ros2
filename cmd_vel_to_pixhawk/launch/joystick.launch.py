from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    config_file = os.path.join(
        get_package_share_directory('cmd_vel_to_pixhawk'),
        'config',
        'teleop.yaml'
    )

    return LaunchDescription([

        Node(
            package='joy',
            executable='joy_node',
            name='joy_node',
            output='screen'
        ),

        Node(
            package='teleop_twist_joy',
            executable='teleop_node',
            name='teleop_twist_joy',
            output='screen',
            parameters=[config_file]
        ),

        Node(
            package='cmd_vel_to_pixhawk',
            executable='cmd_vel_to_pixhawk',
            name='cmd_vel_to_pixhawk',
            output='screen',
        ),
    
    ])