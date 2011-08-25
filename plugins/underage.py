from mechanize import Browser
import re
from util import hook
import urllib

@hook.command
def legal(inp):
	args = {"action":"opensearch", "search":inp,"imit":"1"}
	q = "http://en.wikipedia.org/w/api.php?%s" % urllib.urlencode(args)

	f = urllib.urlopen(q)
	s = f.read()
	print s
	n2 = eval(s)[1][0]

	print n2
	n = n2.replace(" ", "_")

	q = "http://en.wikipedia.org/wiki/%s" % n

	f.close()

	br = Browser()
	br.set_handle_robots(False)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

	f = br.open(q)
	s = f.read()

	res = re.search("\(age.*?([0-9]+)\)", s)

	if int(res.group(1)) >= 18:
		return "%s is legal! (%s years old)" % (n2, res.group(1))
	else:
		return "%s is %s and isn't legal yet, hella boner kill.. or not? >:]" % (n2, res.group(1))
