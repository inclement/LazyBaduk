from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty, AliasProperty, StringProperty, DictProperty, BooleanProperty, StringProperty, OptionProperty


def get_stone_image_location(colour):
    print('@@@@@@@@@@')
    print('called get_stone_image_location', colour)
    try:
        stone_type = App.get_running_app().stone_type
    except IOError:
        stone_type = 'default'

    # limiting_size = min(screen_size)
    # stone_limiting_size = int(limiting_size/19.)
    # if stone_limiting_size < 40:
    #     size = '40'
    # elif stone_limiting_size < 60:
    #     stone = '60'
    # elif stone_limiting_size < 80:
    #     stone = '80'
    # else:
    #     stone = '100'

    if colour == 'black':
        if stone_type == 'slate and shell':
            source = 'black_shell_100.png'
        else:
            source = 'black_simple_100.png'
    elif colour == 'white':
        if stone_type == 'slate and shell':
            source = 'white_shell_100.png'
        else:
            source = 'white_simple_100.png'
    print('...and returned', source)
    return './media/stones/' + source


class WhiteStoneDrawn(Widget):
    colour = StringProperty('white')
    stone_image = StringProperty('./media/stones/white_simple_100.png')


class BlackStoneDrawn(Widget):
    colour = StringProperty('black')
    stone_image = StringProperty('./media/stones/white_simple_100.png')


class WhiteStoneStylised(Widget):
    colour = StringProperty('white')
    stone_image = StringProperty('./media/stones/white_stylised_100.png')


class BlackStoneStylised(Widget):
    colour = StringProperty('black')
    stone_image = StringProperty('./media/stones/white_stylised_100.png')


class WhiteStoneSimple(Widget):
    colour = StringProperty('white')
    stone_image = StringProperty('./media/stones/white_simple_100.png')


class BlackStoneSimple(Widget):
    colour = StringProperty('black')
    stone_image = StringProperty('./media/stones/black_shell_100.png')


from random import choice


class WhiteStoneShell(Widget):
    colour = StringProperty('white')
    stone_image = StringProperty('./media/stones/white_shell_100.png')

    def __init__(self, *args, **kwargs):
        super(WhiteStoneShell, self).__init__(*args, **kwargs)
        self.stone_image = choice([
            './media/stones/white_shell_100.png',
            './media/stones/white_shell_100_2.png',
            './media/stones/white_shell_100_3.png',
            './media/stones/white_shell_100_4.png',
            './media/stones/white_shell_100_5.png',
        ])


class WhiteStoneBorderedShell(Widget):
    colour = StringProperty('white')
    stone_image = StringProperty(
        './media/stones/white_borderedshell_100_2.png')


class BlackStoneBorderedShell(Widget):
    colour = StringProperty('black')
    stone_image = StringProperty('./media/stones/black_borderedshell_100.png')


class BlackStoneShell(Widget):
    colour = StringProperty('black')
    stone_image = StringProperty('./media/stones/black_shell_100.png')


class Stone(Widget):
    colour = StringProperty('black')
    stone_image = StringProperty('./media/stones/black_simple_100.png')
    # def __init__(self,*args,**kwargs):
    #     print '""""""""'
    #     print 'Stone inited',self
    #     print args,kwargs
    #     if 'stone_image' in kwargs:
    #         self.stone_image = kwargs['stone_image']
    #     super(Stone,self).__init__(*args,**kwargs)
    #     print 'and now',self.colour,self.stone_image
    # def on_stone_image(self,*args,**kwargs):
    #     print '%%%%%%%%%%%%%'
    #     print 'stone at',self
    #     print 'stone_image set to',self.stone_image
    #     self.canvas.ask_update()
    # def set_colour(self,colour):
    #     print
    #     print 'asked to set colour',colour
    #     self.colour = colour
    #     self.stone_image = get_stone_image_location(colour)
    #     print 'stone_image',self.stone_image


class KoMarker(Widget):
    markercolour = ListProperty([0, 0, 0])
    pass


class TriangleMarker(Widget):
    markercolour = ListProperty([0, 0, 0])
    pass


class SquareMarker(Widget):
    markercolour = ListProperty([0, 0, 0])


class CircleMarker(Widget):
    markercolour = ListProperty([0, 0, 0])


class CrossMarker(Widget):
    markercolour = ListProperty([0, 0, 0])


class TextMarker(Widget):
    markercolour = ListProperty([0, 0, 0])
    text = StringProperty('')

    def printinfo(self):
        print('##############')
        print(self.markercolour)
        print(self.text)
        print(self.pos)
        print(self.size)
        return 0.7


class VarStone(Widget):
    colour = ListProperty([1, 1, 1, 0.5])
    textcolour = ListProperty([0, 0, 0.5])
    text = StringProperty('')

    def set_colour(self, colour):
        if colour in ['black', 'b']:
            self.colour = [0, 0, 0, 1]
            self.textcolour = [1, 1, 1, 1]
        elif colour in ['white', 'w']:
            self.colour = [1, 1, 1, 1]
            self.textcolour = [0, 0, 0, 1]
        else:
            print('colour doesn\'t exist:', colour)
            # should raise exception
