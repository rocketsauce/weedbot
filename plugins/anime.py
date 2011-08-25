from util import hook
from BeautifulSoup import BeautifulSoup
from mechanize import Browser
import re
import random

prefs = ["nyaaaa~!", "hai!"]

def getimgs(url):
    br = Browser()
    br.set_handle_robots(False)
    result = br.open(url)
    fc = result.read()

    soup = BeautifulSoup(fc)
    xs = soup.findAll("a", {"href": re.compile("http://images.4chan.org/a/src/.*$")})
    xs = list(set(map(lambda x: x["href"], xs)))
    return xs

@hook.command
def anime(inp, nick='', chan='', db=None):
    xs = getimgs("http://boards.4chan.org/a/")
    return "%s %s" % (random.choice(prefs), random.choice(xs))

@hook.command
def hentai(inp, nick='', chan='', db=None):
    xs = getimgs("http://boards.4chan.org/h/")
    return "check out this hot slice of nws action %s %s" % (random.choice(prefs), random.choice(xs))

