from model.live import Live


class Stage:
    def __init__(self):
        self.is_play = False
        self.is_live = False
        self.live = None
        self.vote_dict = {"红": "a", "蓝": "b", "a": "a", "b": "b"}

    def end(self):
        self.is_live = False
        self.live = None

    def battle(self, dp_remove: bool):
        self.is_live = True
        self.live = Live(dp_remove=dp_remove, a=0, b=0, love=0)

    def dance_2gh(self, dp_remove: bool):
        self.is_live = True
        self.live = Live(dp_remove=dp_remove, a=0, b=0, love=0)

    def msg_vote(self, msg: str, uid: str):
        if self.is_live is True:
            if msg in self.vote_dict.keys():
                group = self.vote_dict[msg]
                self.live.vote(group, 1, uid)
                return True

    def gift_vote(self, pool: str, num: str, price: str, uid: str):
        if self.is_live is True:
            if pool in self.vote_dict.keys():
                group = self.vote_dict[pool]
                total = int(num) * int(price) * 1
                self.live.vote(group, total, uid)
                return True


if __name__ == '__main__':
    stage = Stage()
    stage.dance_2gh(dp_remove=True)
    stage.live.get_vote("left", "1234")
    stage.live.get_vote("love", "1234")
    print(stage.live.votes)
