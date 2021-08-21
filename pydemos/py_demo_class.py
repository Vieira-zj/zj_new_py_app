# -*- coding: utf-8 -*-
'''
Created on 2019-03-17
@author: zhengjin

Python class and meta class examples.
'''

from typing import List


def py_base_ext():
    import py_demo_base
    py_demo_base.py_base_ex02()


# example 01, 使用函数当做元类
def py_class_ex01():

    def upper_attr(*args, **kwargs):
        '''
        Return a class object, attrs are upper case.
        '''
        future_class_name, future_class_parents, future_class_attr = args
        print('upper_attr is invoked, cls attrs:', future_class_attr.items())
        attrs = ((name, value) for name,
                 value in future_class_attr.items() if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)

        return type(future_class_name, future_class_parents, uppercase_attr)

    class Foo(metaclass=upper_attr):
        # __metaclass__ = upper_attr
        bar = 'bip'

    # main
    print('attr bar:', hasattr(Foo, 'bar'))
    print('attr BAR:', hasattr(Foo, 'BAR'))
    print('BAR:', Foo.BAR)

    f = Foo()
    print('Foo class:', f.__class__)
    print('Foo super class:', f.__class__.__class__)  # type


# example 02, 使用class来当做元类
def py_class_ex02():

    class UpperAttrMetaclass(type):  # extends from "type"
        def __new__(cls, *args, **kwargs):
            name, bases, dct = args
            print('upper_attr is invoked, cls attrs:', dct.items())
            attrs = ((name, value)
                     for name, value in dct.items() if not name.startswith('__'))
            uppercase_attr = dict((name.upper(), value)
                                  for name, value in attrs)

            return super(UpperAttrMetaclass, cls).__new__(cls, name, bases, uppercase_attr)

    class Foo(metaclass=UpperAttrMetaclass):
        # __metaclass__ = UpperAttrMetaclass
        bar = 'bip'

    # main
    print('attr bar:', hasattr(Foo, 'bar'))
    print('attr BAR:', hasattr(Foo, 'BAR'))
    print('BAR:', Foo.BAR)

    f = Foo()
    print('Foo class:', f.__class__)
    print('Foo super class:', f.__class__.__class__)  # UpperAttrMetaclass


# example 03, class: __new__, __init__, __call__
def py_class_ex03():

    class Foo(object):
        # create instance from cls
        def __new__(cls, *args, **kwargs):
            print('Foo __new__ is invoked: args=%s, kwargs=%s' % (args, kwargs))
            return super(Foo, cls).__new__(cls)

        # instance self created in __new__ and init
        def __init__(self, *args, **kwargs):
            print('Foo __init__ is invoked: args=%s, kwargs=%s' % (args, kwargs))
            self.value = args[0]

        def __call__(cls, *args, **kwargs):
            print('Foo __call__ is invoked: args=%s, kwargs=%s' % (args, kwargs))
            # super has no attr __call__
            # return super(Foo, cls).__call__(*args, **kwargs)

    # main
    f1 = Foo(1)
    print('f1 value:', f1.value)
    f1('instance1')
    print()
    f2 = Foo(2)
    print('f2 value:', f2.value)
    f2('instance2')


# example 04, metaclass and class: __new__, __init__, __call__
def py_class_ex04():
    # workflow:
    # 1) Metaclass.__new__ => Metaclass.__init__ => Metaclass, Foo
    # 2) Metaclass.__call__ => Foo.__new__ => Foo.__init__ => Metaclass.__call__ return => Foo, Foo object

    class Metaclass(type):
        def __new__(cls, *args, **kwargs):
            print('Metaclass __new__ is invoked, args:', args)
            name, bases, dct = args
            return super(Metaclass, cls).__new__(cls, name, bases, dct)

        def __init__(self, *args, **kwargs):
            print('Metaclass __init__ is invoked, args:', args)
            print('Metaclass __init__ self:', self)  # self = Foo

        def __call__(self, *args, **kwargs):
            print('Metaclass __call__ is invoked, args:', args)
            print('Metaclass __call__ self:', self)
            return super(Metaclass, self).__call__(*args, **kwargs)

    class Foo(metaclass=Metaclass):
        def __new__(cls, *args, **kwargs):
            print('Foo __new__ is invoked, args:', args)
            return super(Foo, cls).__new__(cls)

        def __init__(self, *args, **kwargs):
            print('Foo __init__ is invoked, args:', args)
            self.name = args[0]

    # main
    f1 = Foo('1')
    print()

    print(f1, [item for item in dir(f1) if not item.startswith('__')])
    f1_cls = f1.__class__  # f1_cls = type(f1)
    print(f1_cls, [item for item in dir(f1_cls) if not item.startswith('__')])
    f1_super_cls = f1.__class__.__class__
    print(f1_super_cls, [item for item in dir(
        f1_super_cls) if not item.startswith('__')])
    print()

    print('Foo attr name:', hasattr(Foo, 'name'))
    print('f1 attr name:', hasattr(f1, 'name'))
    print('name:', f1.name)


