from model.stage import Stage
from model.user import User, save_user_set, get_user_in_set, update_user_in_set
from util.Excption import WarnException


class Hall:
    def __init__(self, user_set, block_user_set, user_data_dir, media_dir):
        self.user_set = user_set
        self.block_user_set = block_user_set

        self.user_data_dir = user_data_dir
        self.media_dir = media_dir

        self.hall_user_set = set()
        self.max_user = 100
        self.stage = Stage()

    def add_user(self, uid, nickname, timeline, pool="a", sc=0, gender='None'):
        user = User(uid=uid)
        if user in self.hall_user_set:
            raise WarnException("已存在用户")
        user = User(uid=uid, nickname=nickname, active_time=timeline, pool=pool, sc=sc, gender=gender)
        if len(self.hall_user_set) < self.max_user:
            self.hall_user_set.add(user)
            return True
        else:
            raise WarnException("舞厅已满")

    def remove_user(self, uid):
        user = User(uid=uid)
        if user in self.hall_user_set:
            self.hall_user_set.remove(user)
            return True
        else:
            raise WarnException("移除失败，用户不在舞厅中")

    def update_user(self, uid, nickname, timeline, pool="a", sc=0, gender='None'):
        user = User(uid=uid)
        if user in self.hall_user_set:
            if sc != 0:
                sc = get_user_in_set(self.hall_user_set, User(uid=uid))["sc"] + int(sc)
            if gender == 'None':
                gender = get_user_in_set(self.hall_user_set, User(uid=uid))["gender"]
            if pool == 0:
                gender = get_user_in_set(self.hall_user_set, User(uid=uid))["pool"]
            self.hall_user_set.remove(user)
            self.add_user(uid, nickname, timeline, pool=pool, sc=sc, gender=gender)
            return True
        raise WarnException("更新失败，用户不在舞厅中")

    def nickname_find_uid(self, uid, nickname):
        for i in self.hall_user_set:
            if i["nickname"] == nickname:
                return i["uid"]
        for j in self.hall_user_set:
            if j["uid"] != uid:
                return j["uid"]
        return False

    def save_new_user(self, user):
        user.update(sc=0, gender='None')
        self.user_set.add(user)

    def save_hall_user(self, user):
        u = get_user_in_set(self.hall_user_set, user)
        update_user_in_set(self.user_set,
                           User(uid=u['uid'], nickname=u['uid'], active_time=u['active_time'], sc=u['sc'],
                                gender=u['gender']))

    def save_commit(self):
        save_user_set(self.user_set, self.user_data_dir + 'user_data.json')
