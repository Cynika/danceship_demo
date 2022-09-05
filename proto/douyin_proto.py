import time

from proto import doyin_live_pb2


def dict_barrage(timeline, uid, nickname, text):
    # 记录发言
    return {'timeline': timeline, 'uid': uid, 'nickname': nickname, 'text': text, 'state': 0}


def decode_proto(response):
    Resp = doyin_live_pb2.Response()
    Resp.ParseFromString(response)
    dicts = list()
    for i in Resp.messages:
        match i.method:
            case 'WebcastChatMessage':
                CM = doyin_live_pb2.ChatMessage()
                CM.ParseFromString(i.payload)
                dicts.append(dict_barrage(time.time(), CM.user.shortId, CM.user.nickname, CM.content))
            case 'WebcastGiftMessage':
                GM = doyin_live_pb2.GiftMessage()
                GM.ParseFromString(i.payload)
                content = f"弹幕礼物 {GM.gift.name} {GM.gift.diamondCount}"
                dicts.append(dict_barrage(time.time(), GM.user.shortId, GM.user.nickname, content))
            case _:
                pass
    return dicts
