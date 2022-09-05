import json


def catch(bar_s: str):
    bar = json.loads(bar_s)
    if "common" in bar:
        try:
            match bar["common"]["method"]:
                case 'WebcastChatMessage':
                    return {'timeline': bar['eventTime'], 'uid': bar["user"]["shortId"],
                            'nickname': bar["user"]["nickname"],
                            'text': bar["content"], 'uface': bar["user"]["avatarThumb"]["urlListList"][0], 'state': 0}
                case 'WebcastGiftMessage':
                    return {'timeline': bar["common"]['createTime'], 'uid': bar["user"]["shortId"],
                            'nickname': bar["user"]["nickname"],
                            'text': f"礼物 {bar['gift']['name']} {bar['comboCount']} {bar['gift']['diamondCount']}",
                            'uface': bar["user"]["avatarThumb"]["urlListList"][0], 'state': 0}

        except Exception as e:
            pass
            # print(e, bar_s)
