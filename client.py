import json
import socket
import sys
from functools import wraps


class Client(socket.socket):
    def __init__(self, server_address):
        # 1. 设置服务器套接字
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        # 2. 链接服务器
        try:
            self.connect(server_address)
        except Exception as e:
            raise e

    def send_json(self, send_data):
        # 3. 发送数据
        self.send(json.dumps(send_data).encode('utf-8'))

    def recv_json(self):
        # 4. 接受数据
        re_data = self.recv(2048).decode('utf-8').split('\x00')
        call_dict = json.loads(re_data[0])
        return call_dict


def polling(func):
    @wraps(func)
    def call_func():
        try:
            while True:
                func()
        except ConnectionResetError:
            sys.exit('网络中断,请重新启动')

    return call_func
