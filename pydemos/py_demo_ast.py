# coding=utf-8

import ast
import astunparse

"""
dep:
pip install astunparse
"""


def ast_demo01():
    code = """
var = 1
print(var)
"""
    head = ast.parse(code)
    print('ast dumps:', ast.dump(head))

    body = head.body
    print('var value:', body[0].value.n)

    body[0].value.n = 2
    print('\nchanged code:', astunparse.unparse(head))

#
# demo 代码替换
# 问题：会丢失了原始源代码的所有格式和注释。
#


def is_multi_index_rename_node(node):
    """
    Checks if the given node represents the code: <var>.levels[<idx>].name = <val>
    and returns the corresponding var, idx and val if it does.
    """
    try:
        if (
            isinstance(node, ast.Assign)
            and node.targets[0].attr == 'name'
            and node.targets[0].value.value.attr == 'levels'
        ):
            var = node.targets[0].value.value.value.id
            idx = node.targets[0].value.slice.value.n
            val = node.value
            return True, var, idx, val
    except:
        pass
    return False, None, None, None


def get_new_multi_index_rename_node(var, idx, val):
    """
    Returns AST node that represents the code: <var> = <var>.set_names(<val>, level=<idx>)
    for the given var, idx and val.
    """
    return ast.Assign(
        targets=[ast.Name(id=var)],
        value=ast.Call(
            func=ast.Attribute(value=ast.Name(id=var), attr='set_names'),
            args=[val],
            keywords=[ast.keyword(arg='level', value=ast.Num(n=idx))],
        ),
    )


def patch(node):
    # If it is a leaf node, then no patching needed.
    if not hasattr(node, '_fields'):
        return node

    for (name, field) in ast.iter_fields(node):
        if isinstance(field, list):
            for i in range(len(field)):
                ok, var, idx, val = is_multi_index_rename_node(field[i])
                if ok:
                    field[i] = get_new_multi_index_rename_node(var, idx, val)
                else:
                    patch(field[i])
        else:
            ok, var, idx, val = is_multi_index_rename_node(field)
            if ok:
                setattr(node, name, get_new_multi_index_rename_node(var, idx, val))
            else:
                patch(field)


def ast_demo02():
    code = """
import pandas as pd
mi = pd.MultiIndex.from_product([[1, 2], ['a', 'b']], names=['x', 'y'])
mi.levels[0].name = "new name"
"""
    head = ast.parse(code)
    patch(head)
    print(astunparse.unparse(head))


def ast_demo03():
    code = """
import pandas as pd
class C():
    def f():
        def g():
            mi.levels[
                0
            ].name = "new name"
mi = pd.MultiIndex.from_product([[1, 2], ['a', 'b']], names=['x', 'y'])
"""
    head = ast.parse(code)
    patch(head)
    print(astunparse.unparse(head))


#
# demo 代码检查
#

def var_name_check(node):
    """
    Takes an AST rooted at the given node and checks if there are single character
    variable names.
    """
    if not hasattr(node, '_fields'):
        return

    for child_node in ast.iter_child_nodes(node):
        if isinstance(child_node, ast.Name) and len(child_node.id) == 1:
            print(
                f"Single character name '{child_node.id}' used at line number {child_node.lineno}")
        var_name_check(child_node)


def ast_demo04():
    code = """
a = 1
b = a
print(b)
"""
    head = ast.parse(code)
    var_name_check(head)


def unlogged_except_check(node):
    """
    Takes an AST rooted at the given node and checks if there are un-logged except
    code blocks.
    """
    if not hasattr(node, '_fields'):
        return

    for child_node in ast.iter_child_nodes(node):
        if isinstance(child_node, ast.excepthandler) and not is_logging_present(child_node):
            print(
                f"Neither 'error' nor 'exception' logging is present within the except block starting at line number {child_node.lineno}")
        unlogged_except_check(child_node)


def is_logging_present(node):
    """
    Takes an AST rooted at the given node and checks whether there is an 'error'
    or 'exception' logging present in it.
    """
    if not hasattr(node, '_fields'):
        return False

    # If it represents an "error" or "exception" function call.
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in ['error', 'exception']
    ):
        return True

    for child_node in ast.iter_child_nodes(node):
        if is_logging_present(child_node):
            return True
    return False


def ast_demo05():
    code = """
try:
    pass
except ValueError:
    logging.error("Error occurred")
    try:
        pass
    except KeyError:
        logging.exception("Exception handled")
    except NameError:
        pass
try:
    pass
except:
    logging.info("Info level logging")
"""
    head = ast.parse(code)
    unlogged_except_check(head)


if __name__ == '__main__':

    ast_demo05()
    print('ast demo done.')
