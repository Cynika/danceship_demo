import json
import threading
import time
import webbrowser
import hashlib
from multiprocessing import Queue
from multiprocessing.managers import BaseManager
from playwright.sync_api import sync_playwright as playwright


class WechatBarrage:
    def __init__(self):
        try:
            self.bar_que = Queue()
            BaseManager.register('get_queue', callable=lambda: self.bar_que)
            self.manager = BaseManager(address=('', 52000), authkey=b'1')
        except Exception as e:
            raise e

    def start(self):
        try:
            threading.Thread(target=manager_server, args=(self.manager,)).start()
            threading.Thread(target=play, args=()).start()
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


def client_start():
    m = BaseManager(address=('127.0.0.1', 52000), authkey=b'1')
    m.connect()
    queue = m.get_queue()
    return queue


def chat_barrage(timeline, uid, nickname, text):
    # 记录发言
    return {'timeline': timeline, 'uid': uid, 'nickname': nickname, 'text': text, 'state': 0}


def gift_barrage(timeline, uid, nickname, gift, count):
    # 记录发言
    return {'timeline': timeline, 'uid': uid, 'nickname': nickname, 'text': f"礼物 {gift} {count} 1", 'state': 0}


def login(page):
    page.goto("https://channels.weixin.qq.com/platform/login")
    qrcode = page.get_attribute(".qrcode", "src")
    img = '<div style=\'text-align:center\'><img src="' + qrcode + '"/></div>'
    tip = '<h1 style=\'text-align:center\'>请15秒内微信扫码登录</h1>'
    js = '<script type="text/javascript">function close_it(){setTimeout("self.close()", 15000);}close_it();</script>'
    html_file = open("login_qrcode.html", "w")
    html_file.write(img + tip + js)
    webbrowser.open("login_qrcode.html")


def play():
    def run(p):
        browser = p.webkit.launch(headless=True)
        page = browser.new_page()
        return page

    try:
        with playwright() as pw:
            main_page = run(pw)
            login(main_page)
            time.sleep(15)
            main_page.goto("https://channels.weixin.qq.com/platform/live/liveBuild")
            main_page.on("response", filter_response)
            catch_gift(main_page)
            main_page.wait_for_timeout(100000000)
    except Exception as e:
        raise e


def catch_gift(page):
    name = 'null'
    gift = 'null'
    while True:
        time.sleep(0.1)
        try:
            container = page.locator(".live-message-scroller-container")
            messages = container.locator(".live-message-item-container")
            last_message = messages.nth(-1)
            message_type = last_message.locator(".message-type").inner_html()
            if message_type == '礼物':
                message_present_desc = last_message.locator(".message-present-desc").inner_html()
                message_present_count = last_message.locator(".message-present-count").inner_html()
                mlist = message_present_desc.split("送出了")
                count = message_present_count.split("x")
                if name != mlist[0] and gift != mlist[1]:
                    name = mlist[0]
                    gift = mlist[1]
                    uid = int(hashlib.sha1(name.encode('utf-8')).hexdigest(), 16) % (14 ** 8)
                    queue = client_start()
                    bar = gift_barrage(time.time(), uid, name, gift, count)
                    queue.put(bar)
        except Exception:
            pass


def filter_response(response):
    if 'https://channels.weixin.qq.com/cgi-bin/mmfinderassistant-bin/live/msg' in response.url:
        json_body = json.loads(response.body().decode('utf-8'))
        if json_body["data"]["msgList"] is not None:
            for i in json_body["data"]["msgList"]:
                if i is not None:
                    queue = client_start()
                    uid = int(hashlib.sha1(i['nickname'].encode('utf-8')).hexdigest(), 16) % (14 ** 8)
                    bar = chat_barrage(time.time(), uid, i['nickname'], i['content'])
                    queue.put(bar)
    else:
        pass
    return response
