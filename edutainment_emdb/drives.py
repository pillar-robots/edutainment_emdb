import rclpy
from copy import copy
import random
from math import exp, isclose
from cognitive_nodes.drive import DriveTopicInput, Drive
from builtin_interfaces.msg import Time as TimeMsg
from core.utils import class_from_classname

class DriveExponentialOpo(DriveTopicInput):
    def evaluate(self, perception=None):
        """
        Evaluates the drive value according to an inverted exponential function.

        :param perception: The given normalized perception.
        :type perception: dict
        :return: The valuation of the perception and its timestamp.
        :rtype: cognitive_node_interfaces.msg.Evaluation
        """
        self.old_evaluation = copy(self.evaluation)
        if self.input >= 0:
            a = 1-self.min_eval
            self.evaluation.evaluation = a*exp(-5*self.input) + self.min_eval
            if isclose(self.input, 1.0, ):
                self.evaluation.evaluation = 1.0
        else:
            self.evaluation.evaluation = 0.0
        self.evaluation.timestamp = self.get_clock().now().to_msg()

        return self.evaluation
