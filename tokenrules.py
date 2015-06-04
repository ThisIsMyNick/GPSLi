#TODO: rename token names to be less generic. eg, MINUS rather than DASH.

reserved = {
        'print' : 'PRINT',
}

tokens = (
        'PLUS',
        'DASH',
        'STAR',
        'SLASH',
        'ASSIGN',
        'ID',
        'FLOAT',
        'INT',
        'PRINT',
        'SEMICOLON',
)

t_PLUS = r'\+'
t_DASH = r'-'
t_STAR = r'\*'
t_SLASH = r'/'
t_ASSIGN = r'='
t_SEMICOLON = r';'

def t_FLOAT(t):
    r'\d+\.\d*'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9?]*'
    t.type = reserved.get(t.value, 'ID')
    return t

t_ANY_ignore = ' \n\t\f\v'

def t_error(t):
    print "Unrecognized character '%s'at line %d" % (t.value[0], t.lineno)
    t.lexer.skip(1)
