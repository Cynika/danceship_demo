import threading
from multiprocessing import Queue
from multiprocessing.managers import BaseManager

from playwright.sync_api import sync_playwright as playwright

from proto.douyin_proto import decode_proto


class DouyinBarrage:
    def __init__(self, room_id):
        try:
            self.room_id = room_id
            self.bar_que = Queue()
            BaseManager.register('get_queue', callable=lambda: self.bar_que)
            self.manager = BaseManager(address=('', 52111), authkey=b'1')
        except Exception as e:
            raise e

    def start(self):
        try:
            threading.Thread(target=manager_server, args=(self.manager,)).start()
            threading.Thread(target=play, args=(self.room_id,)).start()
        except Exception as e:
            raise e

    def get_barrage(self):
        bar = self.bar_que.get(True)
        return bar


def manager_server(m):
    try:
        s = m.get_server()
        s.serve_forever()
    except Exception as me:
        m.shutdown()
        raise me


def play(room_id):
    def run(p):
        browser = p.webkit.launch(headless=True)
        page = browser.new_page()
        return page

    try:
        with playwright() as pw:
            main_page = run(pw)
            lid = str(room_id)
            main_page.goto("https://live.douyin.com/" + lid)
            main_page.on("response", filter_response)
            main_page.wait_for_timeout(100000000)
    except Exception as e:
        raise e


def filter_response(response):
    if 'https://live.douyin.com/webcast/im/fetch/' in response.url:
        m = BaseManager(address=('127.0.0.1', 52111), authkey=b'1')
        m.connect()
        queue = m.get_queue()
        dicts = decode_proto(response.body())
        for i in dicts:
            if i != 'None':
                print(i)
                queue.put(i)
    else:
        pass
    return response


if __name__ == '__main__':
    que = Queue()
    db = DouyinBarrage(565603863848)
    db.start()
