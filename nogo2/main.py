#i Pass empty args on to Kivy, because it annoyingly parses them on import
import sys
argv = sys.argv[1:]
sys.argv = sys.argv[:1]

import os

from kivy.app import App
from kivy import platform
from kivy.core.window import Window
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
import menu

print('cb', misc.ColouredButton)

print('board', board.__file__)

print('argv is', sys.argv)


class NogoApp(App):
    cache = ObjectProperty(WidgetCache())

    stone_type = StringProperty('simple')

    def __init__(self, board_size=19, load_sgf=None, **kwargs):
        super().__init__(**kwargs)
        self.board_size = board_size
        self.load_sgf = load_sgf

    def build(self):
        w = board.PhoneBoardView()
        w.ids.bc.board.gridsize = self.board_size
        if self.load_sgf is not None:
            w.ids.bc.board.load_sgf_from_file('', [self.load_sgf])

        Window.bind(on_keyboard=self.key_input)
        Window.bind(on_request_close=self.on_request_close)

        return w

    def key_input(self, window, key, scancode, codepoint, modifier):
        print('Received key {}'.format(key))
        if key == 27:
            self.back_button_leave_app()
            return True  # back button now does nothing on Android
        return False

    def back_button_leave_app(self):
        if platform != 'android':
            return
        from jnius import autoclass
        activity = autoclass('org.kivy.android.PythonActivity')
        activity.moveTaskToBack(True)


    def play_stone_sound(self):
        pass

    def on_pause(self):
        # Stop LZ pondering to avoid causing problems in the background
        self.root.ids.bc.board.lz_ponder(False)
        return True

    def on_stop(self):
        self.clean_up_subprocess()

    def on_request_close(self, *args, **kwargs):
        self.clean_up_subprocess()

    def clean_up_subprocess(self):
        self.root.ids.bc.board.lz_ponder(False)
        self.root.ids.bc.board.lz_wrapper.kill()

def run(*args, **kwargs):
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--board-size', type=int, default=19)
    parser.add_argument('--load-sgf', default=None)

    args, unknown = parser.parse_known_args(argv)

    NogoApp(board_size=args.board_size,
            load_sgf=args.load_sgf).run()


if __name__ == "__main__":
    run()
