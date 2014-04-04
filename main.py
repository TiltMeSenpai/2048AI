import GameAgents
import inspect
import argparse

def main(agent, timeout=1, wait=.1, lookahead_value=.5, depth = 1):
    game = {i[0] : i[1] for i in inspect.getmembers(GameAgents)}[str(agent)](timeout, wait, lookahead_value, depth)
    while True:
        game.play()
        if not game.is_playable():
           if 2048 in game.getField():
               return("Won")
           else:
                game.browser.close()
                return "Lost " + game.browser.find_element_by_class_name('score-container').text

if "main" in __name__:
    args = argparse.ArgumentParser(description="AI for 2048 Game")
    args.add_argument("-agent", type=str, default="StupidAgent")
    args.add_argument("-t", "--timeout", type=int, default=.5)
    args.add_argument("-w", "--wait",  type=int, default=.1)
    args.add_argument("-l", "--lookahead", type=int, default=.5)
    args.add_argument("-d", "--depth", type=int, default=10)
    args = vars(args.parse_args())
    main(args['agent'], args['timeout'], args['wait'], args['lookahead'], args['depth'])