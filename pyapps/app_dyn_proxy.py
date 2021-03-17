class Cat(object):

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def sayHi(self):
        print('hi, my name is ' + self.name)

    def run(self, speed):
        print(f"i am running at {speed}/m...")


class CatProxy(object):
    """ 动态代理 Cat 类的行为 """

    def __init__(self, cat: Cat):
        self._cat = cat

    def execute(self, fn_name, *arg, **kwargs):
        if not hasattr(self._cat, fn_name):
            raise AttributeError(f"attribute [{fn_name}] not exist!")
        fn = getattr(self._cat, fn_name)
        if not callable(fn):
            raise Exception(f"function [{fn_name}] is not callable!")
        fn(*arg, **kwargs)

    def __getattr__(self, name):
        """ 调用不存在的方法时，进入 __getattr__ """
        def _func(*args, **kwargs):
            self.execute(name, *args, **kwargs)

        _func.__name__ = name
        return _func


if __name__ == '__main__':

    cat = Cat('miroo')
    proxy = CatProxy(cat)
    proxy.sayHi()
    print(proxy.sayHi.__name__)
    proxy.run(10)

    proxy.test()  # func not exist

    print('proxy demo done.')
