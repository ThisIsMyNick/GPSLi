#TODO: rename token names to be less generic. eg, MINUS rather than DASH.
#TODO: use a literals[] list

reserved = {
        'print' : 'PRINT',
        'if' : 'IF',
        'else' : 'ELSE',
        'while' : 'WHILE',
        'for' : 'FOR',
        'func' : 'FUNC',
        'return' : 'RETURN',
        'true' : 'TRUE',
        'false' : 'FALSE',
}

tokens = (
        'PLUS',
        'DASH',
        'STAR',
        'SLASH',
        'MOD',
        'ASSIGN',
        'EQUAL',
        'NEQUAL',
        'GT',
        'GE',
        'LT',
        'LE',
        'TRUE',
        'FALSE',
        'AND',
        'OR',
        'XOR',
        'NOT',
        'ID',
        'STRING',
        'FLOAT',
        'INT',
        'PRINT',
        'IF',
        'ELSE',
        'WHILE',
        'FOR',
        'FUNC',
        'RETURN',
        'SEMICOLON',
        'COMMA',
        'LPAREN',
        'RPAREN',
        'LBRACE',
        'RBRACE',
        'LBRACKET',
        'RBRACKET',
)

t_PLUS = r'\+'
t_DASH = r'-'
t_STAR = r'\*'
t_SLASH = r'/'
t_MOD = r'%'
t_EQUAL = r'=='
t_NEQUAL = r'!='
t_GT = r'>'
t_GE = r'>='
t_LT = r'<'
t_LE = r'<='
t_AND = r'&&'
t_OR = r'\|\|'
t_XOR = r'\^'
t_NOT = r'!'
t_ASSIGN = r'='
t_SEMICOLON = r';'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

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

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1] #strip quotes
    return t

def t_COMMENT(t):
    r'/\*(.|\n)*\*/|//.*'
    pass

t_ANY_ignore = ' \n\r\t\f\v'

def t_error(t):
    print "Unrecognized character '%s'at line %d" % (t.value[0], t.lineno)
    t.lexer.skip(1)
