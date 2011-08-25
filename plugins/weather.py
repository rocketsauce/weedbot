"weather, thanks to google"

from util import hook, http


@hook.command(autohelp=False)
def weather(inp, nick='', server='', reply=None, db=None):
    ".weather <location> [dontsave] -- gets weather data from Google"

    loc = inp

    dontsave = loc.endswith(" dontsave")
    if dontsave:
        loc = loc[:-9].strip().lower()

    db.execute("create table if not exists weather(nick primary key, loc)")

    if not loc:  # blank line
        loc = db.execute("select loc from weather where nick=lower(?)",
                            (nick,)).fetchone()
        if not loc:
            return weather.__doc__
        loc = loc[0]
    
    """h = http.get_html("http://thefuckingweather.com/", zipcode=loc, CELSIUS="yes")
    state = h.xpath("/html/body/div[2]/div/text()")
    place = h.xpath("/html/body/div/span/text()")
    quote = h.xpath("/html/body/div[2]/div[2]/span/text()")

    print quote
    #return "%s %s" % (state[0], state[1])

    info = dict()
    info['temp'] = state[0]
    info['conditions'] = state[1]
    info['city'] = place[0]
    info['quote'] = quote[0]
    #reply("%(city)s: %(temp)s %(conditions)s. %(quote)s" % info)"""

    w = http.get_xml('http://www.google.com/ig/api', weather=loc)
    w = w.find('weather')

    if w.find('problem_cause') is not None:
        return "Couldn't fetch weather data for '%s', try using a zip or " \
                "postal code." % inp

    info = dict((e.tag, e.get('data')) for e in w.find('current_conditions'))
    info['city'] = w.find('forecast_information/city').get('data')
    info['high'] = w.find('forecast_conditions/high').get('data')
    info['low'] = w.find('forecast_conditions/low').get('data')

    s = '%(city)s: %(condition)s, %(temp_f)sF/%(temp_c)sC (H:%(high)sF'\
            ', L:%(low)sF), %(humidity)s, %(wind_condition)s.' % info
    
    reply(s)

    if inp and not dontsave:
        db.execute("insert or replace into weather(nick, loc) values (?,?)",
                     (nick.lower(), loc))
        db.commit()
