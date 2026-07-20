import math
from cognitive_nodes.pnode import PNode

# Global variables for the thresholds
TEACHER_ABSENT_THRESHOLD = 0.0
TEACHER_PRESENT_THRESHOLD = 1.0
TEACHER_TYPE_UNDEFINED_THRESHOLD = 0.0
TEACHER_TYPE_MODERN_THRESHOLD = 0.21 # To avoid rounding errors.
TEACHER_TYPE_OLD_THRESHOLD = 0.8
PYTHON_ERRORS_LOW_THRESHOLD = 0.5
PYTHON_ERRORS_MID_THRESHOLD = 0.6
PYTHON_ERRORS_HIGH_THRESHOLD = 0.8
EVALUATION_ERRORS_LOW_THRESHOLD = 0.5
EVALUATION_ERRORS_MID_THRESHOLD = 0.6
EVALUATION_ERRORS_HIGH_THRESHOLD = 0.8
BORED_LOW_THRESHOLD = 0.5
BORED_HIGH_THRESHOLD = 0.75
STANDING_LOW_THRESHOLD = 0.5
STANDING_HIGH_THRESHOLD = 0.75

class PNodeIdle(PNode): #Pn0
    """
    PNode that represents if the system should be idle or not. It is activated when the python_error_streak_perception is below the low threshold.
    """
    def __init__(self, name='idle_pnode', class_name='cognitive_nodes.pnode.PNode', space_class=None, space=None, history_size=100, **params):
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
            value_raw = perception.get('python_error_streak_perception')
            value = round(value_raw[0]['data'], 1)

            # Pn0: Python errors < low threshold
            if value < PYTHON_ERRORS_LOW_THRESHOLD:
                self.activation.activation = 0.99 
                self.get_logger().debug(f"PNODE DEBUG: idle_pnode: {value}")
            else:
                self.activation.activation = 0.0
            
            self.activation.timestamp = self.get_clock().now().to_msg()
        return self.activation

class PNodePythonErrors(PNode): #Pn1.1
    """
    PNode that represents Python errors
    """
    def __init__(self, name='python_errors_pnode', class_name='cognitive_nodes.pnode.PNode', space_class=None, space=None, history_size=100, **params):
        super().__init__(name, class_name, space_class, space, history_size, **params)
    def calculate_activation(self, perception=None, activation_list=None):
        if activation_list!=None:
            perception={}
            for sensor in activation_list:
                activation_list[sensor]['updated']=False
                perception[sensor]=activation_list[sensor]['data']
        if perception:
            value_raw = perception.get('python_error_streak_perception')
            value = round(value_raw[0]['data'], 1)

            # Pn1.1: Python errors > low threshold
            if value >= PYTHON_ERRORS_LOW_THRESHOLD and value < PYTHON_ERRORS_MID_THRESHOLD:
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
            value_raw = perception.get('evaluation_error_streak_perception')
            value = round(value_raw[0]['data'], 1)

            # Pn1.2: evaluation errors > low threshold
            if value >= EVALUATION_ERRORS_LOW_THRESHOLD and value < EVALUATION_ERRORS_MID_THRESHOLD:
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
            value_raw = perception.get('teacher_present_perception')
            value = round(value_raw[0]['data'], 1)
            value_raw_2 = perception.get('python_error_streak_perception')
            value_2 = round(value_raw_2[0]['data'], 1)
            value_raw_3 = perception.get('evaluation_error_streak_perception')
            value_3 = round(value_raw_3[0]['data'], 1)

            # P1.3: any USER present & Python errors or evaluation errors > high threshold
            if  value == TEACHER_PRESENT_THRESHOLD and (value_2 >= PYTHON_ERRORS_HIGH_THRESHOLD or value_3 >= EVALUATION_ERRORS_HIGH_THRESHOLD):
                self.activation.activation = 0.95
                self.get_logger().debug(f"PNODE DEBUG: python_evaluation_errors_present_pnode: {value}")
            else:
                self.activation.activation = 0.0
            
            self.activation.timestamp = self.get_clock().now().to_msg()
        return self.activation

