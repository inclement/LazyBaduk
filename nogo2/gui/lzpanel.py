from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import (StringProperty, BooleanProperty, ObjectProperty,
                             ListProperty, NumericProperty)

from colorsys import hsv_to_rgb

class LzInfoPanel(BoxLayout):
    lz_name = StringProperty('')
    lz_version = StringProperty('')
    lz_ready = BooleanProperty(False)
    lz_up_to_date = BooleanProperty(False)
    lz_status = StringProperty('loading')

    lz_analysis = ListProperty([])

    board = ObjectProperty(None)


class LzPonderingMarker(Label):
    move = ObjectProperty()

    coordinates = StringProperty('A1')
    visits = NumericProperty(0)
    winrate = NumericProperty(50.0)
    relative_visits = NumericProperty(0)

    bg_colour = ListProperty([1, 1, 1, 1])

    border_colour = ListProperty([0.5, 0.5, 0.5, 0.5])

    def on_move(self, instance, move):
        self.visits = move.visits
        self.winrate = move.winrate
        self.relative_visits = move.relative_visits
    
    def on_relative_visits(self, instance, number):
        r, g, b = hsv_to_rgb(number * 0.33333, 1, 1)  # hue varying from red to green
        alpha = 0.55 + number * 0.3

        r = max(r, 0.2)
        g = max(g, 0.2)
        b = max(b, 0.2)
        self.bg_colour = (r, g, b, alpha)

        if number == 1.0:
            self.border_colour = [0.3, 0.3, 1.0, 0.75]
        else:
            self.border_colour = [1, 1, 1, 0]


class LzVariationDisplay(Button):
    move = ObjectProperty(None)

    coordinates = StringProperty('')

    def on_move(self, instance, move):
        self.coordinates = move.lz_coordinates


class LzVariationSelector(GridLayout):

    moves = ListProperty([])

    def on_moves(self, instance, moves):
        self.make_num_children(len(moves))

        for move, selector in zip(self.moves, self.children[::-1]):
            selector.move = move

    def make_num_children(self, number):
        """Makes sure the number of child widgets equals the given number."""

        while len(self.children) > number:
            self.remove_widget(self.children[0])

        while len(self.children) < number:
            self.add_widget(LzVariationDisplay(move=self.moves[0]))

        print(number, self.children)
