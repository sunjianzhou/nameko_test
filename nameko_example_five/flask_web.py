import json
import uuid
from flasgger import Swagger
from flask_nameko import FlaskPooledClusterRpcProxy
from flask import Flask, request
from gevent.pywsgi import WSGIServer
from gevent import monkey

monkey.patch_all(thread=False)  # 用于协程异步感知IO操作，打的补丁


def create_app():
    flask_app = Flask(__name__)
    flask_app.config['JSON_SORT_KEYS'] = False
    flask_app.config['JSON_AS_ASCII'] = False
    flask_app.config.update(dict(
        NAMEKO_AMQP_URI="pyamqp://guest:guest@localhost"
    ))
    return flask_app


app = create_app()
Swagger(app)  # 用于API注释可视化
rpc = FlaskPooledClusterRpcProxy()
rpc.init_app(app)  # 一次注册，绑定使用


@app.route('/', methods=['GET'])
def get_apis():
    return json.dumps({"web_state": "success"}), 200


@app.route('/hello_world', methods=['GET'])
def call_service_auto():
    """
        Micro Service for hello, say hello to the other people.
    中文说明：这是一个微服务间交流的接口。
    ---
        parameters:
          - in: query
            name: name
            required: true
            description: get result automatically.
            schema:
              type : string
              example: jessica
        responses:
          200:
            description: OK
    """
    topic = request.args.get("topic")
    if topic == "topic_one":
        result = rpc.consumer_one.read_data()
    else:
        result = rpc.consumer_two.read_data()
    return result, 200


@app.route('/hello_world', methods=['POST'])
def call_service_manual():
    """
        Micro Service for hello, say hello to the other people.
    中文说明：这是一个微服务间交流的接口。
    ---
        parameters:
          - in: query
            name: name
            required: true
            description: get result manually.
            schema:
              type : string
              example: jessica
        responses:
          200:
            description: OK
    """
    task_id = uuid.uuid1()
    topic = request.json.get("topic")
    message = request.json.get("message")

    # build data
    rpc.producer.get_data_from_web(task_id, topic, message)

    # get result from topic
    if topic == "topic_one":
        result = rpc.consumer_one.read_data(task_id)
    else:
        result = rpc.consumer_two.read_data(task_id)
    return result, 200


if __name__ == '__main__':
    port = 8001
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()
