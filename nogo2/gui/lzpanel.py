from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.properties import (StringProperty, BooleanProperty, ObjectProperty,
                             ListProperty, NumericProperty)
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color
from kivy.metrics import dp

from colorsys import hsv_to_rgb

from gui.widgets import ColouredButton

class LzInfoPanel(BoxLayout):
    lz_name = StringProperty('')
    lz_version = StringProperty('')
    lz_ready = BooleanProperty(False)
    lz_up_to_date = BooleanProperty(False)
    lz_status = StringProperty('loading')
    lz_generating_move = BooleanProperty(False)

    lz_analysis = ListProperty([])

    lz_winrates_flat = ListProperty([])

    selected_variation = ObjectProperty(None, allownone=True)

    current_node_index = NumericProperty(0)
    current_branch_length = NumericProperty(0)

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


class LzVariationDisplay(ColouredButton):
    move = ObjectProperty(None)

    coordinates = StringProperty('')

    def on_move(self, instance, move):
        self.coordinates = move.alphanumeric_coordinates


class LzVariationSelector(GridLayout):

    moves = ListProperty([])
    touch = ObjectProperty(None, allownone=True)
    selected_variation = ObjectProperty(None, allownone=True)

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

        self.set_selected_variation()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.touch = touch
            self.set_selected_variation()

    def on_touch_move(self, touch):
        if touch is self.touch:
            self.set_selected_variation()

    def on_touch_up(self, touch):
        if touch is self.touch:
            self.touch = None
            self.set_selected_variation()

    def set_selected_variation(self):
        """Work out which variation is currently pressed."""
        for child in self.children:
            child.state = 'normal'

        if self.touch is None:
            self.selected_variation = None
            return

        child_index = int((self.touch.x - self.x) / (2 * self.height))

        if child_index < len(self.children):
            child = self.children[-child_index - 1]
            child.state = 'down'
            self.selected_variation = child.move
        else:
            self.selected_variation = None


class LzWinrateGraph(Widget):
    
    current_node_index = NumericProperty(0)
    current_branch_length = NumericProperty(5)

    current_touch = ObjectProperty(None, allownone=True)

    xs = ListProperty([])
    rectangles = ListProperty([])
    colours = ListProperty([])
    current_node_x = NumericProperty(0)
    node_width = NumericProperty(1)

    winrates = ListProperty([])

    def __init__(self, *args, **kwargs):
        super(LzWinrateGraph, self).__init__(*args, **kwargs)

        self.bind(current_branch_length=self.update_xs,
                  width=self.update_xs,
                  pos=self.update_graph_canvas,
                  size=self.update_graph_canvas)

    def update_xs(self, *args):
        if self.current_branch_length > 0:
            dx = self.width / self.current_branch_length
        else:
            dx = self.width
        xs = [(i + 0.5) * dx for i in range(self.current_branch_length)]
        self.xs = xs
        print('xs are', self.xs)

    def on_xs(self, instance, xs):
        self.update_graph_canvas()

    def on_winrates(self, instance, winrates):
        self.update_graph_canvas()

    def update_graph_canvas(self, *args):
        winrates = self.winrates
        if len(winrates) != len(self.xs):
            winrates = [(0.5, 0) for _ in self.xs]

        while len(self.rectangles) < len(self.xs):
            # self.colours has the same length as self.rectangles
            colour = Color()
            self.colours.append(colour)
            self.canvas.add(colour)

            rectangle = Rectangle(pos=(0, 0), size=(10, 10))
            self.rectangles.append(rectangle)
            self.canvas.add(rectangle)


        while len(self.rectangles) > len(self.xs):
            colour = self.colours.pop(-1)
            self.canvas.remove(colour)
            
            rectangle = self.rectangles.pop(-1)
            self.canvas.remove(rectangle)

        if len(self.xs) > 1:
            dx = self.xs[1] - self.xs[0]
        else:
            dx = self.width
        for colour, rectangle, x, winrate in zip(self.colours, self.rectangles, self.xs, winrates):
            winrate, playouts = winrate

            left = int(x - dx / 2.) + 1.0
            right = int(x + dx / 2.)
            width = right - left

            if playouts == 0:
                colour.rgba = (0.5, 0.5, 0.5, 1)
                rectangle.size = (width, self.height)
                rectangle.pos = (left, self.y)
            else:
                colour.rgba = (1, 1, 1, 1)
                rectangle.size = (width, winrate * self.height)
                rectangle.pos = (left, self.y)


            
    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        self.current_touch = touch
        self.set_current_node_index_from_touch(touch)

    def on_touch_move(self, touch):
        if not touch is self.current_touch:
            return
        if not self.collide_point(*touch.pos):
            return

        self.set_current_node_index_from_touch(touch)

    def set_current_node_index_from_touch(self, touch):
        x, y = touch.pos

        ratio = (x - self.x) / self.width
        ratio = max(ratio, 0)
        ratio = min(ratio, 1)

        index = int((self.current_branch_length) * ratio)

        self.current_node_index = index
