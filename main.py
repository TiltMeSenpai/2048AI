import GameAgents

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