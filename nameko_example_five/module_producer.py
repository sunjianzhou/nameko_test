import random
from nameko.rpc import rpc
from nameko.events import EventDispatcher
from nameko.timer import timer


class ClassOne:
    name = "producer"
    dispatch = EventDispatcher()

    def __init__(self):
        self.personal_name = "producer_center"
        self.age = 18

    @rpc
    def get_personal_info(self):
        return self.personal_name, self.age

    @rpc
    def dispatch_method(self, msg_type, payload):
        if msg_type == 0:
            self.dispatch("topic_one", payload)  # 发布topic_one消息
        elif msg_type == 1:
            self.dispatch("topic_two", payload)  # 发布topic_two消息
        else:
            self.dispatch("public_topic", payload)  # 发布public_topic消息

    @timer(interval=10)
    def producer(self):  # 定时发布消息，故而能定时触发任务
        num = random.randint(1, 10)
        msg_type = num % 3
        if msg_type == 0:
            message = "topic_one message: {}".format(num)
        elif msg_type == 1:
            message = "topic_two message: {}".format(num)
        else:
            message = "public message: {}".format(num)
        payload = {"message": message}
        self.dispatch_method(msg_type, payload)

    @rpc
    def get_data_from_web(self, task_id, topic, message):  # 通过web获取数据，进而通过数据触发任务
        if topic == "topic_one":
            msg_type = 0
        elif topic == "topic_two":
            msg_type = 1
        else:
            msg_type = 2
        payload = {"task_id": task_id, "message": message}
        self.dispatch_method(msg_type, payload)