class PNodeBoredLow(PNode): #Pn2.1 and Pn2.2
    """
    PNode that represents the student being bored
    """
    def __init__(self, name='bored_low_pnode', class_name='cognitive_nodes.pnode.PNode', space_class=None, space=None, history_size=100, **params):
        super().__init__(name, class_name, space_class, space, history_size, **params)
    def calculate_activation(self, perception=None, activation_list=None):
        if activation_list!=None:
            perception={}
            for sensor in activation_list:
                activation_list[sensor]['updated']=False
                perception[sensor]=activation_list[sensor]['data']
        if perception:
            value_raw = perception.get('bored_perception')
            value = round(value_raw[0]['data'], 1)

            # Pn2.1 and Pn2.2: student not engaged > low threshold
            if value >= BORED_LOW_THRESHOLD and value < BORED_HIGH_THRESHOLD:
                self.activation.activation = 0.95
                self.get_logger().debug(f"PNODE DEBUG: bored_low_pnode: {value}")
            else:
                self.activation.activation = 0.0
            
            self.activation.timestamp = self.get_clock().now().to_msg()
        return self.activation

class PNodeBoredHigh(PNode): # Pn2.3
    """
    PNode that represents the student being highly bored
    """
    def __init__(self, name='bored_high_pnode', class_name='cognitive_nodes.pnode.PNode', space_class=None, space=None, history_size=100, **params):
        super().__init__(name, class_name, space_class, space, history_size, **params)
    def calculate_activation(self, perception=None, activation_list=None):
        if activation_list!=None:
            perception={}
            for sensor in activation_list:
                activation_list[sensor]['updated']=False
                perception[sensor]=activation_list[sensor]['data']
        if perception:
            value_raw = perception.get('teacher_type_perception')
            value = round(value_raw[0]['data'], 1)
            value_raw_2 = perception.get('teacher_present_perception')
            value_2 = round(value_raw_2[0]['data'], 1)
            value_raw_3 = perception.get('bored_perception')
            value_3 = round(value_raw_3[0]['data'], 1)

            # Pn2.3: USER2 & any USER present & student not engaged > high threshold
            if TEACHER_TYPE_UNDEFINED_THRESHOLD < value <= TEACHER_TYPE_MODERN_THRESHOLD and value_2 == TEACHER_PRESENT_THRESHOLD and value_3 >= BORED_HIGH_THRESHOLD:
                self.activation.activation = 0.95
                self.get_logger().debug(f"PNODE DEBUG: bored_high_pnode: {value}")
            else:
                self.activation.activation = 0.0
            
            self.activation.timestamp = self.get_clock().now().to_msg()
        return self.activation

class PNodeStandingLow(PNode): # Pn3.1
    """
    PNode that represents the student standing
    """
    def __init__(self, name='standing_low_pnode', class_name='cognitive_nodes.pnode.PNode', space_class=None, space=None, history_size=100, **params):
        super().__init__(name, class_name, space_class, space, history_size, **params)
    def calculate_activation(self, perception=None, activation_list=None):
        if activation_list!=None:
            perception={}
            for sensor in activation_list:
                activation_list[sensor]['updated']=False
                perception[sensor]=activation_list[sensor]['data']
        if perception:
            value_raw = perception.get('standing_perception')
            value = round(value_raw[0]['data'], 1)

            # Pn3.1: student standing up > low threshold
            if value >= STANDING_LOW_THRESHOLD and value < STANDING_HIGH_THRESHOLD:
                self.activation.activation = 0.95
                self.get_logger().debug(f"PNODE DEBUG: standing_low_pnode: {value}")
            else:
                self.activation.activation = 0.0
            
            self.activation.timestamp = self.get_clock().now().to_msg()
        return self.activation

