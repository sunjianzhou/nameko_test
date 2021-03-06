import os
import sys
from flasgger import Swagger
from nameko.standalone.rpc import ClusterRpcProxy
from flask import Flask, jsonify, request
from gevent.pywsgi import WSGIServer
from gevent import monkey

monkey.patch_all()

cur_path = os.path.abspath(sys.argv[0])
work_space = os.sep.join(cur_path.split(os.sep)[:-2])
sys.path.append(work_space)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CONFIG = {'AMQP_URI': "pyamqp://guest:guest@localhost"}
Swagger(app)


@app.route('/hello', methods=['GET'])
def get_apis():
    return jsonify({"web_state": "success"})


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
    name = request.json["name"]
    with ClusterRpcProxy(CONFIG) as rpc:
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
    with ClusterRpcProxy(CONFIG) as rpc:
        result = rpc.nameko_service_2.hello(name=name)
        return result, 200


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    port = 8001
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()
