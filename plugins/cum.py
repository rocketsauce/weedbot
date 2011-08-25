import random
from util import hook
import re
cs = unicode("( .__.) . o O ( cum )", encoding="utf-8")
ms = unicode("( ﾟ ヮﾟ)　ＭＩＴＯＮ ＧＡ ＳＵＫＩ！！！！", encoding="utf-8")
cp = unicode("( ・ω・) . o O ( crap ass )", encoding="utf-8")

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
@hook.regex(*("weedbot", re.I))
@hook.randreply(1.0)
def weedbotname(inp):
	return random.choice([":D", "hi!", "weed", "gotta love me!", "guess who has a boner", "weeeeeeed", "weeeeeeeeeeeeeeeeed"])
