import asyncio
import multiprocessing
from multiprocessing import Process, Queue
import websockets
from playwright.sync_api import sync_playwright as playwright

from util.douyin_catch import catch


def play(room_id):
    def run(p):
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        return page

    try:
        with playwright() as pw:
            main_page = run(pw)
            lid = str(room_id)
            main_page.route(
                "972.6efdc2f8.js",
                lambda route: route.fulfill(path="./972.6efdc2f8.js")
            )
            main_page.goto("https://live.douyin.com/" + lid)
            main_page.wait_for_timeout(100000000)

    except Exception as e:
        raise e


def start_recv(que):
    async def check_permit(websocket):
        send_text = 'lx'
        await websocket.send(send_text)
        return True

    async def recv_msg(websocket, que):
        while 1:
            recv_text = await websocket.recv()
            bar = catch(recv_text)
            if bar is not None:
                print(bar)
                que.put(bar)

    async def main_logic(websocket):
        await check_permit(websocket)
        await recv_msg(websocket, que)

    start_server = websockets.serve(main_logic, '127.0.0.1', 8921)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    que = Queue()
    Process(target=play, args=(124126296651,)).start()
    Process(target=start_recv, args=(que,)).start()
