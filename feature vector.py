import sys
import ast
import difflib
import operator
import argparse
import itertools
from collections import Counter
import types
import astunparse
from collections import deque
import numpy as np
import extract


class Operation(ast.NodeTransformer):
    def __init__(self):
        self.nodes_type = np.array([

            [ast.Constant, ast.Num, ast.Str, ast.FormattedValue, ast.JoinedStr, ast.Bytes, ast.List, ast.Tuple, ast.Set,
             ast.Dict, ast.Ellipsis, ast.NameConstant],

            [ast.Name, ast.Load, ast.Store, ast.Del, ast.Starred],

            [ast.Expr, ast.UnaryOp, ast.UAdd, ast.USub, ast.Not, ast.Invert, ast.BinOp, ast.Add, ast.Sub, ast.Mult,
             ast.Div, ast.FloorDiv, ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
             ast.MatMult, ast.BoolOp, ast.And, ast.Or, ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
             ast.Is, ast.IsNot,ast.In, ast.NotIn, ast.Call, ast.keyword, ast.IfExp, ast.Attribute],

            [ast.Subscript, ast.Index, ast.Slice, ast.ExtSlice],

            [ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp, ast.comprehension],

            [ast.Assign, ast.AnnAssign, ast.AugAssign, ast.Raise, ast.Assert, ast.Delete, ast.Pass],

            [ast.If, ast.For, ast.While, ast.Break, ast.Continue, ast.Try, ast.ExceptHandler, ast.With, ast.withitem],

            [ast.FunctionDef, ast.Lambda, ast.arguments, ast.arg, ast.Return, ast.Yield, ast.YieldFrom, ast.Global,
             ast.Nonlocal, ast.ClassDef, ast.AsyncFunctionDef, ast.Await, ast.AsyncFor, ast.AsyncWith],

        ], dtype=object)

    def generic_visit(self, node):
        # you are allowed to add arbitrary fields to python objects
        node.vector = np.zeros(8)
        ast.NodeTransformer.generic_visit(self, node)
        for general_type_index, one_general_type in enumerate(self.nodes_type):
            if type(node) in one_general_type:
                node.vector[general_type_index] += 1
        for a in ast.iter_child_nodes(node):
            # this node will be sum of all children nodes
            # as well as case logic below.
            node.vector += a.vector
        # print("{} {} {}".format("node.vector:", type(node).__name__, node.vector))
        return node

    def general_transform_to_vector(self, path, question_num):
        all_ast_vector = {}
        ast_vector = {}
        all_code = extract.exact_every_students_code(path, question_num)
        for student_key in all_code:
            single_student_code = all_code[student_key]
            for question_key in single_student_code:
                node = ast.parse(single_student_code[question_key])
                vector = self.generic_visit(node).vector
                ast_vector[question_key + "_vector"] = vector
            if __name__ == "__main__":
                print(ast_vector)
            all_ast_vector[student_key + " vector"] = ast_vector
        return all_ast_vector


if __name__ == "__main__":
    path = "testdata/Assignment 1/Assignment 1/last"
    k = Operation()
    print(k.general_transform_to_vector(path, 4))

