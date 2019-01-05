from kivy.properties import (NumericProperty, ReferenceListProperty,
                             ObjectProperty, ListProperty, AliasProperty,
                             StringProperty, DictProperty, BooleanProperty,
                             StringProperty, OptionProperty)
from gui.boardwidgets import (
    Stone, TextMarker, TriangleMarker, SquareMarker, CircleMarker, CrossMarker,
    VarStone, get_stone_image_location, BlackStoneSimple, WhiteStoneSimple,
    BlackStoneShell, WhiteStoneShell, BlackStoneDrawn, WhiteStoneDrawn,
    WhiteStoneBorderedShell, BlackStoneBorderedShell, WhiteStoneStylised,
    BlackStoneStylised)

from kivy.app import App


def get_stone(colour):
    stone_type = App.get_running_app().stone_type
    if colour == 'white':
        if stone_type == 'slate and shell':
            return WhiteStoneShell()
        elif stone_type == 'bordered slate and shell':
            return WhiteStoneBorderedShell()
        elif stone_type == 'stylised':
            return WhiteStoneStylised()
        elif stone_type == 'simple':
            return WhiteStoneSimple()
        else:
            return WhiteStoneDrawn()
    else:
        if stone_type == 'slate and shell':
            return BlackStoneShell()
        elif stone_type == 'bordered slate and shell':
            return BlackStoneBorderedShell()
        elif stone_type == 'stylised':
            return BlackStoneStylised()
        elif stone_type == 'simple':
            return BlackStoneSimple()
        else:
            return BlackStoneDrawn()


class WidgetCache(object):
    # Cached board widgets
    blackstonecache = []
    whitestonecache = []
    labelcache = {}
    varstonecache = []
    shapecache = {}

    def get_black_stone(self, size=(0, 0), pos=(0, 0)):
        bsc = self.blackstonecache
        if len(bsc) > 0:
            stone = bsc.pop(0)
        else:
            stone = get_stone('black')
            #stone.set_colour('black')
        return stone

    def cache_black_stone(self, stone):
        self.blackstonecache.append(stone)

    def get_white_stone(self, size=(0, 0), pos=(0, 0)):
        wsc = self.whitestonecache
        if len(wsc) > 0:
            stone = wsc.pop(0)
        else:
            stone = get_stone('white')
            #stone.set_colour('white')
        return stone

    def cache_white_stone(self, stone):
        self.whitestonecache.append(stone)

    def get_stone(self, colour='b'):
        if colour == 'b':
            return self.get_black_stone()
        elif colour == 'w':
            return self.get_white_stone()
        else:
            print('asked for stone colour that doesn\'t exist')

    def cache_stone(self, stone, colour):
        if colour in ['b', 'black']:
            self.cache_black_stone(stone)
        elif colour in ['w', 'white']:
            self.cache_white_stone(stone)
        else:
            print('asked to cache stone colour that doesn\'t exist', stone,
                  colour)

    def purge_stone_cache(self):
        self.blackstonecache = []
        self.whitestonecache = []

    def get_label(self, text):
        lc = self.labelcache
        if text in lc:
            #print 'Already have such a label!'
            labels = lc[text]
            label = labels.pop(0)
            #print 'got',label,'from',labels
            if len(labels) == 0:
                lc.pop(text)
            return label
        # if len(lc) > 0:
        #     alttext = lc.keys()[0]
        #     labels = lc[alttext]
        #     label = labels.pop(0)
        #     if len(labels)==0:
        #         lc.pop(alttext)
        #     label.text = text
        #     return label
        label = TextMarker(text=text)
        return label

    def cache_label(self, label):
        text = label.text
        lc = self.labelcache
        if text not in lc:
            lc[text] = []
        lc[text].append(label)

    def get_var_stone(self):
        vsc = self.varstonecache
        if len(vsc) > 0:
            varstone = vsc.pop(0)
        else:
            varstone = VarStone()
        return varstone

    def cache_var_stone(self, varstone):
        self.varstonecache.append(varstone)

    def get_shape_marker(self, shape):
        sc = self.shapecache
        print('asked for shape marker', shape, sc)
        if shape in sc:
            markers = sc[shape]
            marker = markers.pop(0)
            if len(markers) == 0:
                sc.pop(shape)
            return marker

        if shape == 'triangle':
            return TriangleMarker()
        elif shape == 'square':
            return SquareMarker()
        elif shape == 'circle':
            return CircleMarker()
        elif shape == 'cross':
            return CrossMarker()

    def cache_shape_marker(self, marker):
        sc = self.shapecache
        print('asked to cache shape marker', marker, sc)
        if isinstance(marker, TriangleMarker):
            try:
                sc['triangle'].append(marker)
            except KeyError:
                sc['triangle'] = [marker]
        elif isinstance(marker, SquareMarker):
            try:
                sc['square'].append(marker)
            except KeyError:
                sc['square'] = [marker]
        elif isinstance(marker, CrossMarker):
            try:
                sc['cross'].append(marker)
            except KeyError:
                sc['cross'] = [marker]
        elif isinstance(marker, CircleMarker):
            try:
                sc['circle'].append(marker)
            except KeyError:
                sc['circle'] = [marker]

    def cache_marker(self, marker):
        if isinstance(marker, TextMarker):
            self.cache_label(marker)
        else:
            self.cache_shape_marker(marker)
