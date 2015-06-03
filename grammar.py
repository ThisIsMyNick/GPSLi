from __future__ import division

import tokenrules
tokens = tokenrules.tokens

#lower -> greater precedence
precedence = (
        #(associativity, tokens...)
        ('left', 'SEMICOLON'),
        ('nonassoc', 'PRINT'),
        ('left', 'PLUS', 'DASH'),
        ('left', 'STAR', 'SLASH'),
)

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

def p_expression(p):
    '''expression : INT
                  | FLOAT'''
    p[0] = p[1]

def p_print(p):
    '''expression : PRINT expression'''
    print p[2]
    p[0] = p[2]

def p_error(p):
    if p:
        print "Syntax error at '%s' in line %d" % (p.value, p.lineno)
