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
        ('left', 'STAR', 'SLASH', 'MOD'),
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
                  | expression SLASH expression
                  | expression MOD expression'''
    if   p[2] == '+': p[0] = ('Add',        p[1], p[3])
    elif p[2] == '-': p[0] = ('Subtract',   p[1], p[3])
    elif p[2] == '*': p[0] = ('Multiply',   p[1], p[3])
    elif p[2] == '/': p[0] = ('Divide',     p[1], p[3])
    elif p[2] == '%': p[0] = ('Modulus',    p[1], p[3])

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
    elif p[2] == '<':  p[0] = ('LT', p[1], p[3])
    elif p[2] == '<=': p[0] = ('LE', p[1], p[3])

### Conditional

def p_state_if(p):
    '''statement : IF LPAREN expression RPAREN LBRACE statement RBRACE'''
    p[0] = ('If', p[3], p[6])


def p_state_ifelse(p):
    '''statement : IF LPAREN expression RPAREN LBRACE statement RBRACE ELSE LBRACE statement RBRACE'''
    p[0] = ('IfElse', p[3], p[6], p[10])

### Loop

def p_state_while(p):
    '''statement : WHILE LPAREN expression RPAREN LBRACE statement RBRACE'''
    p[0] = ('While', p[3], p[6])

def p_state_for(p):
    '''statement : FOR LPAREN expression SEMICOLON expression SEMICOLON expression RPAREN LBRACE statement RBRACE'''
    p[0] = ('For', p[3], p[5], p[7], p[10])

### Lists

def p_expr_list(p):
    '''expression : LBRACKET list-items RBRACKET'''
    p[0] = ('List', p[2])

def p_listitems(p):
    '''list-items : expression COMMA expression'''
    p[0] = ('ListItems', p[1], p[3])

def p_listitem(p):
    '''list-items : expression'''
    p[0] = ('ListItem', p[1])

def p_listitems_null(p):
    '''list-items : '''
    p[0] = ('NullListItem',)

### Functions

def p_funcparams(p):
    '''func-params : ID COMMA ID'''
    p[0] = ('FuncParams', p[1], p[3])

def p_funcparam(p):
    '''func-params : ID'''
    p[0] = ('FuncParam', p[1])

def p_funcparam_null(p):
    '''func-params :'''
    p[0] = ('NullFuncParam',)

def p_funcargs(p):
    '''func-args : list-items'''
    p[0] = p[1]

def p_state_funcdef(p):
    '''statement : FUNC ID LPAREN func-params RPAREN LBRACE statement RBRACE'''
    p[0] = ('Function', p[2], p[4], p[7])

def p_expr_funccall(p):
    '''expression : ID LPAREN func-args RPAREN'''
    p[0] = ('FunctionCall', p[1], p[3])

def p_expr_return(p):
    '''expression : RETURN expression'''
    p[0] = ('Return', p[2])

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
