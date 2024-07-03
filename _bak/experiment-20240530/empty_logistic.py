from holon.HolonicAgent import HolonicAgent
from holon.logistics.base_logistic import BaseLogistic


class EmptyLogistic(BaseLogistic):
    def __init__(self, agent:HolonicAgent, request_id="", job_topic=None):
        self.agent = agent


    def publish(self, topic, payload, request_payload=None):
        # print(f"publish, topic: {topic}, payload: {payload}")
        self.agent.publish(topic, payload)


    def subscribe(self, topic, topic_handler=None):
        # print(f"subscribe, topic: {topic}, topic_handler: {topic_handler}")
        self.agent.subscribe(topic, topic_handler=topic_handler)
        