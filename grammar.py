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
def p_expr_semi(p):
    '''statement : expression SEMICOLON'''
    p[0] = ('Statement', p[1])

def p_state_state(p):
    '''statement : statement statement''' #lhs is statement so it can recurse
    p[0] = ('Statements', p[1], p[2])

def p_binop_arithmetic(p):
    '''expression : expression PLUS expression
                  | expression DASH expression
                  | expression STAR expression
                  | expression SLASH expression'''
    if   p[2] == '+': p[0] = ('Add',        p[1], p[3])
    elif p[2] == '-': p[0] = ('Subtract',   p[1], p[3])
    elif p[2] == '*': p[0] = ('Multiply',   p[1], p[3])
    elif p[2] == '/': p[0] = ('Divide',     p[1],  p[3])

def p_compare(p):
    '''expression : expression EQUAL expression
                  | expression NEQUAL expression
                  | expression GT expression
                  | expression GE expression
                  | expression LT expression
                  | expression LE expression'''
    if   p[2] == '==': p[0] = ('EQ', p[1], p[3])
    elif p[2] == '!=': p[0] = ('NE', p[1], p[3])
    elif p[2] == '>':  p[0] = ('GT', p[1], p[3])
    elif p[2] == '>=': p[0] = ('GE', p[1], p[3])
    elif p[2] == '>':  p[0] = ('LT', p[1], p[3])
    elif p[2] == '<=': p[0] = ('LE', p[1], p[3])

def p_state_if(p):
    '''statement : IF LPAREN expression RPAREN LBRACE statement RBRACE'''
    p[0] = ('If', p[3], p[6])

def p_state_ifelse(p):
    '''statement : IF LPAREN expression RPAREN LBRACE statement RBRACE ELSE LBRACE statement RBRACE'''
    p[0] = ('IfElse', p[3], p[6], p[10])

### Pre/Post Inc/Dec

def p_preinc(p):
    '''expression : PLUS PLUS ID'''
    p[0] = ('PreInc', p[3])

def p_predec(p):
    '''expression : DASH DASH ID'''
    p[0] = ('PreDec', p[3])

### Literals

def p_expression(p):
    '''expression : INT
                  | FLOAT'''
    p[0] = ('NumToExpr', p[1])

### ID

def p_expr_id(p):
    '''expression : ID'''
    p[0] = ('IDToExpr', p[1])

def p_expr_assign(p):
    '''expression : ID ASSIGN expression'''
    p[0] = ('Assign', p[1], p[3])

def p_print(p):
    '''expression : PRINT expression'''
    p[0] = ('Print', p[2])

def p_error(p):
    if p:
        #TODO: does this line # thing work?
        print "Syntax error at '%s' in line %d" % (p.value, p.lineno)
