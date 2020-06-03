import json
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
def hello():
    """
        Micro Service for hello, say hello to the other people.
    中文说明：这是一个微服务间交流的接口。
    ---
        parameters:
          - in: query
            name: name
            required: true
            description: People who talk first.
            schema:
              type : string
              example: jessica
        responses:
          200:
            description: OK
    """
    name = request.args.get("name")
    if name == "service_1":
        result = rpc.service_1.communication()
    else:
        result = rpc.service_2.communication()
    return result, 200


if __name__ == '__main__':
    port = 8001
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()