# example 05, __new__方法实现单例
def py_class_ex05():

    class Singleton(object):
        def __new__(cls, *args, **kwargs):
            print('Singleton __new__ is invoked: args=%s, kwargs=%s' %
                  (args, kwargs))
            if not hasattr(cls, '_instance'):
                cls._instance = super(Singleton, cls).__new__(cls)
            return cls._instance

        def __init__(self, *args, **kwargs):
            print('Singleton __init__ is invoked: args=%s, kwargs=%s' %
                  (args, kwargs))
            print('self attr _instance:', hasattr(self, '_instance'))
            self.name = args[0]

    # main
    s1 = Singleton('s1')
    print('s1 name:', s1.name)
    print()
    s2 = Singleton('s2')
    print('s2 name:', s2.name)
    print()
    print('s1 and s2 are same object:', s1 is s2)


# example 06, 元类实现单例
def py_class_ex06():

    class Singleton(type):
        def __init__(self, *args, **kwargs):
            print('meta Singleton __init__ is invoked: args=%s, kwargs=%s' %
                  (args, kwargs))
            self._instance = None

        def __call__(self, *args, **kwargs):
            print('meta Singleton __call__ is invoked: args=%s, kwargs=%s' %
                  (args, kwargs))
            if self._instance is None:
                self._instance = super(
                    Singleton, self).__call__(*args, **kwargs)
            return self._instance

    class Foo(metaclass=Singleton):
        def __init__(self, *args, **kwargs):
            print('Foo __init__ is invoked: args=%s, kwargs=%s' % (args, kwargs))
            self.name = args[0]

    # main
    foo1 = Foo('1')
    print('f1 name:', foo1.name)
    print()
    foo2 = Foo('2')
    print('f1 name:', foo2.name)
    print()

    print(Foo.__dict__)
    print('Foo instance:', Foo._instance, foo1, foo2)
    print('foo1 and foo2 are same object:', foo1 is foo2)


# example 07, private and final attrs in class
def py_class_ex07():

    class Foo(object):
        _cls_private = 'foo_class_private'
        __cls_final = 'foo_class_final'

        def __init__(self, *args, **kwargs):
            print('===> foo init')
            self.name = 'foo'
            self._inst_private = 'foo_instance_private'
            self.__inst_final = 'foo_instance_final'

        def get_name(self):
            return self.name

        def get_private_attrs(self):
            return 'cls_private=%s, ins_private=%s' % (self._cls_private, self._inst_private)

        def get_final_attrs(self):
            return 'cls_final=%s, ins_final=%s' % (self.__cls_final, self.__inst_final)

    class Bar(Foo):
        _cls_private = 'bar_class_private'
        __cls_final = 'bar_class_final'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            print('===> bar init')
            self.name = 'bar'
            self._inst_private = 'bar_instance_private'
            self.__inst_final = 'bar_instance_final'

    # main
    f = Foo()
    print('f class private attr:', f._cls_private)
    print('f instance private attr:', f._inst_private)
    print('f class final attr:', f._Foo__cls_final)
    print('f instance final attr:', f._Foo__inst_final)
    print()

    b = Bar()
    print(b.__dict__)
    print('name:', b.get_name())
    print('private attrs:', b.get_private_attrs())
    print('final attrs:', b.get_final_attrs())


# example 08, access global var in class
number = 10


def py_class_ex08():

    # not global access
    # number = 10

    class Foo(object):
        def add_number(self, n):
            global number
            number += n

        def print_number(self):
            global number
            print('number: %d' % number)

    # main
    f = Foo()
    f.print_number()
    f.add_number(1)
    f.print_number()


