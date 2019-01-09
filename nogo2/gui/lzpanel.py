from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
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
    coordinates = StringProperty('A1')
    visits = NumericProperty(0)
    winrate = NumericProperty(50.0)
    relative_visits = NumericProperty(0)

    bg_colour = ListProperty([1, 1, 1, 1])

    border_colour = ListProperty([0.5, 0.5, 0.5, 0.5])
    
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
