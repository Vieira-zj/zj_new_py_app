# coding: utf-8
import locust
import os
import importlib
import inspect


def load_locustfile(path):
    """
    统计 locust file 中 task ratio 的信息。

    Output:
    {'QuickstartUser': {'ratio': 1.0, 'tasks': {'hello_world': {'ratio': 0.25}, 'view_item': {'ratio': 0.75}}}}
    """
    _, locustfile = os.path.split(path)
    fullname = os.path.splitext(locustfile)[0]
    source = importlib.machinery.SourceFileLoader(fullname, path)
    imported = source.load_module(fullname)
    if imported.__doc__:
        print('doc:', imported.__doc__)

    # 从加载的 module 文件中找到 QuickstartUser 类
    user_classes = {name: value for name, value in vars(imported).items(
    ) if inspect.isclass(value) and hasattr(value, 'abstract') and not value.abstract}

    user_classes = list(user_classes.values())
    print(get_task_ratio_dict(user_classes))

    # run a task
    clazz, foo_task = get_foo_task(user_classes)
    assert foo_task is not None and callable(foo_task)
    _self = clazz()
    foo_task(_self)


def get_task_ratio_dict(tasks, parent_ratio=1.0):
    """
    Return a dict containing task execution ratio info.
    """
    ratio = {}
    for task in tasks:
        ratio.setdefault(task, 0)
        ratio[task] += 1

    divisor = len(tasks) / parent_ratio
    ratio_percent = dict((k, float(v) / divisor) for k, v in ratio.items())

    task_dict = {}
    for task, pct in ratio_percent.items():
        d = {"ratio": pct}
        if inspect.isclass(task):
            d["tasks"] = get_task_ratio_dict(task.tasks)
        task_dict[task.__name__] = d

    return task_dict


def get_foo_task(user_classes):
    for clazz in user_classes:
        if inspect.isclass(clazz):
            for task in clazz.tasks:
                if task.__name__ == 'foo':
                    return clazz, task


if __name__ == '__main__':

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(cur_dir, 'locust_demo.py')
    load_locustfile(path)

    print('app load source Done.')
