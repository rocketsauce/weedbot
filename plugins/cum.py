import random
from util import hook
import re
cs = unicode("( .__.) . o O ( cum )", encoding="utf-8")
ms = unicode("( ﾟ ヮﾟ)　ＭＩＴＯＮ ＧＡ ＳＵＫＩ！！！！", encoding="utf-8")
cp = unicode("( ・ω・) . o O ( crap ass )", encoding="utf-8")
ft = unicode("ヾ(´□｀* )ノ ftw ヾ(@゜∇゜@)ノ ftw o(≧∇≦o) ftw (´∇ﾉ｀*)ノ", encoding="utf-8")
ap = unicode("( ･ิз･ิ) apple basically makes the best computers.. heh", encoding="utf=8")

@hook.nonick
@hook.regex(*("cum", re.I))
@hook.randreply(0.5)
def cum(inp):
	return cs

@hook.nonick
@hook.regex(*("mitten", re.I))
@hook.randreply(0.5)
def mitten(inp):
	return ms

@hook.nonick
@hook.regex(*("crap", re.I))
@hook.randreply(0.5)
def crap(inp):
	return cp

@hook.nonick
@hook.regex(*("ass", re.I))
@hook.randreply(0.5)
def ass(inp):
	return cp

@hook.nonick
@hook.regex(*("ftw", re.I))
@hook.randreply(0.5)
def ftw(inp):
    return ft

@hook.nonick
@hook.regex(*("(^| )own($|s|ed)", re.I))
@hook.randreply(0.5)
def owns(inp):
    ons = unicode("owns "*random.randint(1, 3) + "OWNS "*random.randint(1, 3) + "o-(' 'Q)")
    return ons

@hook.nonick
@hook.regex(*("apple", re.I))
@hook.randreply(0.5)
def apple(inp):
	return ap

@hook.nonick
@hook.regex(*("weedbot", re.I))
@hook.randreply(1.0)
def weedbotname(inp):
	return random.choice([":D", "hi!", "weed", "gotta love me!", "guess who has a boner", "weeeeeeed", "weeeeeeeeeeeeeeeeed"])
