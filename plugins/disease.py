#!/usr/bin/env python

"""
disease.py written by Rocketsauce 2011
"""

from util import hook

from parse import parser
import parse
from sys import argv

class disease:
	def process_story(self):
		for rule in self.story.rules.values():
			self.process_expr(rule.body)

	def process_expr(self, e):
		if e.__class__ == parse.choice or e.__class__ == parse.lst:
			for exp in e.body:
				self.process_expr(exp)
		elif e.__class__ == parse.expr:
			self.process_expr(e.body)
		elif e.__class__ == parse.nonterm:
			if self.story.rules[e.body] != None:
				e.body = self.story.rules[e.body]

	def __init__(self, path):
		self.path = path
		f = open(path, "r")
		self.story = parser.parse(f.read())
		f.close()

		self.process_story()
	
	def __str__(self):
		ret = str()
		for rule in self.story.rules.keys():
			ret += "%s:\n\t%s\n\n" % (rule, self.story.rules[rule])

		return ret
	
	def gen_story(self):
		return self.story.gen_value()

for arg in argv[1:]:
	d = disease(arg)
	for i in xrange(10):
		print d.gen_story()

@hook.command
def web20(inp, nick='', chan='', db=None):
	d = disease("plugins/web2.0.rul")
	return d.gen_story()

@hook.command
def porntitle(inp, nick='', chan='', db=None):
	d = disease("plugins/porntitle.rul")
	return d.gen_story()

@hook.command
def tosgen(inp, nick='', chan='', db=None):
	d = disease("plugins/tosgen.rul")
	return d.gen_story()
