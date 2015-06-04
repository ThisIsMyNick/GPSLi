from __future__ import division

import tokenrules
tokens = tokenrules.tokens

'''
scopes will be represented by a list
last element in list is the current scope
each scope is a dictionary
'''
scopes = [{}] #TODO: Set initial scope at entrypoint, not here.

def get_val(key):
    for scope in reversed(scopes):
        if key in scope:
            return scope[key]
    raise KeyError("%s not in scope" % key)

def assign(key, val):
    new_var = True
    for index,scope in enumerate(reversed(scopes)):
        if key in scope:
            scopes[len(scopes)-index-1][key] = val
            new_var = False
            break
    if new_var:
        scopes[-1][key] = val

#later in tuple -> greater precedence
precedence = (
        #(associativity, tokens...)
        ('left', 'SEMICOLON'),
        ('nonassoc', 'PRINT'),
        ('right', 'ASSIGN'),
        ('left', 'PLUS', 'DASH'),
        ('left', 'STAR', 'SLASH'),
)

#TODO: better way to separate statements? or nah
def p_semicolon(p):
    '''expression : expression SEMICOLON expression
                  | expression SEMICOLON'''
    pass

def p_binop_arithmetic(p):
    '''expression : expression PLUS expression
                  | expression DASH expression
                  | expression STAR expression
                  | expression SLASH expression'''
    if   p[2] == '+': p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]

### Pre/Post Inc/Dec

def p_preinc(p):
    '''expression : PLUS PLUS ID'''
    oldval = get_val(p[3])
    assign(p[3], oldval + 1)
    p[0] = oldval + 1

def p_predec(p):
    '''expression : DASH DASH ID'''
    oldval = get_val(p[3])
    assign(p[3], oldval - 1)
    p[0] = oldval - 1

"""
#these dont work, idk why. parser errors out.
def p_postinc(p):
    '''expression : ID PLUS PLUS'''
    oldval = get_val(p[1])
    assign(p[1], oldval + 1)
    p[0] = oldval

def p_postdec(p):
    '''expression : ID DASH DASH'''
    oldval = get_val(p[1])
    assign(p[1], oldval - 1)
    p[0] = oldval
"""

### Literals

def p_expression(p):
    '''expression : INT
                  | FLOAT'''
    p[0] = p[1]

### ID

def p_expr_id(p):
    '''expression : ID'''
    p[0] = get_val(p[1])

def p_expr_assign(p):
    '''expression : ID ASSIGN expression'''
    assign(p[1], p[3])
    p[0] = p[3]

def p_print(p):
    '''expression : PRINT expression'''
    print p[2]
    p[0] = p[2]

def p_error(p):
    if p:
        #TODO: does this line # thing work?
        print "Syntax error at '%s' in line %d" % (p.value, p.lineno)
