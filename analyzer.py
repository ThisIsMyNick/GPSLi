scopes = [{}]

def get_val(key):
    if isinstance(key, int) or isinstance(key, float): return key
    for scope in reversed(scopes):
        if key in scope:
            return scope[key]
    raise KeyError("%s not in scope" % key)

def assign(key, val):
    for index, scope in enumerate(reversed(scopes)):
        if key in scope:
            scopes[len(scopes)-index-1][key] = val
            return
    scopes[-1][key] = val

def PreInc(x):
    newval = get_val(x) + 1
    assign(x, newval)
    return newval

def PreDec(x):
    newval = get_val(x) - 1
    assign(x, newval)
    return newval

def execute(ast):
    #print ast
    if type(ast) != type(()):
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
    if ast[0] == 'PreInc':
        return PreInc(execute(ast[1]))
    if ast[0] == 'PreDec':
        return PreDec(execute(ast[1]))
    if ast[0] == 'NumToExpr':
        return execute(ast[1])
    if ast[0] == 'IDToExpr':
        return get_val(execute(ast[1]))
    if ast[0] == 'Assign':
        val = execute(ast[2])
        assign(ast[1], val)
        return val
    if ast[0] == 'Print':
        print execute(ast[1])
        return
    if ast[0] == 'If':
        if execute(ast[1]) == True: #disallow implicit crap.
            return execute(ast[2])
        return
    if ast[0] == 'IfElse':
        if execute(ast[1]) == True:
            return execute(ast[2])
        else:
            return execute(ast[3])
    if ast[0]=='EQ': return get_val(execute(ast[1])) == get_val(execute(ast[2]))
    if ast[0]=='NE': return get_val(execute(ast[1])) != get_val(execute(ast[2]))
    if ast[0]=='GT': return get_val(execute(ast[1])) >  get_val(execute(ast[2]))
    if ast[0]=='GE': return get_val(execute(ast[1])) >= get_val(execute(ast[2]))
    if ast[0]=='LT': return get_val(execute(ast[1])) <  get_val(execute(ast[2]))
    if ast[0]=='LE': return get_val(execute(ast[1])) <= get_val(execute(ast[2]))
    print "Unexpected node:", ast
