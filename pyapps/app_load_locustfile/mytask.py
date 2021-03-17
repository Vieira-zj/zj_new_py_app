# coding: utf-8

def task(weight=1):
    """ @task 注解 """
    def deco_func(func):
        if func.__name__ in ('on_stop', 'on_start'):
            print('@task should not be on func on_stop/on_start')
        func.task_weight = weight  # func 添加一个 weight 属性
        return func

    if callable(weight):
        # for declare @task
        func = weight
        weight = 1
        return deco_func(func)
    else:
        # for declare @task(3)
        return deco_func


def get_tasks_from_classes(class_dict):
    ret_tasks = []
    for item in class_dict.values():
        # func with attr "task_weight"
        if 'task_weight' in dir(item):
            for _ in range(item.task_weight):
                ret_tasks.append(item)

    return ret_tasks


class UserMeta(type):

    def __new__(mcs, classname, bases, class_dict):
        # 设置 tasks 和 abstract 静态成员变量
        tasks = get_tasks_from_classes(class_dict)
        class_dict['tasks'] = tasks

        if not class_dict.get('abstract'):
            class_dict['abstract'] = False

        return type.__new__(mcs, classname, bases, class_dict)
