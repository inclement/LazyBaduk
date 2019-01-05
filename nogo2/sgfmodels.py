'''Peewee ORM models for storing sgf metadata.'''

from peewee import *
import datetime
import time
import json
import random

from os.path import join, realpath, dirname
path = dirname(realpath(__file__))
db = SqliteDatabase(join(path, 'sgfs.db'))
db.connect()


def embolden(s):
    if s[:3] != '[b]':
        s = '[b]' + s + '[/b]'
    return s


class BaseModel(Model):
    class Meta(object):
        database = db


class Collection(BaseModel):
    name = CharField()
    date_created = DateTimeField(default=datetime.datetime.now)
    directory = CharField(default='./games')

    other = TextField(null=True)
    '''Anything else I think of...'''

    def __str__(self, *args):
        return '<{} collection>'.format(self.name)

    def __repr__(self, *args):
        return str(self)

    def random_sgf(self):
        games = get_games_in(self)
        print('games are', games)
        choice = random.choice(games)
        print('choice is', choice)
        if len(games) == 0:
            return None
        else:
            return choice


class Sgf(BaseModel):
    '''Peewee model for storing sgf metadata in a database.'''

    filename = CharField(default='', null=True)

    sgf = TextField(null=True)
    '''The entire sgf.'''

    other = TextField(null=True)
    '''Anything else I think of...'''

    keywords = CharField(null=True)

    def get_keywords(self):
        return json.loads(self.keywords)

    def set_keywords(self, keywords):
        self.keywords = json.dumps(keywords)

    user_rating = IntegerField(null=True)

    user_created = BooleanField(null=True)

    date_created = DateTimeField(default=datetime.datetime.now)

    # Direct sgf properties
    ap = CharField(null=True)
    charset = CharField(null=True)
    fileformat = CharField(null=True)
    gametype = CharField(null=True)
    # Should always be 1 (== Go) for us...
    varshow = CharField(null=True)
    # We ignore this, and I'm not sure anyone uses it anyway
    gridsize = IntegerField(null=True)
    annotater = CharField(null=True)
    brank = CharField(null=True)
    bteam = CharField(null=True)
    copyright = CharField(null=True)
    date = CharField(default=lambda: str(datetime.date.today()), null=True)
    event = CharField(null=True)

    gname = CharField(null=True)
    gamecomment = CharField(null=True)
    opening = CharField(null=True)
    overtime = CharField(null=True)
    bname = CharField(null=True)
    place = CharField(null=True)
    wname = CharField(null=True)
    result = CharField(null=True)
    round = CharField(null=True)
    rules = CharField(null=True)
    source = CharField(null=True)
    timelim = CharField(null=True)
    user = CharField(null=True)
    wrank = CharField(null=True)
    wteam = CharField(null=True)
    handicap = CharField(null=True)
    komi = CharField(null=True)
    bterritory = CharField(null=True)
    # Or area, depending on rules
    wterritory = CharField(null=True)

    # Or area, depending on rules

    # def __init__(self, *args, **kwargs):
    #     super(Sgf, self).__init__(*args, **kwargs)

    def get_collections(self, *args):
        return list(Collection.select().join(CollectionSgf).join(Sgf).where(
            Sgf.id == self.id))

    def auto_filename(self):
        collections = self.get_collections()
        if len(collections) > 0:
            directory = collections[0].directory
        else:
            directory = './games'
        filen = directory + '/' + time.asctime().replace(' ', '_')
        if self.wname:
            filen += '_' + self.wname
        if self.bname:
            filen += '_' + self.bname
        if self.event:
            filen += '_' + self.event
        filen += '.sgf'
        self.filename = filen
        return self.filename

    def populate_from_gameinfo(self, info):
        print('populating sgf from gameinfo')
        for key, value in info.items():
            print(key, value, hasattr(self, key))
            if hasattr(self, key):
                setattr(self, key, value)

        self.save()
        print('populated self from gameinfo')
        print('size is', self.gridsize)
        print('wname is', self.wname)


class CollectionSgf(BaseModel):
    collection = ForeignKeyField(Collection)
    sgf = ForeignKeyField(Sgf)

    def __str__(self):
        return '<CollectionSgf {} in {}>'.format(self.sgf, self.collection)

    def __repr__(self):
        return str(self)


def get_collections():
    return list(Collection.select().order_by(Collection.date_created))[::-1]


def collections_args_converter(ri, col):
    games = list(Sgf.select().join(CollectionSgf).join(Collection).where(
        Collection.name == col.name))
    return {'colname': col.name, 'numentries': len(games), 'collection': col}


def get_games_in(collection):
    games = list(Sgf.select().join(CollectionSgf).join(Collection).where(
        Collection.name == collection.name))
    return games


def games_args_converter(ri, game):
    info = {}
    info['sgf'] = game

    collection_list = list(Collection.select().join(CollectionSgf).join(Sgf)
                           .where(Sgf.id == game.id))
    if len(collection_list) > 0:
        info['collection'] = collection_list[0]

    if game.filename:
        info['filepath'] = game.filename
    if game.result:
        info['result'] = game.result
        winner = game.result[0].lower()
    else:
        winner = ''
    if game.wname:
        info['wname'] = game.wname
        if winner == 'w':
            info['wname'] = embolden(info['wname'])
    else:
        info['wname'] = 'unknown'
    if game.bname:
        info['bname'] = game.bname
        if winner == 'b':
            info['bname'] = embolden(info['bname'])
    else:
        info['bname'] = 'unknown'
    if game.date:
        info['date'] = game.date
    if hasattr(game, 'boardname'):
        info['boardname'] = game.boardname

    return info


def get_default_collection():
    collections = list(Collection.select().where(Collection.name == 'unsaved'))
    if len(collections) == 0:
        collection = Collection(name='unsaved')
        collection.save()
    else:
        collection = collections[0]
    return collection


def delete_collection_from(selection):
    if len(selection) == 0:
        return False
    selection[0].collection.delete_instance()
