#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Point
import math

class ForwardKinematicsNode(Node):
    def __init__(self):
        super().__init__('forward_kinematics_node')

        # Link lengths
        self.L1 = 2.0
        self.L2 = 1.5

        # Subscriber
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )

        # Publisher
        self.publisher = self.create_publisher(
            Point,
            '/end_effector_position',
            10
        )

        self.get_logger().info('Forward Kinematics Node has been started.')

    def joint_state_callback(self, msg):
        # Assuming joint order: [shoulder, elbow]
        theta1 = msg.position[0] + math.pi / 2.0
        theta2 = msg.position[1]

        # Compute FK
        x = self.L1 * math.cos(theta1) + self.L2 * math.cos(theta1 + theta2)
        y = self.L1 * math.sin(theta1) + self.L2 * math.sin(theta1 + theta2)

        # Publish
        point = Point()
        point.x = x
        point.y = y
        point.z = 0.0

        self.publisher.publish(point)
        self.get_logger().info(f'Published End Effector Position: x={x:.3f}, y={y:.3f}')

def main(args=None):
    rclpy.init(args=args)
    node = ForwardKinematicsNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
