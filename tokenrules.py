
reserved = {
        'print' : 'PRINT',
}

tokens = (
        'PLUS',
        'DASH',
        'STAR',
        'SLASH',
        'FLOAT',
        'INT',
        'PRINT',
        'SEMICOLON',
)

t_PLUS = r'\+'
t_DASH = r'-'
t_STAR = r'\*'
t_SLASH = r'/'
t_PRINT = r'print' #TODO: Use a dict of reserved keywords
t_SEMICOLON = r';'

def t_FLOAT(t):
    r'\d+\.\d*'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ANY_ignore = ' \n\t\f\v'

def t_error(t):
    print "Unrecognized character '%s'at line %d" % (t.value[0], t.lineno)
    t.lexer.skip(1)
