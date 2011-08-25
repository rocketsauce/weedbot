from util import hook
import os
from random import shuffle
import random
from PIL import Image, ImageDraw, ImageFont

@hook.command("comic")
def comic(paraml, input=None, db=None, bot=None, conn=None):
    #print os.getcwd()
    if len(paraml) == 0:
        paraml = input.chan
    msgs = bot.mcache[(paraml,conn)]
    sp = 0
    chars = set()

    for i in xrange(len(msgs)-1, 0, -1):
        sp += 1
        diff = msgs[i][0] - msgs[i-1][0]
        chars.add(msgs[i][1])
        if sp > 10 or diff.total_seconds() > 120 or len(chars) > 3:
            break

    #print sp, chars
    msgs = msgs[-1*sp:]

    panels = []
    panel = []

    for (d, char, msg) in msgs:
        if len(panel) == 2 or len(panel) == 1 and panel[0][0] == char:
            panels.append(panel)
            panel = []
        panel.append((char, msg))

    panels.append(panel)

    print repr(chars)
    print repr(panels)

    fname = ''.join([random.choice("fartpoo42069") for i in range(16)]) + ".jpg"

    make_comic(chars, panels).save(os.path.join("/var/www/runcoward.com/idiotcomics/", fname), quality=85)
    return "http://runcoward.com/idiotcomics/" + fname

def wrap(st, font, draw, width):
    #print "\n\n\n"
    st = st.split()
    mw = 0
    mh = 0
    ret = []

    while len(st) > 0:
        s = 1
        #print st
        #import pdb; pdb.set_trace()
        while True and s < len(st):
            w, h = draw.textsize(" ".join(st[:s]), font=font)
            if w > width:
                s -= 1
                break
            else:
                s += 1

        if s == 0 and len(st) > 0: # we've hit a case where the current line is wider than the screen
            s = 1

        w, h = draw.textsize(" ".join(st[:s]), font=font)
        mw = max(mw, w)
        mh += h
        ret.append(" ".join(st[:s]))
        #print st[:s]
        #print
        st = st[s:]

    return (ret, (mw, mh))

def rendertext(st, font, draw, pos):
    ch = pos[1]
    for s in st:
        w, h = draw.textsize(s, font=font)
        draw.text((pos[0], ch), s, font=font, fill=(0xff,0xff,0xff,0xff))
        ch += h

def fitimg(img, (width, height)):
    scale1 = float(width) / img.size[0]
    scale2 = float(height) / img.size[1]

    l1 = (img.size[0] * scale1, img.size[1] * scale1)
    l2 = (img.size[0] * scale2, img.size[1] * scale2)

    if l1[0] > width or l1[1] > height:
        l = l2
    else:
        l = l1

    return img.resize((int(l[0]), int(l[1])), Image.ANTIALIAS)

def make_comic(chars, panels):
    #filenames = os.listdir(os.path.join(os.getcwd(), 'chars'))

    panelheight = 300
    panelwidth = 450

    filenames = os.listdir('chars/')
    shuffle(filenames)
    filenames = map(lambda x: os.path.join('chars', x), filenames[:len(chars)])
    chars = list(chars)
    chars = zip(chars, filenames)
    charmap = dict()
    for ch, f in chars:
        charmap[ch] = Image.open(f)

    #print charmap


    imgwidth = panelwidth
    imgheight = panelheight * len(panels)

    bg = Image.open("backgrounds/beach-paradise-beach-desktop.jpg")

    im = Image.new("RGBA", (imgwidth, imgheight), (0xff, 0xff, 0xff, 0xff))
    font = ImageFont.truetype("plugins/COMICBD.TTF", 14)

    for i in xrange(len(panels)):
        pim = Image.new("RGBA", (panelwidth, panelheight), (0xff, 0xff, 0xff, 0xff))
        pim.paste(bg, (0, 0))
        draw = ImageDraw.Draw(pim)

        st1w = 0; st1h = 0; st2w = 0; st2h = 0
        (st1, (st1w, st1h)) = wrap(panels[i][0][1], font, draw, 2*panelwidth/3.0)
        rendertext(st1, font, draw, (10, 10))
        if len(panels[i]) == 2:
            (st2, (st2w, st2h)) = wrap(panels[i][1][1], font, draw, 2*panelwidth/3.0)
            rendertext(st2, font, draw, (panelwidth-10-st2w, st1h + 10))

        texth = st1h + 10
        if st2h > 0:
            texth += st2h + 10 + 5

        maxch = panelheight - texth
        im1 = fitimg(charmap[panels[i][0][0]], (2*panelwidth/5.0-10, maxch))
        pim.paste(im1, (10, panelheight-im1.size[1]), im1)

        if len(panels[i]) == 2:
            im2 = fitimg(charmap[panels[i][1][0]], (2*panelwidth/5.0-10, maxch))
            im2 = im2.transpose(Image.FLIP_LEFT_RIGHT)
            pim.paste(im2, (panelwidth-im2.size[0]-10, panelheight-im2.size[1]), im2)

        draw.line([(0, 0), (0, panelheight-1), (panelwidth-1, panelheight-1), (panelwidth-1, 0), (0, 0)], (0, 0, 0, 0xff))
        del draw
        im.paste(pim, (0, panelheight * i))

    return im

if __name__ == "__main__":
    chars = set([u'smELLsBAD_reTARDkrew', u'jeanluc', u'bud'])
    panels = [[(u'smELLsBAD_reTARDkrew', u'naw'), (u'jeanluc', u'w/e.......')], [(u'bud', u'\x037R\x038A\x039P\x0311E\x0312 \x0313I\x034N\x037 \x038P\x039R\x0311I\x0312S\x0313O\x034N http://www.loompanics.com/Articles/RapeInPrison.html You may be raped when you go to prison. I am not trying to scare you. ... Most   rapes are not reported. Sexual attacks in prison are considered rape ... This   guide is for the person who has never done any kind of time. ... He himself has   been in several times. Chances of rape in this situation: Practically zero. ...'), (u'jeanluc', u'same')], [(u'smELLsBAD_reTARDkrew', u'what do u think it would b like being sold a dozen times or traded for a few cigs all da time')], [(u'smELLsBAD_reTARDkrew', u'does it turn u on'), (u'jeanluc', u'it would be like being a g0d')], [(u'smELLsBAD_reTARDkrew', u'my cellm8s were faggots')], [(u'smELLsBAD_reTARDkrew', u'las tcellbklock no1 slept the whole time i was trhere')], [(u'smELLsBAD_reTARDkrew', u'i think they went 2 their beds as i was leavin')], [(u'smELLsBAD_reTARDkrew', u'l0l')]]

    make_comic(chars, panels).save("/var/www/runcoward.com/img/img.jpg")
