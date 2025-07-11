from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='week4_arm',
            executable='fk_node.py',
            name='forward_kinematics_node',
            output='screen'
        )
    ])
