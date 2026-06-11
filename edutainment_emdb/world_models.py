import rclpy
from copy import deepcopy
from cognitive_nodes.world_model import WorldModel
from std_msgs.msg import Float32
from rclpy.callback_groups import ReentrantCallbackGroup, MutuallyExclusiveCallbackGroup
from core.utils import class_from_classname, perception_msg_to_dict, separate_perceptions
from cognitive_node_interfaces.msg import Perception, PerceptionStamped
from rclpy.time import Time

class EdutainmentStudentExpert(WorldModel):
    def __init__(self,
                 name='EXPERT_WM',
                 class_name='cognitive_nodes.world_model.WorldModel',
                 **params):
        super().__init__(name, class_name, **params)
        self.selected_behavior = None
        self.configure_activation_inputs(self.neighbors)

    def calculate_activation(self, perception=None, activation_list=None):
        if activation_list!=None:
            perception={}
            for sensor in activation_list:
                activation_list[sensor]['updated']=False
                perception[sensor]=activation_list[sensor]['data']
        if perception:
            value_raw = perception.get('student_type_perception')
            value = round(value_raw[0]['data'], 1)

            # Apply your activation logic
            if value > 0.5:
                self.activation.activation = 1.0
                self.selected_behavior = "expert_student"
                self.get_logger().debug(f"[{self.name}] Selected behavior: {self.selected_behavior}")
            else:
                self.activation.activation = 0.0

            self.activation.timestamp = self.get_clock().now().to_msg()
        return self.activation
    
    def create_activation_input(self, node: dict): #Adds or deletes a node from the activation inputs list. By default reads activations.
        """
        Adds perceptions to the activation inputs list.

        :param node: Dictionary with the information of the node {'name': <name>, 'node_type': <node_type>}.
        :type node: dict
        """    
        name=node['name']
        node_type=node['node_type']
        if node_type == "Perception":
            subscriber=self.create_subscription(PerceptionStamped, "perception/" + str(name) + "/value", self.read_activation_callback, 1, callback_group=self.cbgroup_activation)
            data=Perception()
            updated=False
            timestamp=Time()
            new_input=dict(subscriber=subscriber, data=data, updated=updated, timestamp=timestamp)
            self.activation_inputs[name]=new_input
            self.get_logger().debug(f'{self.name} -- Created new activation input: {name} of type {node_type}')

    def read_activation_callback(self, msg: PerceptionStamped):
        """
        Callback method that reads a perception and stores it in the activation inputs list.

        :param msg: PerceptionStamped message that contains the perception and its timestamp.
        :type msg: cognitive_node_interfaces.msg.PerceptionStamped
        """        
        perception_dict=perception_msg_to_dict(msg=msg.perception)
        if len(perception_dict)>1:
            self.get_logger().error(f'{self.name} -- Received perception with multiple sensors: ({perception_dict.keys()}). Perception nodes should (currently) include only one sensor!')
        if len(perception_dict)==1:
            node_name=list(perception_dict.keys())[0]
            if node_name in self.activation_inputs:
                self.activation_inputs[node_name]['data']=perception_dict[node_name]
                self.activation_inputs[node_name]['updated']=True
                self.activation_inputs[node_name]['timestamp']=Time.from_msg(msg.timestamp)
        else:
            self.get_logger().warn("Empty perception recieved in P-Node. No activation calculated")

