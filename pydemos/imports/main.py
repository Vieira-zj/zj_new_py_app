from . import func
from ..py_demo_base import py_base_ex02


def run():
    """
    use relative import ".module" and "..module"

    it's ok when invoked from [project-root]/main.py.
    raise error "attempted relative import beyond top-level package" when invoked from pydemos/py_demo_base.py.
    """
    print(func.add(1, 2))
    print(func.div(4, 2))
    print()
    py_base_ex02()
