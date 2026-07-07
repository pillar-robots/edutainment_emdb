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
import requests

class PolicySkill1(Policy):
    def __init__(self, name='skill_1_python_policy', class_name='cognitive_nodes.policy.Policy', publisher_msg=None, publisher_topic=None, **params):
        super().__init__(name, class_name, publisher_msg, publisher_topic, **params)
    async def execute_callback(self, request, response):
        requests.post("http://localhost:2727/api/skills/1")
        response.policy = self.name
        return response

class PolicySkill2(Policy):
    def __init__(self, name='skill_2_evaluation_policy', class_name='cognitive_nodes.policy.Policy', publisher_msg=None, publisher_topic=None, **params):
        super().__init__(name, class_name, publisher_msg, publisher_topic, **params)
    async def execute_callback(self, request, response):
        requests.post("http://localhost:2727/api/skills/2")
        response.policy = self.name
        return response

class PolicySkill3(Policy):
    def __init__(self, name='skill_3_teacher_policy', class_name='cognitive_nodes.policy.Policy', publisher_msg=None, publisher_topic=None, **params):
        super().__init__(name, class_name, publisher_msg, publisher_topic, **params)
    async def execute_callback(self, request, response):
        requests.post("http://localhost:2727/api/skills/3")
        response.policy = self.name
        return response

class PolicySkill4(Policy):
    def __init__(self, name='skill_4_sit_policy', class_name='cognitive_nodes.policy.Policy', publisher_msg=None, publisher_topic=None, **params):
        super().__init__(name, class_name, publisher_msg, publisher_topic, **params)
    async def execute_callback(self, request, response):
        requests.post("http://localhost:2727/api/skills/4")
        response.policy = self.name
        return response

class PolicySkill5(Policy):
    def __init__(self, name='skill_5_break_policy', class_name='cognitive_nodes.policy.Policy', publisher_msg=None, publisher_topic=None, **params):
        super().__init__(name, class_name, publisher_msg, publisher_topic, **params)
    async def execute_callback(self, request, response):
        requests.post("http://localhost:2727/api/skills/5")
        response.policy = self.name
        return response

class PolicySkill6(Policy):
    def __init__(self, name='skill_6_video_policy', class_name='cognitive_nodes.policy.Policy', publisher_msg=None, publisher_topic=None, **params):
        super().__init__(name, class_name, publisher_msg, publisher_topic, **params)
    async def execute_callback(self, request, response):
        requests.post("http://localhost:2727/api/skills/6")
        response.policy = self.name
        return response

class PolicySkill7(Policy):
    def __init__(self, name='skill_7_gamification_policy', class_name='cognitive_nodes.policy.Policy', publisher_msg=None, publisher_topic=None, **params):
        super().__init__(name, class_name, publisher_msg, publisher_topic, **params)
    async def execute_callback(self, request, response):
        requests.post("http://localhost:2727/api/skills/7")
        response.policy = self.name
        return response
