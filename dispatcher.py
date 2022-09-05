from model.user import User, get_user_in_set
from util.Excption import InfoException, WarnException
from util.filter import user_filter, task_filter, args_filter


class Dispatcher:
    def __init__(self, default, hall):
        self.default = default
        self.task_default = self.default['task_default']
        self.args_default = self.default['args_default']

        self.hall = hall
        self.stage = self.hall.stage
        self.user_set = self.hall.user_set
        self.block_user_set = self.hall.block_user_set
        self.hall_user_set = self.hall.hall_user_set

    def three_filter(self, task):
        return args_filter(self, (task_filter(self, (user_filter(self, task)))))

    def task_dispatch(self, task):
        if task.state == 0:
            match task.task:
                case 'join':
                    if self.user_set.__contains__(User(uid=task.uid)):
                        return task
                    else:
                        self.hall.save_new_user(
                            User(uid=task.uid, nickname=task.nickname, active_time=task.timeline))
                        return task
                case 'model_dance':
                    if 'girl_model' in task.args:
                        task.args = {'model': task.args['girl_model'], "short_dance": "default"}
                    if 'boy_model' in task.args:
                        task.args = {'model': task.args['boy_model'], "short_dance": "default"}
                    return task
                case 'pool_scale':
                    return task
                case 'call':
                    if self.stage.is_live:
                        if self.stage.msg_vote(task.args['msg'], task.uid):
                            task.task = 'vote_msg'
                            task.args.update(self.stage.live.votes)
                            return task
                    return task
                case 'call_all':
                    return task
                case 'gift':
                    task.args.update({'msg': f"我送出了{task.args['name']}"})
                    if self.stage.is_live:
                        pool = get_user_in_set(self.hall_user_set, User(uid=task.uid))['pool']
                        if self.stage.gift_vote(pool, task.args['num'], task.args['price'], task.uid):
                            task.task = 'vote_gift'
                            task.args.update(self.stage.live.votes)
                            return task
                    return task
                case 'shot_me':
                    if self.stage.is_play is False:
                        return task
                case 'lead':
                    if self.stage.is_play is False:
                        return task
                case 'battle':
                    if self.stage.is_play is False:
                        target_id = self.hall.nickname_find_uid(task.uid, task.args['target_id'])
                        task.args.update({"target_id": target_id})
                        return task
                case 'dance_2gh':
                    if self.stage.is_play is False:
                        target_id = self.hall.nickname_find_uid(task.uid, task.args['target_id'])
                        task.args.update({"target_id": target_id})
                        return task

        if task.state == 1:
            match task.task:
                case 'join':
                    if self.hall_user_set.__contains__(User(uid=task.uid)) is False:
                        self.hall.add_user(task.uid, task.nickname, task.timeline, pool=task.args['pool'])
                        raise InfoException("已进入舞厅" + str(task.__dict__))
                case 'model_dance':
                    self.hall.update_user(task.uid, task.nickname, task.timeline)
                    raise InfoException("已切换模型,跳舞信息成功" + str(task.__dict__))
                case 'pool_scale':
                    self.hall.update_user(task.uid, task.nickname, task.timeline, pool=task.args['pool'])
                    raise InfoException("改变大小或舞池成功" + str(task.__dict__))
                case 'call':
                    raise InfoException("发言成功" + str(task.__dict__))
                case 'call_all':
                    raise InfoException("一起喊成功" + str(task.__dict__))
                case 'gift':
                    self.hall.update_user(task.uid, task.nickname, task.timeline)
                    self.hall.update_user(task.uid, task.nickname, task.timeline, sc=task.args['price'])
                    self.hall.save_hall_user(User(uid=task.uid))
                    raise InfoException("礼物成功" + str(task.__dict__))
                case 'shot_me':
                    raise InfoException("给镜头成功" + str(task.__dict__))
                case 'lead':
                    self.stage.is_play = True
                    self.stage.dance_2gh(dp_remove=False)
                    raise InfoException("领舞开始" + str(task.__dict__))
                case 'battle':
                    self.stage.is_play = True
                    self.stage.battle(dp_remove=True)
                    raise InfoException("斗舞开始" + str(task.__dict__))
                case 'dance_2gh':
                    self.stage.is_play = True
                    self.stage.dance_2gh(dp_remove=False)
                    raise InfoException("合舞开始" + str(task.__dict__))

        if task.state == 2:
            match task.task:
                case 'join':
                    raise WarnException("加入失败" + str(task.__dict__))
                case 'model_dance' | 'pool_scale':
                    raise WarnException("切换模型，跳舞信息或舞池大小失败" + str(task.__dict__))
                case 'call' | 'call_all':
                    raise WarnException("发言失败" + str(task.__dict__))
                case 'lead' | 'battle' | 'dance_2gh':
                    self.stage.is_play = False
                    raise WarnException("领舞,斗舞或合舞失败" + str(task.__dict__))

        if task.state == 3:
            match task.task:
                case 'lead' | 'battle' | 'dance_2gh':
                    self.stage.is_play = False
                    self.stage.end()
                    self.hall.save_commit()
                    raise InfoException("领舞,斗舞或合舞结束" + str(task.__dict__))


if __name__ == '__main__':
    pass
