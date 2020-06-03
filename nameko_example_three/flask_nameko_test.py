import json
from flasgger import Swagger
from flask_nameko import FlaskPooledClusterRpcProxy
from flask import Flask, request
from gevent.pywsgi import WSGIServer
from gevent import monkey

monkey.patch_all()      # 用于协程异步感知IO操作，打的补丁


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
        Micro Service for hello, say hello to you.
    中文说明：这是一个say hello的接口。
    ---
        parameters:
          - in: query
            name: name
            required: true
            description: your name.
            schema:
              type : string
              example: jessica
        responses:
          200:
            description: OK
    """
    name = request.args.get("name")
    result = rpc.nameko_service_1.hello(name=name)
    return result, 200


@app.route('/hello_world', methods=['POST'])
def hello_people():
    """
        Micro Service for hello_people
    中文说明：这是一个say how are you的接口。
    ---
        parameters:
          - name: body
            in: body
            required: true
            schema:
              id: data
              properties:
                name:
                  type: string
        responses:
          200:
            description: say how are you to you.
    """
    name = request.json["name"]
    result = rpc.nameko_service_2.hello(name=name)
    return result, 200


if __name__ == '__main__':
    port = 8001
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()
