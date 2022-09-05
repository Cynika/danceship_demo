from util.Excption import WarnException


class Task:
    def __init__(self, bar_dict):
        try:
            self.timeline = bar_dict['timeline']
            self.uid = int(bar_dict['uid'])
            self.nickname = bar_dict['nickname']
            self.task = ''
            self.state = bar_dict['state']
            # state
            # 0为用户请求
            # 1为游戏端执行成功回应
            # 2为游戏端执行失败回应
            # 3为管理员用户请求
            # 4为游戏端成功执行并完成回应
            if self.state == 0:
                args = []  # 支持@和空格分割
                for i in bar_dict['text'].split('@'):
                    for j in i.split():
                        args.append(j)
                self.args = args
            else:
                self.task = bar_dict['task']
                self.args = bar_dict['args']
        except Exception as e:
            raise WarnException('弹幕解析失败' + e.__str__() + str(bar_dict))


if __name__ == '__main__':
    text = "斗舞@text"
    v = []
    for a in text.split('@'):
        for b in a.split():
            v.append(b)
    print(v)
