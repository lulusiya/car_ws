import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
import os


class PathPublisher(Node):
    def __init__(self):
        super().__init__('path_publisher')
        # 发布 Path 的话题，pure_pursuit_planner 默认订阅 /plan
        self.publisher_ = self.create_publisher(Path, 'plan', 10)
        timer_period = 2.0  # 每2秒发布一次路径
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        path = Path()
        path.header.frame_id = "map"  # 路径的坐标系，可以改成 "odom" 或 "base_link"
        path.header.stamp = self.get_clock().now().to_msg()

        # 路径文件位置，注意修改路径
        file_path = os.path.expanduser("~/car_ws/src/path_publisher/path.txt")

        if not os.path.exists(file_path):
            self.get_logger().error(f"路径文件 {file_path} 不存在！")
            return

        with open(file_path, 'r') as f:
            for line in f:
                try:
                    x, y = line.strip().split(',')
                    pose = PoseStamped()
                    pose.header.frame_id = "map"
                    pose.header.stamp = self.get_clock().now().to_msg()
                    pose.pose.position.x = float(x)
                    pose.pose.position.y = float(y)
                    pose.pose.position.z = 0.0
                    pose.pose.orientation.w = 1.0  # 朝向默认不旋转
                    path.poses.append(pose)
                except ValueError:
                    self.get_logger().warn(f"无法解析行: {line.strip()}")

        self.publisher_.publish(path)
        self.get_logger().info(f'发布路径，共 {len(path.poses)} 个点')


def main(args=None):
    rclpy.init(args=args)
    node = PathPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

