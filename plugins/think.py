from util import hook

@hook.command
@hook.nonick
def think(inp):
	return "( .__.) . o O ( %s )" % inp
