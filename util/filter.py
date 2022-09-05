# -*- coding: utf-8 -*-
import random

from util.Excption import WarnException
from model.user import User


def user_filter(dis, task):
    if task is None:
        raise WarnException("弹幕任务为空" + str(task.__dict__))
    if task.state != 0:
        return task
    user = User(uid=task.uid)
    if dis.block_user_set.__contains__(user):
        raise WarnException("黑名单用户" + str(task.__dict__))
    if dis.hall_user_set.__contains__(user) is False:
        task.args = ["加入"]
    return task


def task_filter(dis, task):
    if task is None:
        raise WarnException("无效弹幕任务" + str(task.__dict__))
    if task.state != 0:
        return task
    try:
        for i in dis.task_default:
            if task.args[0] == i:
                task.task = dis.task_default[i]['task']
                if 'args' in dis.task_default[i]:
                    args = {}
                    index = 1
                    for j in dis.task_default[i]['args'].keys():
                        match dis.task_default[i]['args'][j]:
                            case "random":
                                args.update({j: "random"})
                            case "default":
                                args.update({j: "default"})
                            case "user":
                                args.update({j: task.args[index]})
                            case _:
                                args.update({j: dis.task_default[i]['args'][j]})
                        index += 1
                    task.args = args
                else:
                    task.args = {"msg": task.args[0]}
                return task

        for i in dis.default['model']:
            if task.args[0] == i:
                task.task = 'model'
                task.args = {'model': task.args[0]}
                return task

        for i in dis.default['short_dance']:
            if task.args[0] == i:
                task.task = 'dance'
                task.args = {'short_dance': task.args[0]}
                return task

        task.task = 'call'
        task.args = {'msg': task.args[0]}
        return task

    except Exception:
        raise WarnException('弹幕任务解析失败' + str(task.__dict__))


def args_filter(dis, task):
    if task is None:
        raise WarnException("无效弹幕任务" + str(task.__dict__))
    if task.state != 0:
        return task
    try:
        for i in task.args:
            for j in dis.args_default:
                if i == j:
                    if task.args[i] == "random":
                        task.args[i] = random.choice(list(dis.default[i].keys()))
                    for k in dis.default[i]:
                        if task.args[i] == k:
                            task.args[i] = dis.default[i][k]
                            break
                    else:
                        task.args[i] = 'default'
        return task
    except Exception:
        raise WarnException('弹幕任务参数解析失败' + str(task.__dict__))
