import time
import rclpy
from rclpy.action import ActionClient
import random
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectoryPoint, JointTrajectory
from builtin_interfaces.msg import Duration
from cognitive_nodes.policy import Policy
from core.utils import perception_msg_to_dict
from cognitive_node_interfaces.srv import SetActivation
from core.service_client import ServiceClientAsync
from std_msgs.msg import Float32
from my_controll.joke import TellJoke


class PolicySkill1(Policy):
    def __init__(self, name='skill_1_python_tip', class_name='cognitive_nodes.policy.Policy', publisher_msg=None, publisher_topic=None, **params):
        super().__init__(name, class_name, publisher_msg, publisher_topic, **params)

    async def execute_callback(self, request, response):
        idle_motion = AutonomousIdleMotion()
        idle_motion.execute_random_motion()

        node_speek_joken = TellJoke()
        node_speek_joken.move_joke()
        node_speek_joken.destroy_node()
        response.policy = self.name
        #time.sleep(5)
        return response


class AutonomousIdleMotion(Node):
    def __init__(self):
        super().__init__('autonomous_idle_motion')

        self.head_joint_pub = self.create_publisher(JointTrajectory, '/head_controller/joint_trajectory', 0)
        self.torso_pub = self.create_publisher(JointTrajectory, '/torso_controller/joint_trajectory',0)

    def publish_head(self, joint_1, joint_2, duration=2):
        msg = JointTrajectory()
        msg.joint_names = ["head_1_joint", "head_2_joint"]

        point = JointTrajectoryPoint()
        point.positions = [float(joint_1), float(joint_2)]
        point.time_from_start = Duration(sec=duration, nanosec=0)

        msg.points = [point]

        self.head_joint_pub.publish(msg)

    def publish_torso(self, height, duration=2):
        height = max(0.10, min(height, 0.20))

        msg = JointTrajectory()
        msg.joint_names = ["torso_lift_joint"]

        point = JointTrajectoryPoint()
        point.positions = [float(height)]
        point.time_from_start = Duration(sec=duration, nanosec=0)

        msg.points = [point]

        self.torso_pub.publish(msg)

    def execute_random_motion(self):
        head_1 = random.uniform(-0.35, 0.35)
        head_2 = random.uniform(-0.30, 0.30)
        torso = random.uniform(0.10, 0.20)
        move_time = random.uniform(1.0, 2.5)

        self.publish_head(head_1, head_2, int(move_time))
        self.publish_torso(torso, int(move_time))

        time.sleep(move_time)
        time.sleep(random.uniform(0.5, 1.5))

        if random.random() < 0.65:
            self.publish_head(1.1, 0.5, 3)
            time.sleep(4)

        self.publish_head(0.0, 0.0, 2)
        self.publish_torso(0.15, 2)
