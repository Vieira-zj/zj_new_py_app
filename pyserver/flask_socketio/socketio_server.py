# coding=utf8

import os
import json

from flask import Flask
from flask import request
from flask import render_template
from flask_session import Session
from flask_socketio import SocketIO

port = 8001
secret_key = os.urandom(24)
host_list = ['127.0.0.1']

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = True
app.config.from_object(__name__)
Session(app)
socket_io = SocketIO(app)


@app.route('/listen', methods=['post', 'get'])
def listen_func():
    """ 监听发送来的消息，并使用socketio向所有客户端发送消息 """
    msg = {'message': 'unknown error'}
    data = request.args['data'] if request.args.get(
        'data') else request.form.get('data')
    if data:
        socket_io.emit(data=data, event='msg')  # js客户端on绑定这个event的事件
        msg['message'] = 'success'
    return json.dumps(msg)


@socket_io.on('login')
def quotations_func(msg):
    """ 客户端连接 """
    print(msg)
    sid = request.sid
    host = request.host
    can = False
    if host in host_list or host.startswith('local'):
        can = True

    if can:
        socket_io.emit(event='login', data=json.dumps(
            {'message': 'login success!'}))
    else:
        socket_io.emit(event='login', data=json.dumps(
            {'message': 'login refuse!'}))
        socket_io.server.disconnect(sid)


@app.route('/index')
def home_func():
    return render_template('index.html')


if __name__ == '__main__':

    socket_io.run(app=app, host='0.0.0.0', port=port, debug=True)
