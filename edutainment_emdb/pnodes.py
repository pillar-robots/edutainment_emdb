import math
from cognitive_nodes.pnode import PNode

class PNodePythonErrors(PNode): #Pn1.1
    """
    PNode that represents Python errors
    """
    def __init__(self, name='python_errors_pnode', class_name='cognitive_nodes.pnode.PNode', space_class=None, space=None, history_size=100, **params):
        super().__init__(name, class_name, space_class, space, history_size, **params)
    def calculate_activation(self, perception=None, activation_list=None):
        """
        Calculate the new activation value for a given perception.

        :param perception: The perception for which P-Node activation is calculated.
        :type perception: dict
        :param activation_list: The list of activations to be used for the calculation.
        :type activation_list: list
        :return: If there is space, returns the activation of the P-Node. If not, returns 0. 
            It also returs the timestamp.
        :rtype: cognitive_node_interfaces.msg.Activation
        """
        if activation_list!=None:
            perception={}
            for sensor in activation_list:
                activation_list[sensor]['updated']=False
                perception[sensor]=activation_list[sensor]['data']
        if perception:
            value_raw = perception.get('python_errors_perception')
            value = round(value_raw[0]['data'], 1)

            # Pn1.1: Python errors > low threshold
            if value >= 0.5:
                self.activation.activation = 0.95
                self.get_logger().debug(f"PNODE DEBUG: python_errors_pnode: {value}")
            else:
                self.activation.activation = 0.0
            
            self.activation.timestamp = self.get_clock().now().to_msg()
        return self.activation

class PNodeEvaluationErrors(PNode): #Pn1.2
    """
    PNode that represents evaluation errors
    """
    def __init__(self, name='evaluation_errors_pnode', class_name='cognitive_nodes.pnode.PNode', space_class=None, space=None, history_size=100, **params):
        super().__init__(name, class_name, space_class, space, history_size, **params)
    def calculate_activation(self, perception=None, activation_list=None):
        if activation_list!=None:
            perception={}
            for sensor in activation_list:
                activation_list[sensor]['updated']=False
                perception[sensor]=activation_list[sensor]['data']
        if perception:
            value_raw = perception.get('evaluation_errors_perception')
            value = round(value_raw[0]['data'], 1)

            # Pn1.2: evaluation errors > low threshold
            if value >= 0.5:
                self.activation.activation = 0.95
                self.get_logger().debug(f"PNODE DEBUG: evaluation_errors_pnode: {value}")
            else:
                self.activation.activation = 0.0
            
            self.activation.timestamp = self.get_clock().now().to_msg()
        return self.activation

class PNodePythonEvaluationErrorsPresent(PNode): #Pn1.3
    """
    PNode that represents Python and evaluation errors with teacher present
    """
    def __init__(self, name='python_evaluation_errors_present_pnode', class_name='cognitive_nodes.pnode.PNode', space_class=None, space=None, history_size=100, **params):
        super().__init__(name, class_name, space_class, space, history_size, **params)
    def calculate_activation(self, perception=None, activation_list=None):
        if activation_list!=None:
            perception={}
            for sensor in activation_list:
                activation_list[sensor]['updated']=False
                perception[sensor]=activation_list[sensor]['data']
        if perception:
            value_raw = perception.get('python_errors_perception')
            value = round(value_raw[0]['data'], 1)
            value_raw_2 = perception.get('evaluation_errors_perception')
            value_2 = round(value_raw_2[0]['data'], 1)
            value_raw_3 = perception.get('teacher_present_perception')
            value_3 = round(value_raw_3[0]['data'], 1)

            # P1.3: any USER present & Python errors or evaluation errors > high threshold
            if value >= 0.75 and value_2 >= 0.75 and value_3 == 1.0:
                self.activation.activation = 0.95
                self.get_logger().debug(f"PNODE DEBUG: python_evaluation_errors_present_pnode: {value}")
            else:
                self.activation.activation = 0.0
            
            self.activation.timestamp = self.get_clock().now().to_msg()
        return self.activation