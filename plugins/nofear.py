from random import choice
import string
fortunes = []

f = open("nofear/nofear.txt", "r")
fc = f.read()
f.close()

fortunes = map(lambda x: string.strip(x), fc.split("\n"))

def getfortune():
    return choice(fortunes)

if __name__ == "__main__":
    print getfortune()
else:
    from util import hook
    @hook.command
    def nofear(inp):
        return getfortune()
