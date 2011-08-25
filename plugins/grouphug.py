from util import hook, http
import random
import string

@hook.command('gh')
@hook.command
def grouphug(inp, nick='', chan='', say=None):
    rs = ''.join(random.choice(string.letters) for i in xrange(10))
    if inp == '':
        h = http.get_html("http://grouphug.us/random/%s" % rs)
    else:
        h = http.get_html("http://grouphug.us/%s") % (inp)
    hugID = h.xpath('//h2[@class="title"]/a/text()')[1]
    hugContent = h.xpath('//div[@class="content"]/p/text()')[1]
    say(hugContent)

@hook.command('fml')
@hook.command('fm.l')
@hook.command
def fuckmylife(inp, nick='', chan='', say=None):
    h = http.get_html("http://m.fmylife.com/random/")
    #else:
    # h = http.get_html("http://iphone.fmylife.com/%s") % (inp)
    fmlContent = h.xpath('//p[@class="text"]/text()')[0]
    say(fmlContent)

@hook.command('weed')
@hook.command('amnizu')
@hook.command
def thathigh(inp, nick='', chan='', say=None):
    h = http.get_html("http://thathigh.com/random/")
    highContent = h.xpath('//a[@class="storylink"]/text()')[0]
    highOutput = "\x02%s\x0F" % (highContent)
    say(highOutput)
