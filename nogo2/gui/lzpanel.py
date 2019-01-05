from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (StringProperty, BooleanProperty, ObjectProperty,
                             ListProperty)

class LzInfoPanel(BoxLayout):
    lz_name = StringProperty('')
    lz_version = StringProperty('')
    lz_ready = BooleanProperty(False)

    lz_analysis = ListProperty([])

    board = ObjectProperty(None)

    def analysis_string(self, lz_analysis):
        return ', '.join(['{} {} {}'.format(move['coordinates'],
                                            move['visits'],
                                            move['winrate'])
                          for move in lz_analysis])
