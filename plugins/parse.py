import ply.yacc as yacc
import types
import ply.lex as lex
from random import random,randrange

tokens = (
	'LSQUARE',
	'RSQUARE',
	'LBRACE',
	'RBRACE',
	'EQUALS',
	'COLON',
	'NUMBER',
	'STRING',
	'NONTERM',
	'AT',
	'PLUS',
)

t_LSQUARE	= r'\['
t_RSQUARE	= r'\]'
t_LBRACE	= r'\{'
t_RBRACE	= r'\}'
t_EQUALS	= r'='
t_COLON		= r'\:'
t_AT		= r'@'
t_PLUS		= r'\+'

def t_NUMBER(t):
	r'\d*\.\d+'
	t.value = float(t.value)
	return t
	
def t_STRING(t):
	r'".*?"'
	return t
	
def t_NONTERM(t):
	'[A-Za-z][A-Za-z0-9]*'
	return t
	
def t_error(t):
	print "Illegal character '%s'" % t.value[0]
	t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    #t.lexer.lineno += len(t.value)
    #t.lexer.current = t.lexer.lexpos

def t_whitespace(t):
	'[ \t]'

lexer = lex.lex(lextab="diseasetab")

class rule:
	def __init__(self, name, body):
		self.name = name
		self.body = body
	def __str__(self):
		return "%s: %s" % (self.name, self.body)
	def __repr__(self):
		return str(self)

	def gen_value(self):
		return self.body.gen_value()

class story:
	def __init__(self, rules):
		self.rules = rules
	def __str__(self):
		return str(self.rules)

	def gen_value(self):
		return self.rules["root"].gen_value()

class expr:
	def __init__(self, body, prob=1):
		self.body = body
		self.prob = prob
	def __str__(self):
		if self.prob == 1:
			return "%s" % self.body
		else:
			return "(%s * %s)" % (self.body, self.prob)
	def __repr__(self):
		return str(self)

	def gen_value(self):
		if random() < self.prob:
			return self.body.gen_value()
		else:
			return None

class choice:
	def __init__(self, body):
		self.body = body
	def __str__(self):
		return str(self.body)
	def __repr__(self):
		return str(self)

	def gen_value(self):
		return self.body[randrange(len(self.body))].gen_value()

class lst:
	def __init__(self, body, split=True):
		self.body = body
		self.split = split
	def __str__(self):
		return str(self.body)
	def __repr__(self):
		return str(self)

	def gen_value(self):
		l = filter(lambda x: x != None, map(lambda x: x.gen_value(), self.body))
		if len(l) == 0:
			return None
		else:
			if self.split:
				return " ".join(l)
			else:
				return "".join(l)
		
class literal:
	def __init__(self, body):
		self.body = body
	def __str__(self):
		return str(self.body)
	def __repr__(self):
		return str(self)

	def gen_value(self):
		return self.body

class nonterm:
	def __init__(self, body, plus=False):
		self.body = body
		self.plus = plus
	def __str__(self):
		return str(self.body)
	def __repr__(self):
		return str(self)

	def gen_value(self):
		val = self.body.gen_value()
		val2 = None
		if self.plus:
			if random() < .5:
				val2 = self.body.gen_value()
				while val2 == val:
					val2 = self.body.gen_value()
		
		if val2 != None:
			return "%s %s" % (val, val2)
		else:
			return val

"""

****** PARSER STARTS HERE ******

"""

start = 'story'

def p_story(p):
	'''story : rules'''
	p[0] = story(p[1])
	
def p_rule(p):
	'''rule : NONTERM EQUALS pexpr'''
	p[0] = rule(p[1], p[3])

def p_rules(p):
	'''rules : rule
	         | rule rules'''
	
	p[0] = dict()
	
	p[0][p[1].name] = p[1].body
	if len(p) > 2:
		p[0] = dict(p[0].items() + p[2].items())

def p_expr(p):
	'''expr : choice
	        | lst 
	        | STRING
	        | NONTERM
		| NONTERM PLUS'''
	if type(p[1]) == types.InstanceType:
		p[0] = p[1]
	elif p[1][0] == '"':
		p[0] = literal(p[1][1:-1])
	else:
		if len(p) == 3:
			p[0] = nonterm(p[1], True)
		else:
			p[0] = nonterm(p[1])

def p_pexpr(p):
	'''pexpr : NUMBER COLON expr
	         | expr'''
	if len(p) == 2:
		p[0] = expr(p[1])
	elif len(p) == 4:
		p[0] = expr(p[3], p[1])

def p_exprs(p):
	'''exprs : pexpr
	         | pexpr exprs'''
	
	if len(p) == 2:
		p[0] = [ p[1] ]
	elif len(p) == 3:
		p[0] = [ p[1] ] + p[2]

def p_lst(p):
	'''lst : LBRACE exprs RBRACE
	       | AT LBRACE exprs RBRACE'''
	
	if len(p) == 4:
		p[0] = lst(p[2])
	elif len(p) == 5:
		p[0] = lst(p[3], False)

def p_choice(p):
	'''choice : LSQUARE exprs RSQUARE'''
	p[0] = choice(p[2])

def p_error(p):
    print "Syntax error in input!", (p.value, p.lexer.lineno, p.lexer.lexpos - p.lexer.current)


parser = yacc.yacc()
