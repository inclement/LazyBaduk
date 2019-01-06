from kivy.app import App
from kivy import platform
from kivy.properties import (ObjectProperty, StringProperty)

import sys
from os.path import abspath, join, dirname

nogo_path = dirname(abspath(__file__))
sys.path.append(nogo_path)
sys.path.append(dirname(nogo_path))
sys.path.append(join(nogo_path, 'ext'))

# if platform == 'android':
#     from .gui import board
# else:
#     from nogo2.gui import board

from gui import board, misc
from widgetcache import WidgetCache

print('cb', misc.ColouredButton)

print('board', board.__file__)

print('argv is', sys.argv)


class NogoApp(App):
    cache = ObjectProperty(WidgetCache())

    stone_type = StringProperty('simple')

    def build(self):
        w = board.PhoneBoardView()

        return w

    def play_stone_sound(self):
        pass

    def on_pause(self):
        # Stop LZ pondering to avoid causing problems in the background
        self.root.ids.bc.board.lz_ponder(False)
        return True

def run(*args, **kwargs):
    NogoApp().run()


if __name__ == "__main__":
    run()