# example 09, abstract method
def py_class_ex09():
    from abc import ABCMeta, abstractmethod

    class DataProcessor(metaclass=ABCMeta):
        '''Base processor to be used for all preparation.'''

        def __init__(self, input_dir, output_dir):
            self.input_dir = input_dir
            self.output_dir = output_dir

        @abstractmethod
        def read(self):
            '''Read raw data.'''

        @abstractmethod
        def process(self):
            '''Processes raw data.'''

        @abstractmethod
        def save(self):
            '''Saves processed data.'''

    class MyProcess(DataProcessor):
        def __init__(self, input, output):
            super().__init__(input, output)

        def do(self):
            self.read()
            self.process()
            self.save()

        def read(self):
            print('read raw data from:', self.input_dir)

        def process(self):
            print('data process ...')

        def save(self):
            print('save output data:', self.output_dir)

    p = MyProcess('/tmp/input', '/tmp/output')
    p.do()


# example 10-01, invoke instance method by "getattr"
class MyObject(object):
    def echo(self, name):
        print("hello", name)

    def toString(self):
        return "my test object"


def py_class_ex1001():
    obj = MyObject()
    obj.echo("test1")

    getattr(MyObject, "echo")(MyObject, "test2")
    getattr(MyObject, "echo")(MyObject(), "test3")
    print(getattr(MyObject, "toString")(MyObject()))


# example 10-02 wrap class method
class MyMethod(object):
    def __init__(self, method_name, func):
        self.method_name = method_name
        self.func = func

    def __call__(self, *args, **kwargs):
        print("func:", self.method_name)
        print("wrap func:", self.func.__name__)
        return self.func(self.method_name, *args, **kwargs)

    def __getattr__(self, item):
        print(f"{self.method_name}.{item}")


class MyWrapObject(object):
    ''' 包装函数 '''

    def __init__(self, cls_object, cls_instance):
        self.cls_object = cls_object
        self.cls_instance = cls_instance

    def __getattr__(self, item):
        print("\nattr item:", item)
        return MyMethod(item, self._wrapFunc)

    def _wrapFunc(self, method_name, *args, **kwargs):
        print("aop before handler")
        print("invoke %s(%s)" % (method_name, args))
        ret = getattr(self.cls_object, method_name)(
            self.cls_instance, *args, **kwargs)
        print("aop after handler")
        return ret


def py_class_ex1002():
    wrap_obj = MyWrapObject(MyObject, MyObject())
    wrap_obj.echo("tester")
    print(wrap_obj.toString())


# example 10-03 wrap class method
class MyMethod2(object):
    def __init__(self, func, wrapFunc):
        self.func = func
        self.warpFunc = wrapFunc

    def __call__(self, *args, **kwargs):
        ret = self.warpFunc(self.func, *args, **kwargs)
        return ret


class MyWrapObject2(object):
    def __init__(self, cls_object, cls_instance):
        self.cls_object = cls_object
        self.cls_instance = cls_instance

    def __getattr__(self, item):
        f = getattr(self.cls_object, item)
        return MyMethod2(f, self._warpFunc)

    def _warpFunc(self, func, *args, **kwargs):
        print("aop before")
        ret = func(self.cls_instance, *args, **kwargs)
        print("aop after")
        return ret


def py_class_ex1003():
    wrap_obj = MyWrapObject2(MyObject, MyObject())
    wrap_obj.echo("tester")
    print(wrap_obj.toString())


# example 11
class EventHook(object):
    def __init__(self):
        self._handlers = []

    def add_listener(self, handler):
        self._handlers.append(handler)

    def remove_listener(self, handler):
        self._handlers.remove(handler)

    def fire(self, *args, **kwargs):
        for handler in self._handlers:
            handler(*args, **kwargs)


class Events(object):
    id = '1'
    on_start = EventHook
    on_stop = EventHook

    def __init__(self):
        self.id = '01'  # override
        for name, value in vars(type(self)).items():
            if value == EventHook:
                setattr(self, name, value())


def py_class_ex11():
    def start_handler():
        print('start handler')

    def stop_handler():
        print('stop handler')

    events = Events()
    print('event id:', events.id)
    events.on_start.add_listener(start_handler)
    events.on_stop.add_listener(stop_handler)

    events.on_start.fire()
    events.on_stop.fire()


# example 12, @property
class Student(object):

    @property
    def birth(self):
        return self._birth

    @birth.setter
    def birth(self, value):
        if 1982 < value < 2020:
            self._birth = value
        else:
            raise Exception('invalid birth value:', value)

    @property
    def age(self):
        return 2020 - self._birth


def py_class_ex12():
    s = Student()
    s.birth = 2014
    print('age:', s.age)


