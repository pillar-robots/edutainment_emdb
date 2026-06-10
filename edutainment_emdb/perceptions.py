import rclpy
from cognitive_nodes.perception import Perception
from core.utils import perception_dict_to_msg


class EdutainmentPerceptionSim(Perception):
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
                        #guide_face_id=perception.guide_face_id,
                        #group_characterization=perception.group_characterization,
                        #people_placed=perception.people_placed,
                        #group_engagement=perception.group_engagement
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
                            studentType=perception.studentType,
                            teacherType=perception.teacherType,
                            python_errors=perception.python_errors,
                            # noise_level=perception.noise_level,
                            # age=perception.age,
                            # blue_area=perception.blue_area,
                            # spatial=perception.spatial,
                            # posture_state=perception.posture_state,
                            # interpersonal_spacing=perception.interpersonal_spacing,
                            # guide=perception.guide,
                            # engage=perception.engage,
                            # timeline=perception.timeline,
                            # people=perception.people
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