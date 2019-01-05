from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (StringProperty, BooleanProperty, ObjectProperty)

class LzInfoPanel(BoxLayout):
    lz_name = StringProperty('')
    lz_version = StringProperty('')
    lz_ready = BooleanProperty(False)

    board = ObjectProperty(None)