# example 13, 使用 metaclass MetaRoom 动态为类 Room 添加静态成员变量和函数
class Wall(object):

    STATIC_WALL_ATTR = "static wall"

    def init_wall(self):
        self.wall = "attr wall"

    def wall_info(self):
        print("this is wall of room")

    @staticmethod
    def static_wall_func():
        print("static wall info")


class Door(object):

    def init_door(self):
        self.door = "attr door"

    def door_info(self):
        print("this is door of room")
        print(self.door, self.wall, self.STATIC_WALL_ATTR, self.room)


class MetaRoom(type):

    meta_members = ('Wall', 'Door')
    exclude_funcs = ('__new__', '__init__')
    attr_types = (int, str, list, tuple, dict)

    def __init__(cls, name, bases, dic):
        import inspect
        import sys

        print('metaclass __init__, dict:')
        print(dic)
        super(MetaRoom, cls).__init__(name, bases, dic)

        for cls_name in MetaRoom.meta_members:
            cur_mod = sys.modules[__name__]  # 加载 module
            cls_def = getattr(cur_mod, cls_name)
            for func_name, func in inspect.getmembers(cls_def, inspect.isfunction):
                if func_name not in MetaRoom.exclude_funcs:
                    assert not hasattr(cls, func_name), func_name
                    print('add func:', func_name)
                    setattr(cls, func_name, func)

            for attr_name, value in inspect.getmembers(cls_def):
                if isinstance(value, MetaRoom.attr_types) and attr_name not in ('__module__', '__doc__'):
                    assert not hasattr(cls, attr_name), attr_name
                    print('add attr:', attr_name, value)
                    setattr(cls, attr_name, value)


class Room(object, metaclass=MetaRoom):

    def __init__(self):
        self.room = 'attr room'
        self.add_cls_member()

    def add_cls_member(self):
        """ 分别调用各个组合类中的init_cls_name的成员函数 """
        for cls_name in MetaRoom.meta_members:
            init_func_name = "init_%s" % cls_name.lower()
            init_func_imp = getattr(self, init_func_name, None)
            if init_func_imp:
                print('invoke init func imp:', init_func_name)
                init_func_imp()


def py_class_ex13():
    print('\nroom attrs:')
    print(vars(Room))
    # for attr_name in dir(Room):
    #     print(attr_name, type(getattr(Room, attr_name)))

    print('\ncreate room instance:')
    r = Room()
    r.door_info()


# example 14, getattr() and __getattr__
class Apple(object):

    def __init__(self):
        self._id = 1
        self._color = 'green'

    @property
    def id(self):
        return str(self._id)

    @property
    def color(self):
        return self._color

    def __getattr__(self, name):
        """ 当调用的属性不存在时，该方法会被调用 """
        return 'default'


def py_class_ex14():
    apple = Apple()
    print(f'\napple id={apple.id}, color={apple.color}')
    print(getattr(apple, 'name'))


# example 15, instance attributes inherit
class Root(object):

    def __init__(self, name):
        self.name = name


class Sub1(Root):

    desc = 'sub class without init'


class Sub2(Root):

    def __init__(self, desc):
        self.desc = desc


class Sub3(Root):

    def __init__(self, name, desc):
        super().__init__(name)
        self.desc = desc


def py_class_ex15():
    root = Root('root')
    print(vars(root))

    # 没有定义 __init__ 函数, 自动继承 root.name 属性
    sub1 = Sub1('sub1')
    print(vars(sub1))

    # 定义 __init__ 函数, 没有调用 super().__init__(), 没有继承 root.name 属性
    sub2 = Sub2('sub2')
    print(vars(sub2))

    # 定义 __init__ 函数, 显式调用 super.__init__(), 继承 root.name 属性
    sub3 = Sub3('sub3', 'define init with super init')
    print(vars(sub3))


# example 16, class attributes inherit
class TestCase(object):

    config: str
    steps: List[str]

    def perform(self):
        print(f'\nuse config: {self.config}')
        print('run steps:')
        for idx, step in enumerate(self.steps):
            print(f'{idx}. {step}')


class TestHomePage(TestCase):

    config = 'debug=true,level=debug'
    steps = [
        'open url',
        'input products'
        'click search',
    ]


def py_class_ex16():
    test = TestHomePage()
    test.perform()


if __name__ == '__main__':

    # py_base_ext()
    py_class_ex16()
    print('python class demo DONE.')
