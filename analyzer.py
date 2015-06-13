#TODO: function named pineapple for Alex
class ReturnValue:
    val = None
    def __init__(self, v):
        self.val = v

global_scope = {}
local_scopes = [{}]

def new_scope():
    local_scopes.append({})

def exit_scope():
    local_scopes.pop()

def get_val(key):
    if isinstance(key, (int, long, float)): 
        assert False, "isinstance still needed pls fix"
        return key
    """
    for scope in reversed(local_scopes):
        if key in scope:
            return scope[key]
    """
    if key in local_scopes[-1]:
        return local_scopes[-1][key]
    if key in global_scope:
        return global_scope[key]
    raise KeyError("%s not in scope" % key)

def assign(key, val):
    if key in local_scopes[-1]:
        local_scopes[-1][key] = val
        return
    if key in global_scope:
        global_scope[key] = val
        return
    if len(local_scopes) == 1:
        global_scope[key] = val
    else:
        local_scopes[-1][key] = val

def PreInc(x):
    newval = get_val(x) + 1
    assign(x, newval)
    return newval

def PreDec(x):
    newval = get_val(x) - 1
    assign(x, newval)
    return newval

def execute(ast):
    #print "AST:", ast
    if not isinstance(ast, tuple):
        return ast
    if ast[0] == 'Statements':
        execute(ast[1])
        return execute(ast[2])
    if ast[0] == 'Statement':
        return execute(ast[1])
    if ast[0] == 'Add':
        return execute(ast[1]) + execute(ast[2])
    if ast[0] == 'Subtract':
        return execute(ast[1]) - execute(ast[2])
    if ast[0] == 'Multiply':
        return execute(ast[1]) * execute(ast[2])
    if ast[0] == 'Divide':
        return execute(ast[1]) / execute(ast[2])
    if ast[0] == 'Modulus':
        return execute(ast[1]) % execute(ast[2])
    if ast[0] == 'PreInc':
        return PreInc(execute(ast[1]))
    if ast[0] == 'PreDec':
        return PreDec(execute(ast[1]))
    if ast[0] == 'NumToExpr':
        return execute(ast[1])
    if ast[0] == 'BoolToExpr':
        if ast[1] == 'true': return True
        if ast[1] == 'false': return False
        assert False, "bool neither true not false"
    if ast[0] == 'StrToExpr':
        return ast[1]
    if ast[0] == 'IDToExpr':
        return get_val(execute(ast[1]))
    if ast[0] == 'And':
        return execute(ast[1]) and execute(ast[2])
    if ast[0] == 'Or':
        return execute(ast[1]) or execute(ast[2])
    if ast[0] == 'Xor':
        return bool(execute(ast[1])) != bool(execute(ast[2]))
    if ast[0] == 'Not':
        return not bool(execute(ast[1]))
    if ast[0] == 'List':
        return execute(ast[1])
    if ast[0] == 'ListItems':
        return [execute(ast[1]), execute(ast[2])]
    if ast[0] == 'ListItem':
        return [execute(ast[1])]
    if ast[0] == 'NullListItem':
        return []
    if ast[0] == 'Assign':
        val = execute(ast[2])
        assign(ast[1], val)
        return val
    if ast[0] == 'Print':
        print execute(ast[1])
        return
    if ast[0] == 'If':
        ret = None
        if execute(ast[1]):
            ret = execute(ast[2])
        return ret
    if ast[0] == 'IfElse':
        ret = None
        if execute(ast[1]):
            ret = execute(ast[2])
        else:
            ret = execute(ast[3])
        return ret
    if ast[0] == 'While':
        while execute(ast[1]):
            execute(ast[2])
        return
    if ast[0] == 'For':
        execute(ast[1])
        while execute(ast[2]):
            execute(ast[4])
            execute(ast[3])
        return
    if ast[0] == 'FuncParams':
        return [ast[1], ast[2]]
    if ast[0] == 'FuncParam':
        return [ast[1]]
    if ast[0] == 'NullFuncParam':
        return []
    if ast[0] == 'Function':
        assign(ast[1], (execute(ast[2]), ast[3]))
        return
    if ast[0] == 'FunctionCall':
        new_scope()
        params, code = get_val(ast[1])
        args = execute(ast[2])
        #TODO: nicer error check.
        assert len(params) == len(args), "func params/args length conflict."
        for param, arg in zip(params, args):
            assign(param, arg)
        ret = None
        #sorry but i cant think of a less-ugly better way.
        try:
            execute(code)
        except ReturnValue as r:
            ret = r.val
        exit_scope()
        return ret
    if ast[0] == 'Return':
        raise ReturnValue(execute(ast[1]))
    if ast[0]=='EQ': return execute(ast[1]) == execute(ast[2])
    if ast[0]=='NE': return execute(ast[1]) != execute(ast[2])
    if ast[0]=='GT': return execute(ast[1]) >  execute(ast[2])
    if ast[0]=='GE': return execute(ast[1]) >= execute(ast[2])
    if ast[0]=='LT': return execute(ast[1]) <  execute(ast[2])
    if ast[0]=='LE': return execute(ast[1]) <= execute(ast[2])
    print "Unexpected node:", ast
