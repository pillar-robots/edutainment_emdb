import time
import rclpy
import random
import requests
from cognitive_nodes.policy import Policy
from rclpy.node import Node
from std_srvs.srv import Empty

class ServiceClient(Node):
    def __init__(self, name='skill1_client', service_name='pillar_control/skill_1'):
        super().__init__(name)
        self.service_name = service_name
        self.client = self.create_client(Empty, self.service_name)
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(f'Waiting for service {self.service_name}')
        self.request = Empty.Request()

    def call_service(self):
        future = self.client.call_async(self.request)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            self.get_logger().info(f'Called {self.service_name}')
        else:
            self.get_logger().error(f'Error while calling service: {future.exception()}')


class PolicySkill0(Policy): # Dummy idle policy.
    def __init__(self, name='skill_0_idle_policy', class_name='cognitive_nodes.policy.Policy', service_msg=None, service_name=None, **params):
        super().__init__(name=name, class_name=class_name, **params)
    async def execute_callback(self, request, response):
        #requests.post("http://localhost:2727/api/skills/0")
        #node = ServiceClient(name=self.name, service_name='pillar_control/skill_0')
        #node.call_service()
        #node.destroy_node()
        response.policy = self.name
        return response

class PolicySkill1(Policy):
    def __init__(self, name='skill_1_python_policy', class_name='cognitive_nodes.policy.Policy', service_msg=None, service_name=None, **params):
        super().__init__(name=name, class_name=class_name, **params)
    async def execute_callback(self, request, response):
        #requests.post("http://localhost:2727/api/skills/1")
        node = ServiceClient(name=self.name, service_name='pillar_control/skill_1')
        node.call_service()
        node.destroy_node()
        response.policy = self.name
        return response

class PolicySkill2(Policy):
    def __init__(self, name='skill_2_evaluation_policy', class_name='cognitive_nodes.policy.Policy', service_msg=None, service_name=None, **params):
        super().__init__(name=name, class_name=class_name, **params)
    async def execute_callback(self, request, response):
        #requests.post("http://localhost:2727/api/skills/2")
        node = ServiceClient(name=self.name, service_name='pillar_control/skill_2')
        node.call_service()
        node.destroy_node()
        response.policy = self.name
        return response

class PolicySkill3(Policy):
    def __init__(self, name='skill_3_teacher_policy', class_name='cognitive_nodes.policy.Policy', service_msg=None, service_name=None, **params):
        super().__init__(name=name, class_name=class_name, **params)
    async def execute_callback(self, request, response):
        #requests.post("http://localhost:2727/api/skills/3")
        node = ServiceClient(name=self.name, service_name='pillar_control/skill_3')
        node.call_service()
        node.destroy_node()
        response.policy = self.name
        return response

class PolicySkill4(Policy):
    def __init__(self, name='skill_4_sit_policy', class_name='cognitive_nodes.policy.Policy', service_msg=None, service_name=None, **params):
        super().__init__(name=name, class_name=class_name, **params)
    async def execute_callback(self, request, response):
        #requests.post("http://localhost:2727/api/skills/4")
        node = ServiceClient(name=self.name, service_name='pillar_control/skill_4')
        node.call_service()
        node.destroy_node()
        response.policy = self.name
        return response

class PolicySkill5(Policy):
    def __init__(self, name='skill_5_break_policy', class_name='cognitive_nodes.policy.Policy', service_msg=None, service_name=None, **params):
        super().__init__(name=name, class_name=class_name, **params)
    async def execute_callback(self, request, response):
        #requests.post("http://localhost:2727/api/skills/5")
        node = ServiceClient(name=self.name, service_name='pillar_control/skill_5')
        node.call_service()
        node.destroy_node()
        response.policy = self.name
        return response

class PolicySkill6(Policy):
    def __init__(self, name='skill_6_video_policy', class_name='cognitive_nodes.policy.Policy', service_msg=None, service_name=None, **params):
        super().__init__(name=name, class_name=class_name, **params)
    async def execute_callback(self, request, response):
        #requests.post("http://localhost:2727/api/skills/6")
        node = ServiceClient(name=self.name, service_name='pillar_control/skill_6')
        node.call_service()
        node.destroy_node()
        response.policy = self.name
        return response

class PolicySkill7(Policy):
    def __init__(self, name='skill_7_gamification_policy', class_name='cognitive_nodes.policy.Policy', service_msg=None, service_name=None, **params):
        super().__init__(name=name, class_name=class_name, **params)
    async def execute_callback(self, request, response):
        #requests.post("http://localhost:2727/api/skills/7")
        node = ServiceClient(name=self.name, service_name='pillar_control/skill_7')
        node.call_service()
        node.destroy_node()
        response.policy = self.name
        return response
