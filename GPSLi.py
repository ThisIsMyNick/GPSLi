#!/usr/bin/env python

import ply.lex as lex
import ply.yacc as yacc

import tokenrules
import grammar
import analyzer
tokens = tokenrules.tokens

import sys

lexer = lex.lex(module=tokenrules)
parser = yacc.yacc(module=grammar)

def main(filename):
    code = ""
    with open(filename) as f:
        code = f.read()
    ast = parser.parse(code)
    analyzer.execute(ast)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        main(filename)
    else:
        print 'Expected filename.'
        sys.exit(1)
