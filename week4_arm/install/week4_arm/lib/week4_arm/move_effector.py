#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from std_msgs.msg import Float64MultiArray
import numpy as np
import threading

L1 = 2.0
L2 = 1.5

class EffectorMover(Node):
    def __init__(self):
        super().__init__('move_effector')
        self.subscription = self.create_subscription(
            Point,
            '/end_effector_position',
            self.end_effector_callback,
            10
        )
        self.publisher = self.create_publisher(Float64MultiArray, '/joint_angles_goal', 10)
        self.current_position = Point()
        self.get_logger().info("EffectorMover node started. Waiting for /end_effector_position...")

    def end_effector_callback(self, msg):
        self.current_position = msg
        self.get_logger().info(f"Current EE Position: x={msg.x:.2f}, y={msg.y:.2f}")

    def run(self):
        while rclpy.ok():
            print("\n== Move End Effector ==")
            direction = input("Enter direction (x/y): ").strip().lower()
            if direction not in ['x', 'y']:
                print("❌ Invalid direction. Please enter 'x' or 'y'.")
                continue

            try:
                delta = float(input("Enter movement (max 0.5m): "))
            except ValueError:
                print("❌ Invalid number.")
                continue

            if abs(delta) > 0.5:
                print("❌ Movement exceeds 0.5m limit.")
                continue

            # Compute new goal
            new_x = self.current_position.x + delta if direction == 'x' else self.current_position.x
            new_y = self.current_position.y + delta if direction == 'y' else self.current_position.y

            dx2 = new_x**2 + new_y**2
            if dx2 > (L1 + L2)**2 or dx2 < (L1 - L2)**2:
                self.get_logger().warn("Target position unreachable.")
                continue

            # Inverse Kinematics (elbow-down)
            cos_theta2 = (dx2 - L1**2 - L2**2) / (2 * L1 * L2)
            sin_theta2 = np.sqrt(1 - cos_theta2**2)
            theta2 = np.arctan2(sin_theta2, cos_theta2)

            k1 = L1 + L2 * cos_theta2
            k2 = L2 * sin_theta2
            theta1 = np.arctan2(new_y, new_x) - np.arctan2(k2, k1)

            # Adjust θ1 for FK node
            theta1_adjusted = theta1 - np.pi / 2.0

            msg = Float64MultiArray()
            msg.data = [theta1_adjusted, theta2]
            self.publisher.publish(msg)
            self.get_logger().info(f"✅ Published joint angles: θ1={theta1_adjusted:.2f}, θ2={theta2:.2f}")

def main(args=None):
    rclpy.init(args=args)
    node = EffectorMover()

    thread = threading.Thread(target=node.run)
    thread.start()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
