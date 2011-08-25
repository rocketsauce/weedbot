import re
from datetime import datetime
import pytz
from astral import Astral
import random
import threading
a = Astral()
cty = a.citydb.cities

lo = threading.RLock()
chans = set()

def getzone():
	#t = datetime(2011, 06, 29, 3, 35, 00)
	t = datetime.today()
	t = pytz.timezone('America/Los_Angeles').localize(t)
	t = t.astimezone(pytz.utc)
	if t.minute in [20, 35, 50, 5]:
		random.shuffle(cty)
		for c in cty:
			timezone = a[c].timezone
			q = t.astimezone(pytz.timezone(timezone))
			if q.hour == 16 and q.minute == 20:
				return "!!! WEED ALARM!!! hell yea its 420 in %s, %s..! smoke weed ( .__.) . o O ( weed )" % (c, a[c].country)
	return None

if __name__ == "__main__":
	print getzone()
else:
	from util import hook

	@hook.nonick
	@hook.regex(*(".*", re.I))
	def weedalarm(inp, nick='', chan='', db=None, input=None):
		r = getzone()
		if r == None:
			lo.acquire()
			chans.clear()
			lo.release()
		else:
			if chan in chans:
				r = None
			if len(chan)>0:
				chans.add(chan)
		return r

