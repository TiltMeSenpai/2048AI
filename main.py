import random
from timeit import timeit
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class game2048:
    cards = {"tile-" + str(2 ** i): 2 ** i for i in range(1, 12)}
    coordinates = {"tile-position-" + str(i) + '-' + str(j): (j - 1, i - 1) for i in range(1, 5) for j in range(1, 5)}
    UP = Keys.ARROW_UP
    LEFT = Keys.ARROW_LEFT
    DOWN = Keys.ARROW_DOWN
    RIGHT = Keys.ARROW_RIGHT
    keys = [UP, LEFT, DOWN, RIGHT]

    def __init__(self, wait=10):
        self.timeout = wait
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(wait)
        self.browser.get('http://gabrielecirulli.github.io/2048/')
        self.browser.maximize_window()
        self.input = self.browser.find_element_by_class_name('tile-container')
        PlayingField.__init__(self)


class PlayingField:
    def __init__(self, field=[[0] * 4 for i in range(4)]):
        self.field = tuple(field[i] for i in range(field.__len__()))

    def getField(self):
        return self.field

    def getRow(self, i):
        return self.field[i]

    def getCollumn(self, i):
        return [self.field[x][i] for x in range(self.field[0].__len__())]


class Play2048(PlayingField, game2048):
    def setField(self, browser):
        self.field = tuple([0] * 4 for i in range(4))
        while True:
            try:
                tiles = [format(i.get_attribute("class")).split(" ")[1:3] for i in browser.find_elements_by_class_name("tile")]
            except:
                continue
            else:
                break
        for tile in tiles:
            self.field[self.coordinates[tile[1]][0]][self.coordinates[tile[1]][1]] = \
                self.cards[tile[0]] if not None else 0

    def shift(self, tmp):
        l = list(tmp)
        for n in range(l.__len__() - l.count(0)):
            if not 0 in l: break
            i = l.index(0)
            for j in range(4)[i:]:
                if l[j] != 0:
                    l[i], l[j] = l[j], l[i]
                    break
        return l

    def combine(self, tmp):
        l = list(tmp)
        for n in range(l.__len__()):
            try:
                if l[n] == l[n + 1]:
                    l[n] *= 2
                    l[n + 1] = 0
                    l = self.shift(l)
            except IndexError:
                return l

    def look(self, dir, state = None):
        if state is None: state = self.field
        directions = {
            self.UP: self.moveUp,
            self.RIGHT: self.moveRight,
            self.DOWN: self.moveDown,
            self.LEFT: self.moveLeft
        }
        return directions[dir](state)

    def moveUp(self, state):
        tmp = list(zip(*state))
        for c in range(tmp.__len__()):
            tmp[c] = self.shift(tmp[c])
            tmp[c] = self.combine(tmp[c])
        return list(zip(*tmp))

    def moveLeft(self, state):
        tmp = list(state)
        for c in range(tmp.__len__()):
            tmp[c] = self.shift(tmp[c])
            tmp[c] = self.combine(tmp[c])
        return tmp

    def moveRight(self, state):
        tmp = [state[i][::-1] for i in range(state.__len__())]
        for c in range(tmp.__len__()):
            tmp[c] = self.shift(tmp[c])
            tmp[c] = self.combine(tmp[c])
        return [tmp[i][::-1] for i in range(tmp.__len__())]

    def moveDown(self, state):
        tmp = list(zip(*state[::-1]))
        for c in range(tmp.__len__()):
            tmp[c] = self.shift(tmp[c])
            tmp[c] = self.combine(tmp[c])
        return list(zip(*tmp))[::-1]

    def lookUp(self, i, j, field):
        w, x, y, z = field
        tmp = list(zip(w, x, y, z))
        return tmp[i][:j]

    def lookDown(self, i, j, field):
        w, x, y, z = field
        tmp = list(zip(w, x, y, z))
        return tmp[i][j + 1:]

    def lookLeft(self, i, j, field):
        return field[j][:i]

    def lookRight(self, i, j, field):
        return field[j][i + 1:]

    def area(self, i, j, field):
        dir = [
            self.lookUp,
            self.lookRight,
            self.lookDown,
            self.lookRight
        ]
        return [move(i, j, field) for move in dir]

    def move(self, dir):
        if not dir in self.keys: raise ValueError
        self.input.send_keys(dir)
        time.sleep(self.wait)
        self.setField(self.browser)
        return dir

    def is_playable(self):
        self.browser.implicitly_wait(0)
        ret = self.browser.find_elements_by_class_name('game-over').__len__() == 0
        self.browser.implicitly_wait(self.timeout)
        return ret

    def __init__(self, timeout = 10, wait = .5):
        game2048.__init__(self, timeout)
        self.wait = wait
        self.setField(self.browser)

class ExampleAgent(Play2048):
    def __init__(self, timeout, wait, lookahead_value, depth):
        Play2048.__init__(self, timeout, wait)
        self.lookahead_value = lookahead_value
        self.depth = depth

    def play(self):
        raise NotImplementedError("Play should make one move when called")
    
'''
    Insert your agent here. The simplest way to make an agent would be to inherit the ExampleAgent class, then extend
    the play function.
'''

class StupidAgent(ExampleAgent):
    def play(self):
        print(self.move(self.keys[random.randint(0,3)]))

class MyAgent(ExampleAgent):
    def play(self):
        moves = [self.heuristic(m) for m in self.keys]
        self.move(self.keys[random.choice(self.list_duplicates_of(moves, max(moves)))])

    def list_duplicates_of(self, seq, item):
        start_at = -1
        locs = []
        while True:
            try:
                loc = seq.index(item,start_at+1)
            except ValueError:
                break
            else:
                locs.append(loc)
                start_at = loc
        return locs

    def heuristic(self, direction, original=True, field=None):
        look = self.look(direction, field)
        points = 0
        for i in range(16):
            count = 2*(sorted([it for s in look for it in s])[i]) - sorted([it for s in self.field for it in s])[i]
            points += count if count > 0 else 0
        if original:
            for i in range(self.depth):
                moves = [self.heuristic(m, False, look) for m in self.keys]
                points += self.heuristic(self.keys[moves.index(max(moves))], False, look) * self.lookahead_value**i
        return points


def main(agent, timeout=1, wait=.1, lookahead_value=.5, depth = 1):
    game = globals()[str(agent)](timeout, wait, lookahead_value, depth)
    while True:
        game.play()
        if not game.is_playable():
           if 2048 in game.getField():
               return("Won")
           else:
                game.browser.close()
                return "Lost " + game.browser.find_element_by_class_name('score-container').text

print(main('MyAgent', 0, .05, .999, 10))