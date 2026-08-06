import rclpy
import numpy as np
from cognitive_nodes.perception import Perception
from core.container import Container

class EdutainmentPerception(Perception):
    """Edutainment Perception class"""
    def __init__(self, name='perception', class_name='cognitive_nodes.perception.Perception',
                 default_msg=None, default_topic=None, normalize_data=None, **params):
        super().__init__(name=name, class_name=class_name, default_msg=default_msg, default_topic=default_topic, normalize_data=normalize_data, **params)
        self.value = 0.0
    def process_and_send_reading(self):
        """
        Publishes the current perception value (Float32) to its topic.
        The value should already be set externally in self.value.
        """
        if isinstance(self.reading, list):
            if len(self.reading) == 0:
                return # No reading to process, return immediately
            for perception in self.reading:
                teacher_present_perception=perception.teacher_present_perception,
                teacher_type_perception=perception.teacher_type_perception,
                student_type_perception=perception.student_type_perception,
                challenge_completion_perception=perception.challenge_completion_perception,
                python_error_streak_perception=perception.python_error_streak_perception,
                python_error_new_perception=perception.python_error_new_perception,
                evaluation_error_streak_perception=perception.evaluation_error_streak_perception,
                evaluation_error_new_perception=perception.evaluation_error_new_perception,
                bored_perception=perception.bored_perception,
                standing_perception=perception.standing_perception
                data = np.array([teacher_present_perception, teacher_type_perception, student_type_perception, challenge_completion_perception, python_error_streak_perception, python_error_new_perception, evaluation_error_streak_perception, evaluation_error_new_perception, bored_perception, standing_perception])
                labels = ["teacher_present_perception", "teacher_type_perception", "student_type_perception", "challenge_completion_perception", "python_error_streak_perception", "python_error_new_perception", "evaluation_error_streak_perception", "evaluation_error_new_perception", "bored_perception", "standing_perception"]
        else:
            data = np.array([self.reading.data])
            labels = ["data"]
        
        if self.container is None:
            self.container = Container(self.name, max_size=1, container_type="perception", labels=labels)
        self.container.push(data, labels, timestamps=self.get_clock().now().nanoseconds)

        self.get_logger().debug("Publishing normalized " + self.name + " = " + str(self.container))
        sensor_msg = self.container.to_msg()
        self.perception_publisher.publish(sensor_msg)
