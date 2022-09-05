import json
import multiprocessing
import os
import threading
import time
from multiprocessing import Process, Queue

from douyin import start_recv, play
from wechat_barrage import WechatBarrage
from client import Client, polling
from dispatcher import Dispatcher
from model.hall import Hall
from model.task import Task
from model.user import load_user_set
from util.logger import Logger, loop_exc_log

config = json.load(open('config.json', 'r', encoding="utf-8"))
logger = Logger(logger_name=config['logger_name'], log_file=config['log_file']).get_log()

default_dir = config['default_dir']
user_data_dir = config['user_data_dir']
media_dir = config['media_dir']
douyin_room_id = config['douyin_room_id']
server_address = (config['server_address'], config['port'])
user_set = load_user_set(user_data_dir + 'user_data.json')
block_user_set = load_user_set(user_data_dir + 'block_user_data.json')
hall = Hall(user_set, block_user_set, user_data_dir, media_dir)


def load_default(def_dir):
    default = dict()
    # 列出文件夹下所有的目录与文件
    for i in os.listdir(def_dir):
        default.update({i.split('.')[0]: json.load(open(def_dir + i, 'r', encoding="utf-8"))})
    return default


def weixin_barrage_run(bar_que):
    @loop_exc_log(logger)
    def dispatcher_loop():
        # 暂停防止cpu占用过高
        time.sleep(0.1)
        # 获取弹幕
        bar = barrage.get_barrage()
        if bar is not None:
            bar_que.put(bar)

    barrage = WechatBarrage()
    barrage.start()
    print("微信弹幕抓取组件启动完成")
    while True:
        dispatcher_loop()


@loop_exc_log(logger)
def douyin_barrage_run(bar_que):
    print("抖音页面抓取组件启动完成")
    try:
        Process(target=play, args=(douyin_room_id,)).start()
        Process(target=start_recv, args=(bar_que,)).start()
    except Exception as e:
        print("err", e)


def dispatcher_run(bar_que, ta_que):
    @loop_exc_log(logger)
    def dispatcher_loop():
        time.sleep(0.1)
        bar = bar_que.get(True)
        if bar is not None:
            task = dispatcher.three_filter(Task(bar))
            dis_task = dispatcher.task_dispatch(task)
            if dis_task is not None:
                ta_que.put(dis_task)

    dispatcher = Dispatcher(load_default(default_dir), hall)
    print("事务分配器组件启动完成")
    while True:
        dispatcher_loop()


def client_run(ta_que, bar_que):
    @loop_exc_log(logger)
    @polling
    def send_loop():
        time.sleep(0.1)
        task = ta_que.get(True)
        if task is not None:
            client.send_json(task.__dict__)

    @loop_exc_log(logger)
    @polling
    def recv_loop():
        time.sleep(0.1)
        call = client.recv_json()
        if call is not None:
            bar_que.put(call)

    client = Client(server_address)
    threading.Thread(target=send_loop).start()
    threading.Thread(target=recv_loop).start()
    print("游戏端通信组件启动完成")


if __name__ == '__main__':
    multiprocessing.freeze_support()
    task_que = Queue()
    barrage_que = Queue()
    Process(target=weixin_barrage_run, args=(barrage_que,)).start()
    Process(target=client_run, args=(task_que, barrage_que,)).start()
    Process(target=dispatcher_run, args=(barrage_que, task_que,)).start()
