from util import hook
from random import randint

def db_init(db):
	db.execute("create table if not exists dicescore(name, score,"
			"primary key(name))")
	db.commit()

@hook.command("42069")
def dicegame(inp, nick='', chan='', db=None, input=None):
	db_init(db)

	results = map(lambda x: randint(1, 420), range(69))
	cnt = len(filter(lambda x: x == 420, results))

	db.execute("insert or replace into dicescore(name, score) values(?,?)", (input.nick.lower(), cnt))
	db.commit()

	hscore = db.execute("select name, score from dicescore order by score desc limit 1").fetchone()

	print hscore

	return "Your score: %d! Highest score by %s: %d" % (cnt, hscore[0], hscore[1])
