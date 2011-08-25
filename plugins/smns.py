from urllib import urlencode
import re
import string
from BeautifulSoup import BeautifulSoup
from mechanize import Browser
import random
import threading

lo = threading.RLock()
posts = {}

_MP = 10

def getposts(term=''):
	global posts
	br = Browser()
	br.set_handle_robots(False)
	lo.acquire()
	u = "http://shitmyniggersays.com/index.php?p=random"
	data = {}

	if len(term) > 0:
		u = "http://shitmyniggersays.com/index.php?p=search"
		data = {"q": term, "do": "search", "submit": "search"}
		data = urlencode(data)
	try:
		br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
		if len(term) > 0:
			response = br.open(u, data)
		else:
			response = br.open(u)
		soup = BeautifulSoup(response.read())
		print "got page"
		entries = soup.findAll("td", {"class": "body"})
		if term not in posts:
			posts[term] = []
		for entry in entries:
			for sibls in entry.contents:
				if sibls.string is not None and len(string.strip(sibls.string)) > 0:
					posts[term].append(string.strip(sibls.string))
	except RuntimeError as err:
		print err
		pass
	finally:
		lo.release()

def getpost(term=''):
	global posts
	lo.acquire()
	try:
		if term not in posts or len(posts[term]) < _MP:
			getposts(term)
		pst = posts[term][0]
		posts[term] = posts[term][1:]
	finally:
		lo.release()
	return pst

if __name__ == "__main__":
	getpost("weed")
else:
	from util import hook
	"""@hook.command
	def ebonic(inp):
		global posts
		return getpost(inp)

	@hook.regex(*('.*', re.I))
	def updateposts(inp):
		global posts
		lo.acquire()
		try:
			if '' not in posts or len(posts['']) < _MP:
				getposts()
		finally:
			lo.release()

	@hook.randreply(0.01)
	@hook.regex(*(".*", re.I))
	@hook.nonick
	def randebon(inp):
		return getpost()"""

	@hook.command
	def ebonic(inp, conn=None, nick='', chan='', say=None):
		conn.cmd("KICK", [chan, nick])