class EdutainmentStudentAmateur(WorldModel):
    def __init__(self,
                 name='AMATEUR_WM',
                 class_name='cognitive_nodes.world_model.WorldModel',
                 **params):
        super().__init__(name, class_name, **params)
        self.selected_behavior = None
        self.configure_activation_inputs(self.neighbors)

    def calculate_activation(self, perception=None, activation_list=None):
        if activation_list!=None:
            perception={}
            for sensor in activation_list:
                activation_list[sensor]['updated']=False
                perception[sensor]=activation_list[sensor]['data']
        if perception:
            value_raw = perception.get('student_type_perception')
            value = round(value_raw[0]['data'], 1)

            # Apply your activation logic
            if value <= 0.25:
                self.activation.activation = 1.0
                self.selected_behavior = "amateur_student"
                self.get_logger().debug(f"[{self.name}] Selected behavior: {self.selected_behavior}")
            else:
                self.activation.activation = 0.0
            
            self.activation.timestamp = self.get_clock().now().to_msg()
        return self.activation
    
    def create_activation_input(self, node: dict): #Adds or deletes a node from the activation inputs list. By default reads activations.
        """
        Adds perceptions to the activation inputs list.

        :param node: Dictionary with the information of the node {'name': <name>, 'node_type': <node_type>}.
        :type node: dict
        """    
        name=node['name']
        node_type=node['node_type']
        if node_type == "Perception":
            subscriber=self.create_subscription(PerceptionStamped, "perception/" + str(name) + "/value", self.read_activation_callback, 1, callback_group=self.cbgroup_activation)
            data=Perception()
            updated=False
            timestamp=Time()
            new_input=dict(subscriber=subscriber, data=data, updated=updated, timestamp=timestamp)
            self.activation_inputs[name]=new_input
            self.get_logger().debug(f'{self.name} -- Created new activation input: {name} of type {node_type}')

    def read_activation_callback(self, msg: PerceptionStamped):
        """
        Callback method that reads a perception and stores it in the activation inputs list.

        :param msg: PerceptionStamped message that contains the perception and its timestamp.
        :type msg: cognitive_node_interfaces.msg.PerceptionStamped
        """        
        perception_dict=perception_msg_to_dict(msg=msg.perception)
        if len(perception_dict)>1:
            self.get_logger().error(f'{self.name} -- Received perception with multiple sensors: ({perception_dict.keys()}). Perception nodes should (currently) include only one sensor!')
        if len(perception_dict)==1:
            node_name=list(perception_dict.keys())[0]
            if node_name in self.activation_inputs:
                self.activation_inputs[node_name]['data']=perception_dict[node_name]
                self.activation_inputs[node_name]['updated']=True
                self.activation_inputs[node_name]['timestamp']=Time.from_msg(msg.timestamp)
        else:
            self.get_logger().warn("Empty perception recieved in P-Node. No activation calculated")

class EdutainmentStudentGeneral(WorldModel):
    def __init__(self,
                 name='GENERAL_WM',
                 class_name='cognitive_nodes.world_model.WorldModel',
                 **params):
        super().__init__(name, class_name, **params)
        self.selected_behavior = None
        self.configure_activation_inputs(self.neighbors)

    def calculate_activation(self, perception=None, activation_list=None):
        if activation_list!=None:
            perception={}
            for sensor in activation_list:
                activation_list[sensor]['updated']=False
                perception[sensor]=activation_list[sensor]['data']
        if perception:
            value_raw = perception.get('student_type_perception')
            value = round(value_raw[0]['data'], 1)

            # Apply your activation logic
            if 0.25 < value <= 0.5:
                self.activation.activation = 1.0
                self.selected_behavior = "general_student"
                self.get_logger().debug(f"[{self.name}] Selected behavior: {self.selected_behavior}")
            else:
                self.activation.activation = 0.0

            self.activation.timestamp = self.get_clock().now().to_msg()
        return self.activation
    
    def create_activation_input(self, node: dict): #Adds or deletes a node from the activation inputs list. By default reads activations.
        """
        Adds perceptions to the activation inputs list.

        :param node: Dictionary with the information of the node {'name': <name>, 'node_type': <node_type>}.
        :type node: dict
        """    
        name=node['name']
        node_type=node['node_type']
        if node_type == "Perception":
            subscriber=self.create_subscription(PerceptionStamped, "perception/" + str(name) + "/value", self.read_activation_callback, 1, callback_group=self.cbgroup_activation)
            data=Perception()
            updated=False
            timestamp=Time()
            new_input=dict(subscriber=subscriber, data=data, updated=updated, timestamp=timestamp)
            self.activation_inputs[name]=new_input
            self.get_logger().debug(f'{self.name} -- Created new activation input: {name} of type {node_type}')

    def read_activation_callback(self, msg: PerceptionStamped):
        """
        Callback method that reads a perception and stores it in the activation inputs list.

        :param msg: PerceptionStamped message that contains the perception and its timestamp.
        :type msg: cognitive_node_interfaces.msg.PerceptionStamped
        """        
        perception_dict=perception_msg_to_dict(msg=msg.perception)
        if len(perception_dict)>1:
            self.get_logger().error(f'{self.name} -- Received perception with multiple sensors: ({perception_dict.keys()}). Perception nodes should (currently) include only one sensor!')
        if len(perception_dict)==1:
            node_name=list(perception_dict.keys())[0]
            if node_name in self.activation_inputs:
                self.activation_inputs[node_name]['data']=perception_dict[node_name]
                self.activation_inputs[node_name]['updated']=True
                self.activation_inputs[node_name]['timestamp']=Time.from_msg(msg.timestamp)
        else:
            self.get_logger().warn("Empty perception recieved in P-Node. No activation calculated")
