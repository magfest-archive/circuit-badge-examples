from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from autobahn import wamp

from collections import namedtuple

import asyncio

BUTTON_START = "start"
BUTTON_SELECT = "select"
BUTTON_A = "a"
BUTTON_B = "b"
BUTTON_UP = "up"
BUTTON_DOWN = "down"
BUTTON_LEFT = "left"
BUTTON_RIGHT = "right"


Position = namedtuple('Position', ['x', 'y'])


class Player:
    def __init__(self, badge_id, name=""):
        self.badge = badge_id
        self.position = Position(0, 0)
        self.health = 100
        self.name = name

    @property
    def name(self):
        return self.name or str(self.badge)

    def hurt(self, amt=1):
        self.health -= amt

    def heal(self, amt=1):
        self.health += amt

    def move(self, x=0, y=0):
        self.position = Position(self.position.x + x, self.position.y + y)


class ExampleGame(ApplicationSession):
    def __init__(self, component_config, *_, **__):
        #: Maps Badge# => Player
        self.badge_map = {}

    def get_player(self, badge):
        return self.badge_map.get(badge, None)

    @wamp.register(u'game.joincode.updated')
    def joincode(self, code):
        # Turns [['select', 'start'], 'up', 'up', 'down', 'down', 'left', 'right', 'left', 'right', 'b', 'a', 'start'] into "Select+Start, ^ ^ v v < > < > B A Start"
        print("Press {} to join!".format((" ".join((button.title() if isinstance(button, str) else ('+'.join((b.title() for b in button)) + ', ') for button in code)))))

    @wamp.register(u'game.player.join')
    def onjoin(self, badge_id):
        self.badge_map[badge_id] = Player(badge_id)
        print("Badge #{} has entered the game!".format(badge_id))

    @wamp.register(u'game.player.leave')
    def onleave(self, badge_id):
        player = self.get_player(badge_id)
        if player:
            print("Player {} has left the game!".format(player.name))
            del self.badge_map[badge_id]


    @wamp.register(u'badge.button.depress')
    def button_down(self, badge, button):
        player = self.get_player(badge)
        
        if player:
            if button == BUTTON_A:
                player.heal()
            elif button == BUTTON_B:
                player.harm()

                if player.health <= 0:
                    print("Oh no, player {} died!".format(player.badge))
                    player.health = 100
                    player.position = Position(0, 0)

            elif button == BUTTON_SELECT:
                print("Player {0.badge} is at {0.position} with {0.health} health".format(player))
            elif button == BUTTON_START:
                print("Start!!!")
            elif button == BUTTON_LEFT:
                player.move(-1, 0)
            elif button == BUTTON_RIGHT:
                player.move(1, 0)
            elif button == BUTTON_UP:
                player.move(0, 1)
            elif button == BUTTON_DOWN:
                player.move(0, -1)
