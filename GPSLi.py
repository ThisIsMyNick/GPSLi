#!/usr/bin/env python

import ply.lex as lex
import ply.yacc as yacc

import tokenrules
import grammar
import analyzer
import shared
tokens = tokenrules.tokens

import sys

shared.lexer = lex.lex(module=tokenrules)
shared.parser = yacc.yacc(module=grammar)

shared.filename = None

def main(code):
    ast = shared.parser.parse(code)
    analyzer.execute(ast)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        shared.filename = sys.argv[1]
	code = ""
	with open(shared.filename) as f:
		code = f.read()
        main(code)
    else:
	import cgi
	query = cgi.FieldStorage()
	if 'code' in query:
		import urllib
		code = urllib.unquote(query['code'].value)
                #print code
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
