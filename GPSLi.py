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

def main(code):
    ast = parser.parse(code)
    analyzer.execute(ast)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
	code = ""
	with open(filename) as f:
		code = f.read()
        main(code)
    else:
	import cgi
	query = cgi.FieldStorage()
	if 'code' in query:
		import urllib
		code = urllib.unquote(query['code'].value)
                print "Content-Type: text/html\r\n\r"
		print "<!DOCTYPE html>"
		print "<html>"
		print "<head><title>1337 interpreter</title></head>"
		print "<body>"
		print "<p>"
		main(code)
		print "</p>"
		print "</body>"
		print "</html>"
	else:
		print "No code field :C"
