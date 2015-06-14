from os import path
import shared
import builtins

#TODO: function named pineapple for Alex
class ReturnValue:
    val = None
    def __init__(self, v):
        self.val = v

global_scope = {}
local_scopes = [{}]
module_scope = {}

def new_scope():
    local_scopes.append({})

def exit_scope():
    local_scopes.pop()

def get_val(key, module=None):
    if "." in key:
        key, module = get_id_mod(key)
    if module:
        if key in module_scope[module]:
            return module_scope[module][key]
        raise KeyError("%s not in %s module scope" % (key, module))
    if key in local_scopes[-1]:
        return local_scopes[-1][key]
    if key in global_scope:
        return global_scope[key]
    raise KeyError("%s not in scope" % key)

def assign(key, val, module=None):
    if "." in key:
        key, module = get_id_mod(key)
    if module:
        if module not in module_scope:
            module_scope[module] = {}
        module_scope[module][key] = val
        return
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

def include(lib):
    libg = lib + ".lgpsl"
    f = None
    try:
        f = open(path.join(path.dirname(shared.filename), libg))
    except IOError:
        try:
            f = open(path.join(path.dirname(path.realpath(__file__)), "stdlib", libg))
        except IOError as e:
            print "[ERROR]: No file named %s." % libg
            raise e
    ast = shared.parser.parse(f.read())
    execute(ast, lib)

def FunctionCall(funcname, args, module=None):
    if funcname in builtins.functions:
        return builtins.functions[funcname](*execute(args))
    params, code = get_val(funcname, module)
    args = execute(args)
    new_scope()
    #TODO: nicer error check.
    assert len(params) == len(args), "Param/arg length conflict."
    for param, arg in zip(params, args):
        assign(param, arg, module)
    ret = None
    try:
        execute(code, module)
    except ReturnValue as r:
        ret = r.val
    exit_scope()
    return ret

def get_module(ID):
    if "." in ID:
        return ID.split(".")[0]
    return None

def get_id(ID):
    if "." in ID:
        return ID.split(".")[1]
    return ID

def get_id_mod(ID):
    return (get_id(ID), get_module(ID))

def flatten(L):
    if len(L) < 2: return L
    return [L[0]] + flatten(L[1])

def PreInc(x, module):
    newval = get_val(x, module) + 1
    assign(x, newval, module)
    return newval

def PreDec(x, module):
    newval = get_val(x, module) - 1
    assign(x, newval, module)
    return newval

def execute(ast, module=None):
    #print "AST:", ast
    if not isinstance(ast, tuple):
        return ast
    if ast[0] == 'Statements':
        execute(ast[1], module)
        return execute(ast[2], module)
    if ast[0] == 'Statement':
        return execute(ast[1], module)
    if ast[0] == 'Add':
        return execute(ast[1], module) + execute(ast[2], module)
    if ast[0] == 'Subtract':
        return execute(ast[1], module) - execute(ast[2], module)
    if ast[0] == 'Multiply':
        return execute(ast[1], module) * execute(ast[2], module)
    if ast[0] == 'Divide':
        return execute(ast[1], module) / execute(ast[2], module)
    if ast[0] == 'Modulus':
        return execute(ast[1], module) % execute(ast[2], module)
    if ast[0] == 'PreInc':
        return PreInc(*get_id_mod(execute(ast[1], module)))
    if ast[0] == 'PreDec':
        return PreDec(*get_id_mod(execute(ast[1], module)))
    if ast[0] == 'UPlus':
        return execute(ast[1], module)
    if ast[0] == 'UMinus':
        return -execute(ast[1], module)
    if ast[0] == 'NumToExpr':
        return execute(ast[1], module)
    if ast[0] == 'BoolToExpr':
        if ast[1] == 'true': return True
        if ast[1] == 'false': return False
    if ast[0] == 'StrToExpr':
        return ast[1]
    if ast[0] == 'IDToExpr':
        return get_val(ast[1])
    if ast[0] == 'And':
        return execute(ast[1], module) and execute(ast[2], module)
    if ast[0] == 'Or':
        return execute(ast[1], module) or execute(ast[2], module)
    if ast[0] == 'Xor':
        return bool(execute(ast[1], module)) != bool(execute(ast[2], module))
    if ast[0] == 'Not':
        return not bool(execute(ast[1], module))
    if ast[0] == 'List':
        return flatten(execute(ast[1], module))
    if ast[0] == 'ListItems':
        return [execute(ast[1], module), execute(ast[2], module)]
    if ast[0] == 'ListItem':
        return [execute(ast[1], module)]
    if ast[0] == 'NullListItem':
        return []
    if ast[0] == 'ListIndex':
        return execute(ast[1])[execute(ast[2])]
    if ast[0] == 'Assign':
        val = execute(ast[2], module)
        assign(ast[1], val, module)
        return val
    if ast[0] == 'Include':
        include(ast[1])
        return
    if ast[0] == 'Print':
        print execute(ast[1], module)
        return
    if ast[0] == 'If':
        ret = None
        if execute(ast[1], module):
            ret = execute(ast[2], module)
        return ret
    if ast[0] == 'IfElse':
        ret = None
        if execute(ast[1], module):
            ret = execute(ast[2], module)
        else:
            ret = execute(ast[3], module)
        return ret
    if ast[0] == 'While':
        while execute(ast[1], module):
            execute(ast[2], module)
        return
    if ast[0] == 'For':
        execute(ast[1], module)
        while execute(ast[2], module):
            execute(ast[4], module)
            execute(ast[3], module)
        return
    if ast[0] == 'FuncParams':
        return [execute(ast[1]), execute(ast[2])]
    if ast[0] == 'FuncParam':
        return [ast[1]]
    if ast[0] == 'NullFuncParam':
        return []
    if ast[0] == 'Function':
        assign(ast[1], (flatten(execute(ast[2], module)), ast[3]), module)
        return
    if ast[0] == 'FunctionCall':
        return FunctionCall(ast[1], ast[2], module)
    if ast[0] == 'Args':
        return flatten(execute(ast[1]))
    if ast[0] == 'Return':
        raise ReturnValue(execute(ast[1], module))
    if ast[0]=='EQ': return execute(ast[1], module) == execute(ast[2], module)
    if ast[0]=='NE': return execute(ast[1], module) != execute(ast[2], module)
    if ast[0]=='GT': return execute(ast[1], module) >  execute(ast[2], module)
    if ast[0]=='GE': return execute(ast[1], module) >= execute(ast[2], module)
    if ast[0]=='LT': return execute(ast[1], module) <  execute(ast[2], module)
    if ast[0]=='LE': return execute(ast[1], module) <= execute(ast[2], module)
    print "Unexpected node:", ast
