import rclpy
from cognitive_nodes.perception import Perception
from core.utils import perception_dict_to_msg

class EdutainmentPerception(Perception):
    """Edutainment Perception class"""
    def __init__(self, name='perception',
                 class_name='cognitive_nodes.perception.Perception',
                 default_msg=None,
                 default_topic=None,
                 normalize_data=None,
                 **params):
        super().__init__(name, class_name, default_msg, default_topic, normalize_data, **params)
        self.value = 0.0
    def process_and_send_reading(self):
        """
        Publishes the current perception value (Float32) to its topic.
        The value should already be set externally in self.value.
        """
        sensor = {}
        value = []
        if isinstance(self.reading.data, list):
            for perception in self.reading.data:
                value.append(
                    dict(
                            teacher_present_perception=perception.teacher_present_perception,
                            teacher_type_perception=perception.teacher_type_perception,
                            student_type_perception=perception.student_type_perception,
                            challenge_completion_perception=perception.challenge_completion_perception,
                            python_errors_perception=perception.python_errors_perception,
                            evaluation_error_streak_perception=perception.evaluation_error_streak_perception,
                            error_streak_perception=perception.error_streak_perception,
                            bored_perception=perception.bored_perception,
                            standing_perception=perception.standing_perception
                    )
                )
        else:
            value.append(dict(data=self.reading.data))
        sensor[self.name] = value
        self.get_logger().debug("Publishing normalized " + self.name + " = " + str(sensor))
        sensor_msg = perception_dict_to_msg(sensor)
        self.publish_msg.perception=sensor_msg
        self.publish_msg.timestamp=self.get_clock().now().to_msg()
        self.perception_publisher.publish(self.publish_msg)
