from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.properties import (ListProperty, NumericProperty)

from kivy.lang import Builder

Builder.load_file('gui/misc.kv')


class ColouredButton(ButtonBehavior, Label):
    background_normal = ListProperty([1, 1, 1, 1])
    background_down = ListProperty([0.5, 0.5, 0.5, 1])
    padding = NumericProperty(0)
    radius = NumericProperty(0)
