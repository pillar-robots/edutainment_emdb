import time
import rclpy
from rclpy.action import ActionClient
import random
from rclpy.node import Node
from core.utils import perception_msg_to_dict
from core.service_client import ServiceClientAsync
from cognitive_nodes.policy import Policy
from cognitive_node_interfaces.srv import SetActivation
from trajectory_msgs.msg import JointTrajectoryPoint, JointTrajectory
from builtin_interfaces.msg import Duration
from std_msgs.msg import Float32

class PolicySkill1(Policy):
    def __init__(self, name='skill_1_python_policy', class_name='cognitive_nodes.policy.Policy', publisher_msg=None, publisher_topic=None, **params):
        super().__init__(name, class_name, publisher_msg, publisher_topic, **params)

    async def execute_callback(self, request, response):
        #idle_motion = AutonomousIdleMotion()
        #idle_motion.execute_random_motion()
        #node_speek_joken = TellJoke()
        #node_speek_joken.move_joke()
        #node_speek_joken.destroy_node()
        response.policy = self.name
        ##time.sleep(5)
        return response
