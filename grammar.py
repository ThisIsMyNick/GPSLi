from __future__ import division

import tokenrules
tokens = tokenrules.tokens

#later in tuple -> greater precedence
precedence = (
        #(associativity, tokens...)
        ('left', 'SEMICOLON'),
        ('nonassoc', 'PRINT', 'RETURN',),
        ('right', 'ASSIGN'),
        ('left', 'AND', 'OR', 'XOR'),
        ('left', 'EQUAL', 'NEQUAL', 'GT', 'GE', 'LT', 'LE'),
        ('right', 'NOT'),
        ('left', 'PLUS', 'DASH'),
        ('left', 'STAR', 'SLASH', 'MOD'),
        ('right', 'UPLUS', 'UMINUS'),
        ('right', 'LBRACKET', 'RBRACKET'),
)

#TODO: better way to separate statements? or nah
def p_expr_semi(p):
    '''statement : expression SEMICOLON'''
    p[0] = ('Statement', p[1])

def p_state_state(p):
    '''statement : statement statement''' #lhs is statement so it can recurse
    p[0] = ('Statements', p[1], p[2])

def p_expr_parens(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

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

def p_binop_bool(p):
    '''expression : expression AND expression
                  | expression OR expression
                  | expression XOR expression'''
    if   p[2] == '&&': p[0] = ('And', p[1], p[3])
    elif p[2] == '||': p[0] = ('Or',  p[1], p[3])
    elif p[2] == '^' : p[0] = ('Xor', p[1], p[3])

def p_unop_bool(p):
    '''expression : NOT expression'''
    if p[1] == '!': p[0] = ('Not', p[2])

def p_unop_sign(p):
    '''expression : PLUS expression %prec UPLUS
                  | DASH expression %prec UMINUS'''
    if   p[1] == '+': p[0] = ('UPlus',  p[2])
    elif p[1] == '-': p[0] = ('UMinus', p[2])

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
    '''list-items : expression COMMA list-items'''
    p[0] = ('ListItems', p[1], p[3])

def p_listitem(p):
    '''list-items : expression'''
    p[0] = ('ListItem', p[1])

def p_listitems_null(p):
    '''list-items : '''
    p[0] = ('NullListItem',)

def p_expr_listindex(p):
    '''expression : expression LBRACKET expression RBRACKET'''
    p[0] = ('ListIndex', p[1], p[3])

### Functions

def p_funcparams(p):
    '''func-params : ID COMMA func-params'''
    p[0] = ('FuncParams', p[1], p[3])

def p_funcparam(p):
    '''func-params : ID'''
    p[0] = ('FuncParam', p[1])

def p_funcparam_null(p):
    '''func-params :'''
    p[0] = ('NullFuncParam',)

def p_funcargs(p):
    '''func-args : list-items'''
    p[0] = ('Args', p[1])

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

def p_expr_num(p):
    '''expression : INT
                  | FLOAT'''
    p[0] = ('NumToExpr', p[1])

def p_expr_bool(p):
    '''expression : TRUE
                  | FALSE'''
    p[0] = ('BoolToExpr', p[1])

def p_expr_str(p):
    'expression : STRING'
    p[0] = ('StrToExpr', p[1])

### ID

def p_expr_id(p):
    '''expression : ID'''
    p[0] = ('IDToExpr', p[1])

def p_expr_assign(p):
    '''expression : ID ASSIGN expression'''
    p[0] = ('Assign', p[1], p[3])

# Modules

def p_expr_include(p):
    'expression : INCLUDE STRING'
    p[0] = ('Include', p[2])

#General

def p_print(p):
    '''expression : PRINT expression'''
    p[0] = ('Print', p[2])

def p_error(p):
    if p:
        #TODO: does this line # thing work?
        # apparently not
        print "Syntax error at '%s' in line %d" % (p.value, p.lineno)
