from Game2048 import game2048, Play2048
import random

class ProtoAgent(Play2048):
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

class StupidAgent(ProtoAgent):
    def play(self):
        self.move(self.keys[random.randint(0,3)])

class ThreesAgent(ProtoAgent):
    everyOther = False
    def play(self):
        self.everyOther ^= True
        if random.randint(0, 10) == 5:
            self.move(self.DOWN)
        elif self.everyOther:
            self.move(self.RIGHT)
        else:
            self.move(self.UP)

class MyAgent(ProtoAgent):
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