class PNodeStandingHighPresent(PNode): # Pn3.2
    """
    PNode that represents the student standing for a long time with teacher present
    """
    def __init__(self, name='standing_high_present_pnode', class_name='cognitive_nodes.pnode.PNode', space_class=None, space=None, history_size=100, **params):
        super().__init__(name, class_name, space_class, space, history_size, **params)
    def calculate_activation(self, perception=None, activation_list=None):
        if activation_list!=None:
            perception={}
            for sensor in activation_list:
                activation_list[sensor]['updated']=False
                perception[sensor]=activation_list[sensor]['data']
        if perception:
            value_raw = perception.get('teacher_present_perception')
            value = round(value_raw[0]['data'], 1)
            value_raw_2 = perception.get('standing_perception')
            value_2 = round(value_raw_2[0]['data'], 1)

            # Pn3.2: any USER present & student standing up > high threshold
            if value == TEACHER_PRESENT_THRESHOLD and value_2 >= STANDING_HIGH_THRESHOLD:
                self.activation.activation = 0.95
                self.get_logger().debug(f"PNODE DEBUG: standing_high_present_pnode: {value}")
            else:
                self.activation.activation = 0.0
            
            self.activation.timestamp = self.get_clock().now().to_msg()
        return self.activation

class PNodeStandingHighAbsentOld(PNode): # Pn3.3
    """
    PNode that represents the student standing for a long time with an old-school teacher absent
    """
    def __init__(self, name='standing_high_absent_old_pnode', class_name='cognitive_nodes.pnode.PNode', space_class=None, space=None, history_size=100, **params):
        super().__init__(name, class_name, space_class, space, history_size, **params)
    def calculate_activation(self, perception=None, activation_list=None):
        if activation_list!=None:
            perception={}
            for sensor in activation_list:
                activation_list[sensor]['updated']=False
                perception[sensor]=activation_list[sensor]['data']
        if perception:
            value_raw = perception.get('teacher_type_perception')
            value = round(value_raw[0]['data'], 1)
            value_raw_2 = perception.get('teacher_present_perception')
            value_2 = round(value_raw_2[0]['data'], 1)
            value_raw_3 = perception.get('standing_perception')
            value_3 = round(value_raw_3[0]['data'], 1)

            # Pn3.3: USER1 & no USER present & student standing up > high threshold
            if value >= TEACHER_TYPE_OLD_THRESHOLD and value_2 == TEACHER_ABSENT_THRESHOLD and value_3 >= STANDING_HIGH_THRESHOLD:
                self.activation.activation = 0.95
                self.get_logger().debug(f"PNODE DEBUG: standing_high_absent_old_pnode: {value}")
            else:
                self.activation.activation = 0.0
            
            self.activation.timestamp = self.get_clock().now().to_msg()
        return self.activation
    
class PNodeStandingHighAbsentModern(PNode): # Pn3.4
    """
    PNode that represents the student standing for a long time with a modern teacher absent
    """
    def __init__(self, name='standing_high_absent_modern_pnode', class_name='cognitive_nodes.pnode.PNode', space_class=None, space=None, history_size=100, **params):
        super().__init__(name, class_name, space_class, space, history_size, **params)
    def calculate_activation(self, perception=None, activation_list=None):
        if activation_list!=None:
            perception={}
            for sensor in activation_list:
                activation_list[sensor]['updated']=False
                perception[sensor]=activation_list[sensor]['data']
        if perception:
            value_raw = perception.get('teacher_type_perception')
            value = round(value_raw[0]['data'], 1)
            value_raw_2 = perception.get('teacher_present_perception')
            value_2 = round(value_raw_2[0]['data'], 1)
            value_raw_3 = perception.get('standing_perception')
            value_3 = round(value_raw_3[0]['data'], 1)

            # Pn3.4: USER2 & not USER present & student standing up > high threshold
            if TEACHER_TYPE_UNDEFINED_THRESHOLD < value <= TEACHER_TYPE_MODERN_THRESHOLD and value_2 == TEACHER_ABSENT_THRESHOLD and value_3 >= STANDING_HIGH_THRESHOLD:
                self.activation.activation = 0.95
                self.get_logger().debug(f"PNODE DEBUG: standing_high_absent_modern_pnode: {value}")
            else:
                self.activation.activation = 0.0
            
            self.activation.timestamp = self.get_clock().now().to_msg()
        return self.activation
