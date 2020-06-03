import json
from nameko.rpc import rpc, RpcProxy
from nameko.events import event_handler


class ClassOne:
    name = "consumer_one"
    producer_rpc = RpcProxy("producer")  # 用于rpc建立连接

    data_result_auto = list()  # 这里没法用实例属性，因为nameko run后的实例，在flask里没法直接捕获到。
    data_result_manual = dict()  # 定时获取的结果用列表存储，手动触发的用字典存储

    def __init__(self):
        self.personal_name = "consumer_one"

    @rpc
    def talk_to_producer(self):  # 可用于连通性测试
        target_name, target_age = self.producer_rpc.get_personal_info()
        print("hello {}, I know your are {} years old!".format(target_name, target_age))
        return "{} call {} finished!".format(self.personal_name, target_name)

    @event_handler("producer", "topic_one")
    def personal_topic_data(self, payload):
        print("I'm consumer_one, received topic_one message from producer: {}".format(payload))
        task_id = payload.get("task_id")
        # here we can do some thing for this payload
        if not task_id:
            self.data_result_auto.append(payload)
        else:
            self.data_result_manual.update({task_id: payload})

    @event_handler("producer", "public_topic")
    def public_topic_data(self, payload):
        print("I'm consumer_one, received public message from producer: {}".format(payload))
        task_id = payload.get("task_id")
        # here we can do some thing for this payload
        if not task_id:
            self.data_result_auto.append(payload)
        else:
            self.data_result_manual.update({task_id: payload})

    @rpc
    def read_data(self, task_id=None):
        if task_id is None:  # 自动定时任务获得的结果
            if not self.data_result_auto:
                return "consumer_one has no message the current"
            else:
                return json.dumps(self.data_result_auto.pop())
        else:   # 主动触发获得的结果
            if not self.data_result_manual.get(task_id):
                return "consumer_one has no message the current"
            else:
                return json.dumps(self.data_result_manual.pop(task_id))  # 获取结果，并删除结果
