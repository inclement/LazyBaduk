#!/usr/bin/env python2

# Copyright 2013 Alexander Taylor

# This file is part of noGo.

# noGo is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# noGo is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with noGo. If not, see http://www.gnu.org/licenses/gpl-3.0.txt

from kombilo.kombiloNG import KEngine, Pattern
import kombilo.kombiloNG as kng
import os

class KombiloInterface(KEngine):
    def load_databases(self):
        for folder in os.listdir('./kombilo_databases'):
            print(folder)
            sgfpath = '/home/asandy/Go/Database/' + folder + '/'
            folder = './kombilo_databases/' + folder + '/'
            print(sgfpath, folder)
            self.gamelist.DBlist.append({'sgfpath': sgfpath,
                                         'name': (folder, 'kombilo1'),
                                         'data': None,
                                         'disabled': 0})
        self.loadDBs()

    def search_pattern(self, code, pos, shape):
        print('changed', pos, 'to', side_name_to_ptype(pos))
        p = Pattern(code, ptype=side_name_to_ptype(pos), sizeX=shape[0], sizeY=shape[1])
        self.patternSearch(p)
        details = self.patternSearchDetails()
        print(details)
        self.gamelist.reset()
        print('\nand continuations are...\n\n')
        print(self.continuations)
        return details

def side_name_to_ptype(name):
    return eval('kng.' + name)
    
