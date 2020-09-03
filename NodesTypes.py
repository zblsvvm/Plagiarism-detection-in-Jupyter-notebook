import ast

"""
Record 9-dimensional characteristic vector and 35-dimensional characteristic vector required AST node type
"""


def return_nodes_array(num=9):
    ninety_seven_nodes_type = [

        ast.Constant, ast.Num, ast.Str, ast.FormattedValue, ast.JoinedStr, ast.Bytes, ast.List, ast.Tuple, ast.Set,
        ast.Dict, ast.Ellipsis, ast.NameConstant,

        ast.Name, ast.Load, ast.Store, ast.Del, ast.Starred,

        ast.Expr, ast.UnaryOp, ast.UAdd, ast.USub, ast.Not, ast.Invert, ast.BinOp, ast.Add, ast.Sub, ast.Mult,
        ast.Div, ast.FloorDiv, ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
        ast.MatMult, ast.BoolOp, ast.And, ast.Or, ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
        ast.Is, ast.IsNot, ast.In, ast.NotIn, ast.Call, ast.keyword, ast.IfExp, ast.Attribute,

        ast.Subscript, ast.Index, ast.Slice, ast.ExtSlice,

        ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp, ast.comprehension,

        ast.Assign, ast.AnnAssign, ast.AugAssign, ast.Raise, ast.Assert, ast.Delete, ast.Pass,

        ast.Import, ast.ImportFrom, ast.alias,

        ast.If, ast.For, ast.While, ast.Break, ast.Continue, ast.Try, ast.ExceptHandler, ast.With, ast.withitem,

        ast.FunctionDef, ast.Lambda, ast.arguments, ast.arg, ast.Return, ast.Yield, ast.YieldFrom, ast.Global,
        ast.Nonlocal, ast.ClassDef, ast.AsyncFunctionDef, ast.Await, ast.AsyncFor, ast.AsyncWith,

    ]

    fifty_six_nodes_type = [

        ast.Num, ast.Str, ast.List, ast.Tuple, ast.NameConstant,

        ast.Name, ast.Load, ast.Store,

        ast.Expr, ast.UnaryOp, ast.UAdd, ast.USub, ast.Not, ast.BinOp, ast.Add, ast.Sub, ast.Mult,

        ast.Div, ast.FloorDiv, ast.Mod, ast.Pow, ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE,

        ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn, ast.Call, ast.keyword, ast.Attribute,

        ast.Subscript, ast.Index, ast.Slice, ast.ExtSlice,

        ast.ListComp, ast.GeneratorExp, ast.comprehension,

        ast.Assign, ast.AugAssign, ast.Assert, ast.Pass,

        ast.ImportFrom, ast.alias,

        ast.If, ast.For, ast.While, ast.Break,

        ast.FunctionDef, ast.arguments, ast.arg, ast.Return
    ]

    nine_nodes_type = [

        [ast.Constant, ast.Num, ast.Str, ast.FormattedValue, ast.JoinedStr, ast.Bytes, ast.List, ast.Tuple, ast.Set,
         ast.Dict, ast.Ellipsis, ast.NameConstant],

        [ast.Name, ast.Load, ast.Store, ast.Del, ast.Starred],

        [ast.Expr, ast.UnaryOp, ast.UAdd, ast.USub, ast.Not, ast.Invert, ast.BinOp, ast.Add, ast.Sub, ast.Mult,
         ast.Div, ast.FloorDiv, ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
         ast.MatMult, ast.BoolOp, ast.And, ast.Or, ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
         ast.Is, ast.IsNot, ast.In, ast.NotIn, ast.Call, ast.keyword, ast.IfExp, ast.Attribute],

        [ast.Subscript, ast.Index, ast.Slice, ast.ExtSlice],

        [ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp, ast.comprehension],

        [ast.Assign, ast.AnnAssign, ast.AugAssign, ast.Raise, ast.Assert, ast.Delete, ast.Pass],

        [ast.Import, ast.ImportFrom, ast.alias],

        [ast.If, ast.For, ast.While, ast.Break, ast.Continue, ast.Try, ast.ExceptHandler, ast.With, ast.withitem],

        [ast.FunctionDef, ast.Lambda, ast.arguments, ast.arg, ast.Return, ast.Yield, ast.YieldFrom, ast.Global,
         ast.Nonlocal, ast.ClassDef, ast.AsyncFunctionDef, ast.Await, ast.AsyncFor, ast.AsyncWith],

    ]

    thirty_five_nodes_type = [

        ast.Num, ast.Str, ast.List, ast.Tuple, ast.NameConstant,

        ast.Name, ast.Load, ast.Store,

        ast.Expr, ast.UnaryOp, [ast.UAdd, ast.USub, ast.Not], ast.BinOp, ast.Add, ast.Sub, ast.Mult,

        [ast.Div, ast.FloorDiv, ast.Mod, ast.Pow], ast.Compare, [ast.Eq, ast.NotEq, ast.Lt, ast.LtE,

                                                                 ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn],

        ast.Call, ast.keyword, ast.Attribute,

        ast.Subscript, ast.Index, ast.Slice, ast.ExtSlice,

        [ast.ListComp, ast.GeneratorExp, ast.comprehension],

        [ast.Assign, ast.AugAssign, ast.Assert, ast.Pass],

        [ast.ImportFrom, ast.alias],

        ast.If, ast.For, [ast.While, ast.Break],

        ast.FunctionDef, ast.arguments, ast.arg, ast.Return
    ]

    if num == 9:
        return nine_nodes_type
    elif num == 35:
        return thirty_five_nodes_type
    elif num == 97:
        return ninety_seven_nodes_type
    elif num == 56:
        return fifty_six_nodes_type
    else:
        print("this is no such nodes_type as %d,please enter number 9 or 35", num)
        return None
