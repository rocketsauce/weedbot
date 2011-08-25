import mechanize
from datetime import datetime,timedelta,time

def getvals():
	url = "https://mtgox.com/code/data/getTrades.php"
	lens = [timedelta(minutes=10), timedelta(hours=1), timedelta(hours=12), timedelta(hours=24), timedelta(hours=48)]
	br = mechanize.Browser()
	response = br.open(url)
	p = eval(response.read())
	#print "latest date: %s" % datetime.fromtimestamp(p[-1]["date"])

	now = datetime.now()

	b = map(lambda x: (now - datetime.fromtimestamp(x["date"]), x["amount"]), p)
	b = map(lambda x: filter(lambda y: y[0] <= x, b), lens)
	b = map(lambda x: reduce(lambda y, z: y + z[1], x, 0), b)
	b = map(lambda (x, y): x / (y.days * 24 *60 + y.seconds / 60), zip(b, lens))

	px = map(lambda x: x["price"], p)
	mx = max(px)
	mn = min(px)
	md = max(map(lambda x:x["date"], p))
	#print "max date: %s" % datetime.fromtimestamp(md)
	t = datetime.fromtimestamp(p[-1]["date"]).timetz().isoformat()
	lp = p[-1]["price"]
	b = [lp, t, mn, mx] + b

	return "Latest price: \x02$%.2f\x02@%s, 48h min: \x02$%.2f\x02, 48h max: \x02$%.2f\x02, BTC/min last 10m/1h/12h/24h/48h: \x02%.2f\x02/\x02%.2f\x02/\x02%.2f\x02/\x02%.2f\x02/\x02%.2f\x02" % tuple(b)

a = getvals() 
at = datetime.now()

if __name__ == "__main__":
	print getvals()
else:
	from util import hook
	@hook.command
	def bitcoins(inp):
		global a
		global at
		print at
		print datetime.now() - at
		if datetime.now() - at > timedelta(minutes=1):
			print "getting new btc value"
			a = getvals()
			at = datetime.now()
		return a
