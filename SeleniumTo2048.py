from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
