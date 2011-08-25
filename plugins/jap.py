from util import hook, http
import shlex
import os
import subprocess

@hook.command
def jap(inp):
	print ["./deeng"] + inp.split()
	proc = subprocess.Popen(["./deeng"] + inp.split(), stdout=subprocess.PIPE)
	txt = proc.stdout.read()
	proc.wait()
	print "[%s]" % txt
	return txt.replace('^',"").replace("\n"," ")
