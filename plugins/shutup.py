import random
from util import hook
import re
choices = ["shut up", "who cares", "i don't know, why don't you ask my butt?", "no one knows"]

@hook.nonick
@hook.regex(*(r"(\?$|^what|^is |^are |^why|^who|^how|^which)", re.I))
@hook.randreply(0.05)
def shutup(inp):
	return random.choice(choices)
