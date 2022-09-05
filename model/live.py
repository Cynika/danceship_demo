class Live:
    def __init__(self, dp_remove: bool, **kwargs):
        self.dp_remove = dp_remove
        self.votes = kwargs
        self.members = set()

    def vote(self, group: str, num: int, uid: str):
        if self.dp_remove and uid in self.members:
            return False
        else:
            if group in self.votes:
                self.votes[group] += num
                self.votes['love'] += num
                self.members.add(uid)
                return True
            else:
                return False


if __name__ == '__main__':
    v = {'3': 1}
    live = Live(dp_remove=True, a=0, b=0)
    live.vote("a", 2, "1234")
    live.vote("a", 1, "1234")
    v.update(live.votes)
    print(v)
