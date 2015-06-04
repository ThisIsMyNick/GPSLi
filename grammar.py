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

#later in tuple -> greater precedence
precedence = (
        #(associativity, tokens...)
        ('left', 'SEMICOLON'),
        ('nonassoc', 'PRINT'),
        ('right', 'ASSIGN'),
        ('left', 'PLUS', 'DASH'),
        ('left', 'STAR', 'SLASH'),
)

#TODO: better way to separate statements
def p_semicolon(p):
    '''expression : expression SEMICOLON expression'''
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
    scopes[-1][p[1]] = p[3]
    p[0] = p[3]

def p_print(p):
    '''expression : PRINT expression'''
    print p[2]
    p[0] = p[2]

def p_error(p):
    if p:
        print "Syntax error at '%s' in line %d" % (p.value, p.lineno)
