'''
Provides the AbstractBoard class, which keeps track of an sgf game
and logical board and returns the moves made whilst moving through the
game tree.

'''

import sys

from gomill import sgf, boards, ascii_boards
from random import randint

adjacencies = [(-1, 0), (0, -1), (1, 0), (0, 1)]


class ScoreBoard(object):
    def __init__(self, size=19):
        self.scoringboard = boards.Board(size)
        self.board = [[[] for j in range(size)] for i in range(size)]
        self.size = size

    def set_board(self, arr):
        self.board.board = arr

    def get_score(self):
        self.scoringboard.board = self.remove_dead()
        print(ascii_boards.render_board(self.scoringboard))
        return self.scoringboard.area_score()

    def toggle_status_at(self, coord):
        cur = self.board[coord[0]][coord[1]]
        if cur == 'w':
            self.board[coord[0]][coord[1]] = 'dw'
        elif cur == 'b':
            self.board[coord[0]][coord[1]] = 'db'
        elif cur == 'dw':
            self.board[coord[0]][coord[1]] = 'w'
        elif cur == 'db':
            self.board[coord[0]][coord[1]] = 'b'
        if cur in ['b', 'w']:
            changed = self.propagate_dead()
        elif cur in ['db', 'dw']:
            changed = self.propagate_alive()
        elif cur is None:
            return ([], self.get_score())
        return (set(changed + [coord]), self.get_score())

    def propagate_dead(self):
        board = self.board
        changing = True
        toggled = []
        while changing:
            changing = False
            for x in range(self.size):
                for y in range(self.size):
                    cur = board[x][y]
                    for dx, dy in adjacencies:
                        if x + dx >= 0 and y + dy >= 0 and x + dx < self.size and y + dy < self.size and dx != dy:
                            adj = board[x + dx][y + dy]
                            if cur == 'b' and adj == 'db':
                                board[x][y] = 'db'
                                changing = True
                                toggled.append((x, y))
                            elif cur == 'w' and adj == 'dw':
                                board[x][y] = 'dw'
                                changing = True
                                toggled.append((x, y))
                            elif cur == 'db' and adj == 'b':
                                board[x + dx][y + dy] = 'db'
                                changing = True
                                toggled.append((x + dx, y + dy))
                            elif cur == 'dw' and adj == 'w':
                                board[x + dx][y + dy] = 'dw'
                                changing = True
                                toggled.append((x + dx, y + dy))
        return toggled

    def propagate_alive(self):
        board = self.board
        changing = True
        toggled = []
        while changing:
            changing = False
            for x in range(self.size):
                for y in range(self.size):
                    cur = board[x][y]
                    for dx, dy in adjacencies:
                        if x + dx >= 0 and y + dy >= 0 and x + dx < self.size and y + dy < self.size and dx != dy:
                            adj = board[x + dx][y + dy]
                            if cur == 'b' and adj == 'db':
                                board[x + dx][y + dy] = 'b'
                                changing = True
                                toggled.append((x + dx, y + dy))
                            elif cur == 'w' and adj == 'dw':
                                board[x + dx][y + dy] = 'w'
                                changing = True
                                toggled.append((x + dx, y + dy))
                            elif cur == 'db' and adj == 'b':
                                board[x][y] = 'b'
                                changing = True
                                toggled.append((x, y))
                            elif cur == 'dw' and adj == 'w':
                                board[x][y] = 'w'
                                changing = True
                                toggled.append((x, y))
        return toggled

    def remove_dead(self):
        board = self.board
        size = self.size
        newboard = [[[] for j in range(size)] for i in range(size)]
        for x in range(size):
            for y in range(size):
                cur = board[x][y]
                if cur == 'b':
                    newboard[x][y] = 'b'
                elif cur == 'w':
                    newboard[x][y] = 'w'
                else:
                    newboard[x][y] = None
        return newboard


'''        
def apply_gameinfo_to_sgfmodel(model, info, save=False):
    for key, value in info.iteritems():
        if hasattr(model, key):
            setattr(model, key, value)
    if save:
        model.save(
        '''


def get_sgf_from_file(filen):
    fileh = open(filen)
    string = fileh.read()
    game = sgf.Sgf_game.from_string(string)
    return game


def argsconverter_get_gameinfo_from_file(row_index, filen):
    info = get_gameinfo_from_file(filen)
    info['filen'] = filen
    info['size_hint'] = (1., None)
    info['height'] = (70, 'sp')
    return info


def get_gameinfo_from_file(filen):
    try:
        info = get_gameinfo_from_sgf(get_sgf_from_file(filen))
    except:
        print('Something went wrong with', filen)
        info = {'wname': '[color=ff0000]ERROR[/color] reading file'}
    info['filepath'] = filen
    return info


def set_gameinfo_in_sgf(info, game):
    root = game.get_root()
    if 'bname' in info:
        bname = info['bname']
        root.set('PB', bname)
    if 'wname' in info:
        wname = info['wname']
        root.set('PW', wname)
    if 'annotate' in info:
        annotate = info['annotate']
        root.set('AN', annotate)
    if 'brank' in info:
        brank = info['brank']
        root.set('BR', brank)
    if 'wrank' in info:
        wrank = info['wrank']
        root.set('WR', wrank)
    if 'bteam' in info:
        bteam = info['bteam']
        root.set('BT', bteam)
    if 'wteam' in info:
        wteam = info['wteam']
        root.set('WT', wteam)
    if 'copyright' in info:
        copyright = info['copyright']
        root.set('CP', copyright)
    if 'date' in info:
        date = info['date']
        root.set('DT', date)
    if 'event' in info:
        event = info['event']
        root.set('EV', event)
    if 'gname' in info:
        gname = info['gname']
        root.set('GN', gname)
    if 'gamecomment' in info:
        gamecomment = info['gamecomment']
        root.set('GC', gamecomment)
    if 'overtime' in info:
        overtime = info['overtime']
        root.set('OT', overtime)
    if 'result' in info:
        result = info['result']
        root.set('RE', result)
    if 'rules' in info:
        rules = info['rules']
        root.set('RU', rules)
    if 'source' in info:
        source = info['source']
        root.set('SO', source)
    if 'timelim' in info:
        timelim = info['timelim']
        root.set('TM', timelim)
    if 'user' in info:
        user = info['user']
        root.set('US', user)
    if 'komi' in info:
        komi = info['komi']
        root.set('KM', komi)
    if 'handicap' in info:
        handicap = info['handicap']
        root.set('HA', handicap)


def get_result_from_sgf(game):
    rootnode = game.get_root()
    props = rootnode.properties()
    if 'RE' in props:
        result = rootnode.find_property('RE')
        return result
    return ''


def get_gameinfo_from_sgf(game):
    info = {}
    bname = game.get_player_name('b')
    if bname is not None:
        info['bname'] = bname
    wname = game.get_player_name('w')
    if wname is not None:
        info['wname'] = wname
    komi = game.get_komi()
    if komi is not None:
        info['komi'] = game.get_komi()
    size = game.get_size()
    if size is not None:
        info['gridsize'] = game.get_size()
    handicap = game.get_handicap()
    if handicap is not None:
        info['handicap'] = game.get_handicap()
    rootnode = game.get_root()
    props = rootnode.properties()
    if 'RE' in props:
        info['result'] = rootnode.find_property('RE')
    if 'SO' in props:
        info['source'] = rootnode.find_property('SO')
    if 'BR' in props:
        info['brank'] = rootnode.find_property('BR')
    if 'WR' in props:
        info['wrank'] = rootnode.find_property('WR')
    if 'BT' in props:
        info['bteam'] = rootnode.find_property('BT')
    if 'WT' in props:
        info['wteam'] = rootnode.find_property('WT')
    if 'CP' in props:
        info['copyright'] = rootnode.find_property('CP')
    if 'DT' in props:
        info['date'] = rootnode.find_property('DT')
    if 'EV' in props:
        info['event'] = rootnode.find_property('EV')
    if 'GN' in props:
        info['gname'] = rootnode.find_property('GN')
    if 'GC' in props:
        info['gamecomment'] = rootnode.find_property('GC')
    if 'OT' in props:
        info['overtime'] = rootnode.find_property('OT')
    if 'RU' in props:
        info['rules'] = rootnode.find_property('RU')
    if 'TM' in props:
        try:
            info['timelim'] = rootnode.find_property('TM')
        except:
            pass
    if 'US' in props:
        info['user'] = rootnode.find_property('US')
    return info


def get_markers_from_node(node):
    properties = node.properties()
    instructions = {'marker': []}
    markers = []
    if 'TR' in properties:
        node_markers = node.find_property('TR')
        for marker in node_markers:
            markers.append((marker, 'TR'))
    if 'SQ' in properties:
        node_markers = node.find_property('SQ')
        for marker in node_markers:
            markers.append((marker, 'SQ'))
    if 'CR' in properties:
        node_markers = node.find_property('CR')
        for marker in node_markers:
            markers.append((marker, 'CR'))
    if 'MA' in properties:
        node_markers = node.find_property('MA')
        for marker in node_markers:
            markers.append((marker, 'MA'))
    if 'LB' in properties:
        node_markers = node.find_property('LB')
        for marker in node_markers:
            markers.append((marker[0], 'LB', marker[1]))

    if len(markers) > 0:
        return {'markers': markers}
    else:
        return {}


def get_setupstones_from_node(node):
    black, white, empty = node.get_setup_stones()
    stones = []
    for stone in black:
        stones.append((stone, 'b'))
    for stone in white:
        stones.append((stone, 'w'))
    for stone in empty:
        stones.append((stone, 'e'))
    return stones


def check_variations_in_node(node):
    if node.parent is None:
        return (1, 1)
    else:
        return (node.parent.index(node) + 1, len(node.parent))


def get_variations_from_node(node):
    vars = []
    if node.parent is not None:
        parent = node.parent
        if len(parent) > 1:
            for child in parent:
                if child is not node:
                    childmove = child.get_move()
                    if childmove[0] is not None and childmove[1] is not None:
                        vars.append((childmove[0], childmove[1],
                                     parent.index(child) + 1))
    return vars


def apply_node_to_board(board, node):
    board = board.copy()
    add_stones = []
    remove_stones = []
    empty_stones = []
    add_playmarker = None

    current_occupied_points = board.list_occupied_points()

    # First, find and deal with setup stones
    if node.has_setup_stones():
        print('### Node has setup stones!')
        setup_stones = get_setupstones_from_node(node)
        if len(setup_stones) > 0:
            for stone in setup_stones:
                coords, col = stone
                if col in ['b', 'w']:
                    board.board[coords[0]][coords[1]] = col
                elif col == 'e':
                    board.board[coords[0]][coords[1]] = None

    # Now deal with the actual new move, if any

    new_move_colour, new_move_point = node.get_move()
    if new_move_point is not None:
        try:
            board.play(new_move_point[0], new_move_point[1], new_move_colour)
        except ValueError:
            print('SGF played existing point')
            board.board[new_move_point[0]][new_move_point[1]] = new_move_colour
    new_occupied_points = board.list_occupied_points()
    for point in new_occupied_points:
        if point not in current_occupied_points:
            add_stones.append((point[1], point[0]))
    for point in current_occupied_points:
        if point not in new_occupied_points:
            remove_stones.append((point[1], point[0]))

    instructions = {}
    if len(add_stones) > 0:
        instructions['add'] = add_stones
    if len(remove_stones) > 0:
        instructions['remove'] = remove_stones
    if len(empty_stones) > 0:
        instructions['empty'] = empty_stones

    nonstone_instructions = get_nonstone_from_node(node)
    instructions.update(nonstone_instructions)

    #instructions.update(setup_stones)

    return (board, instructions)


def compare_boards(old, new):
    add_stones = []
    remove_stones = []

    old_stones = old.list_occupied_points()
    new_stones = new.list_occupied_points()
    for point in new_stones:
        if point not in old_stones:
            add_stones.append((point[1], point[0]))
    for point in old_stones:
        if point not in new_stones:
            remove_stones.append((point[1], point[0]))

    instructions = {}
    if len(add_stones) > 0:
        instructions['add'] = add_stones
    if len(remove_stones) > 0:
        instructions['remove'] = remove_stones

    return instructions


def get_nonstone_from_node(node):
    instructions = {}

    node_markers = get_markers_from_node(node)
    instructions.update(node_markers)

    variations = check_variations_in_node(node)
    if variations[1] > 1:
        instructions['variations'] = variations

    new_move_colour, new_move_point = node.get_move()
    if new_move_point is not None:
        add_playmarker = new_move_point
        instructions['playmarker'] = add_playmarker

    comment = get_comment_from_node(node)
    if len(comment) > 0:
        instructions['comment'] = comment

    nextplayer = get_nextplayer_from_node(node)
    instructions['nextplayer'] = nextplayer

    varposs = get_variations_from_node(node)
    if len(varposs) > 0:
        instructions['varpositions'] = varposs

    return instructions


def get_nextplayer_from_node(node):
    if 'PL' in node.properties():
        return node.find_property('PL')
    else:
        props = node.properties()
        if 'W' in props:
            return 'b'
        if 'B' in props:
            return 'w'
        if 'HA' in props:
            return 'w'
        if node.parent is None:
            return 'b'
    return 'a'


def get_comment_from_node(node):
    props = node.properties()
    annotations = []
    judgements = []
    comment = ''
    if 'N' in props:
        annotations.append('Node name: [b]%s[/b]' % node.find_property('N'))
    if 'DM' in props:
        judgements.append('[b]even position[/b]')
    if 'GB' in props:
        judgements.append('[b]good for black[/b]')
    if 'GW' in props:
        judgements.append('[b]good for white[/b]')
    if 'HO' in props:
        judgements.append('[b]hotspot[/b]')
    if 'UC' in props:
        judgements.append('[b]unclear position[/b]')
    if 'BM' in props:
        judgements.append('[b]bad move[/b]')
    if 'DO' in props:
        judgements.append('[b]doubtful move[/b]')
    if 'IT' in props:
        judgements.append('[b]interesting move[/b]')
    if 'TE' in props:
        judgements.append('[b]tesuji[/b]')
    if 'V' in props:
        annotations.append('Value: %d' % node.find_property('V'))
    if 'C' in props:
        comment = node.find_property('C')
    text = ''
    if len(annotations) > 0:
        text = '\n'.join(annotations)
    if len(judgements) > 0:
        text = ''.join((text, 'SGF annotations: ', ', '.join(judgements)))
    if len(comment) > 0:
        if len(text) > 0:
            text = ''.join((text, '\n----------\n', comment))
        else:
            text = comment

    return text


class AbstractBoard(object):
    def __init__(self, game=None, gridsize=19):
        if game is None:
            game = sgf.Sgf_game(gridsize)
        print('abstractboard initialised with size', game.size, gridsize)

        self.game = game
        self.prisoners = [0, 0]
        self.variation_index = 0

        self.boards = {}
        self.curnode = game.get_root()
        board = boards.Board(self.game.size)
        board, instructions = apply_node_to_board(board, self.curnode)
        self.boards[self.curnode] = board
        self.varcache = {}
        self.filepath = ''

    def get_current_boardpos(self):
        curnode = self.curnode
        newboard = [row[:] for row in self.boards[curnode].board]
        return newboard

    def get_reconstruction(self):
        curnode = self.curnode
        variations = []
        node = curnode
        while node.parent is not None:
            variations.append(node.parent.index(node))
            node = node.parent
        return variations[::-1]

    def reconstruct_from(self, vs):
        #self.reset_position()
        node = self.curnode
        print('reconstructing with', vs)
        try:
            for entry in vs:
                print('node is', node, len(node))
                node = node[entry]
                print('new node is', node, len(node))
            instructions = self.jump_to_node(node)
            return instructions
        except IndexError:
            print('Error reading reconstruction index')
            sys.exit()
            return {}

    def load_sgf_from_file(self, filen):
        print('abstractboard asked to load from', filen)
        print('opening file')
        fileh = open(filen, 'r')
        print('opened')
        sgfdata = fileh.read()
        print('read from file')
        print('sgf is', sgfdata)
        fileh.close()
        print('file closed')
        try:
            self.game = sgf.Sgf_game.from_string(sgfdata)
            self.filepath = filen
            print('Successfully parsed string')
        except ValueError:
            print('Failed to parse string')
            self.game = sgf.Sgf_game(19)
        print('loaded from file')
        self.reset_position()
        print('reset position')

    def get_gameinfo(self):
        info = get_gameinfo_from_sgf(self.game)
        if self.filepath != '':
            info['filepath'] = self.filepath
        return info

    def set_gameinfo(self, info):
        if 'filepath' in info:
            self.filepath = info['filepath']
        set_gameinfo_in_sgf(info, self.game)

    def save_sgf(self, filen):
        print(' ABSTRACT SAVING')
        data = self.game.serialise()
        print('data is', data)
        fileh = open(filen, 'w')
        fileh.write(data)
        fileh.close()
        return True

    def load_sgf_from_text(self, sgftext):
        self.game = sgf.Sgf_game.from_string(sgftext)
        self.reset_position()

    def set_sgf(self, sgf):
        self.game = sgf
        self.reset_position()

    def reset_position(self):
        self.curnode = self.game.get_root()
        self.boards = {}
        self.varcache = {}
        board = boards.Board(self.game.size)
        board, instructions = apply_node_to_board(board, self.curnode)
        self.boards[self.curnode] = board
        node_index = self.current_node_index()
        instructions.update({'nodeindex': node_index})
        return instructions

    def jump_to_varbranch(self):
        curnode = self.curnode
        while len(curnode) <= 1 and curnode.parent is not None:
            print('curnode', len(curnode))
            curnode = curnode.parent
        if curnode in self.varcache:
            self.varcache[curnode] = 0
        return self.jump_to_node(curnode)

    def get_previous_move_coord(self):
        if self.curnode.parent is None:
            return None
        move = self.curnode.parent.get_move()
        return move[1]

    def get_current_move_coord(self):
        move = self.curnode.get_move()
        return move[1]

    def advance_position(self, *args, **kwargs):
        print('advance_position called')
        curnode = self.curnode
        curboard = self.boards[curnode]
        if len(curnode) > 0:
            if curnode in self.varcache:
                newnode = self.curnode[self.varcache[curnode]]
            else:
                newnode = self.curnode[0]

        self.curnode = newnode
        newboard = curboard.copy()

        newboard, instructions = apply_node_to_board(newboard, newnode)
        #        instructions = {'add':[((randint(0,18),randint(0,18)),['w','b'][randint(0,1)])],'playmarker': (randint(0,18),randint(0,18)), 'nextplayer': ['w','b'][randint(0,1)]}

        self.boards[newnode] = newboard

        node_index = self.current_node_index()
        instructions.update({'nodeindex': node_index})

        return instructions

    def retreat_position(self, *args, **kwargs):
        curnode = self.curnode
        curboard = self.boards[curnode]
        if curnode.parent is not None:
            newnode = self.curnode.parent
        else:
            return None

        self.curnode = newnode
        if newnode in self.boards:
            newboard = self.boards[newnode]
        else:
            print('Reconstruct board')

        self.boards[newnode] = newboard

        instructions = compare_boards(curboard, newboard)

        nonstone_instructions = get_nonstone_from_node(newnode)
        instructions.update(nonstone_instructions)

        node_index = self.current_node_index()
        instructions.update({'nodeindex': node_index})

        return instructions

    def jump_to_var(self, num):
        if self.curnode.parent is not None:
            parentnode = self.curnode.parent
            newind = num
            if len(parentnode) > newind:
                newnode = parentnode[newind]
                self.varcache[parentnode] = newind
                return self.jump_to_node(newnode)
        else:
            return None

    def increment_variation(self):
        #instructions = {'add':[((randint(0,18),randint(0,18)),['w','b'][randint(0,1)])],'playmarker': (randint(0,18),randint(0,18))}#, 'nextplayer': ['w','b'][randint(0,1)]}
        #return instructions
        if self.curnode.parent is not None:
            parentnode = self.curnode.parent
            newind = (parentnode.index(self.curnode) + 1) % len(parentnode)
            newnode = parentnode[newind]
            self.varcache[parentnode] = newind
            return self.jump_to_node(newnode)
        else:
            return {}

    def decrement_variation(self):
        if self.curnode.parent is not None:
            parentnode = self.curnode.parent
            newind = (parentnode.index(self.curnode) - 1) % len(parentnode)
            newnode = parentnode[newind]
            self.varcache[parentnode] = newind
            return self.jump_to_node(newnode)
        else:
            return {}

    def jump_to_node(self, node):
        #return {'add':[((randint(0,18),randint(0,18)),['w','b'][randint(0,1)])]}
        oldboard = self.boards[self.curnode]
        self.curnode = node
        newboard = self.get_or_build_board(node)
        instructions = compare_boards(oldboard, newboard)
        nonstone_instructions = get_nonstone_from_node(node)
        instructions.update(nonstone_instructions)
        self.build_varcache_to_node(node)

        node_index = self.current_node_index()
        instructions.update({'nodeindex': node_index})

        return instructions

    def get_current_var_tree(self):
        node = self.curnode
        before = []
        while node.parent is not None:
            node = node.parent
            before.append(node)
        before = before[::-1]

        node = self.curnode
        after = []
        while len(node) > 0:
            if node in self.varcache:
                node = node[self.varcache[node]]
            else:
                node = node[0]
            after.append(node)
        return (len(before), before + [self.curnode] + after)

    def current_node_index(self):
        curnode = self.curnode
        index, sequence = self.get_current_var_tree()
        # index = sequence.index(curnode)
        return (index, len(sequence))

    def jump_to_leaf_number(self, number):
        curnode = self.curnode
        index, sequence = self.get_current_var_tree()
        if number < len(sequence):
            node = sequence[number]
            instructions = self.jump_to_node(node)
            return instructions
        else:
            return {}

    def toggle_background_stone(self, coords, colour='b', force='toggle'):
        curnode = self.curnode

        # This if no longer necessary, handled in boardview?
        curmove = curnode.get_move()
        if curmove[0] is not None:
            curnode = self.curnode.new_child()
            instructions = self.jump_to_node(curnode)
        else:
            instructions = {}
        instructions['add'] = []
        instructions['remove'] = []

        curboard = self.boards[self.curnode]

        curstone = curboard.board[coords[0]][coords[1]]
        if curstone == None:
            self.add_add_stone(coords, colour)
            if colour != 'e':
                instructions['add'].append((coords, colour))
        elif curstone == 'b':
            self.remove_add_stone(coords, 'b')
            self.add_add_stone(coords, 'e')
            instructions['remove'].append((coords, 'b'))
        elif curstone == 'w':
            self.remove_add_stone(coords, 'w')
            self.add_add_stone(coords, 'e')
            instructions['remove'].append((coords, 'w'))

        return instructions

    def remove_add_stone(self, coords, colour='b'):
        curnode = self.curnode
        ab, aw, ae = curnode.get_setup_stones()
        curboard = self.boards[self.curnode]
        if colour == 'b':
            if coords in ab:
                ab.remove(coords)
        elif colour == 'w':
            if coords in aw:
                aw.remove(coords)
        else:
            if coords in ae:
                ae.remove(coords)
        curnode.set_setup_stones(ab, aw, ae)
        if curnode.parent is not None:
            self.rebuild_curboard()

    def rebuild_curboard(self):
        if self.curnode in self.boards:
            curboard = self.boards.pop(self.curnode)
        self.build_boards_to_node(self.curnode)

    def add_add_stone(self, coords, colour='b'):
        curnode = self.curnode
        curboard = self.boards[curnode]
        ab, aw, ae = curnode.get_setup_stones()
        if colour == 'b':
            if coords not in ab:
                ab.add(coords)
                #curboard.board[coords[0]][coords[1]] = 'b'
        elif colour == 'w':
            if coords not in aw:
                aw.add(coords)
                #curboard.board[coords[0]][coords[1]] = 'w'
        else:
            if coords not in ae:
                ae.add(coords)
                #curboard.board[coords[0]][coords[1]] = None
        curnode.set_setup_stones(ab, aw, ae)
        if curnode.parent is not None:
            self.rebuild_curboard()

    def clear_markers_at(self, coords):
        node = self.curnode
        properties = node.properties()
        if 'TR' in properties:
            node_markers = node.find_property('TR')
            if coords in node_markers:
                node_markers.remove(coords)
                if node_markers:
                    node.set('TR', node_markers)
                else:
                    node.unset('TR')
        if 'SQ' in properties:
            node_markers = node.find_property('SQ')
            if coords in node_markers:
                node_markers.remove(coords)
                if node_markers:
                    node.set('SQ', node_markers)
                else:
                    node.unset('SQ')
        if 'CR' in properties:
            node_markers = node.find_property('CR')
            if coords in node_markers:
                node_markers.remove(coords)
                if node_markers:
                    node.set('CR', node_markers)
                else:
                    node.unset('CR')
        if 'MA' in properties:
            node_markers = node.find_property('MA')
            if coords in node_markers:
                node_markers.remove(coords)
                if node_markers:
                    node.set('MA', node_markers)
                else:
                    node.unset('MA')

    def add_marker_at(self, mtype, coords):
        node = self.curnode
        properties = node.properties()
        code = None
        if mtype == 'triangle':
            code = 'TR'
        elif mtype == 'square':
            code = 'SQ'
        elif mtype == 'circle':
            code = 'CR'
        elif mtype == 'cross':
            code = 'MA'
        if code is not None:
            if code in properties:
                node_markers = node.find_property(code)
            else:
                node_markers = set()
            node_markers.add(coords)
            node.set(code, node_markers)

    def add_new_node(self,
                     coord,
                     colour,
                     newmainline=False,
                     jump=True,
                     disallowsuicide=False):
        curboard = self.boards[self.curnode]
        if coord is not None:
            if curboard.board[coord[0]][coord[1]] is not None:
                print('Addition denied, stone already exists!')
                return {}
        curnode = self.curnode
        if coord is not None:
            for entry in self.curnode:
                ecolour, ecoord = entry.get_move()
                if ecolour == colour and ecoord[0] == coord[0] and ecoord[
                        1] == coord[1]:
                    return self.jump_to_node(entry)
        if not newmainline:
            newnode = self.curnode.new_child()
        else:
            newnode = self.curnode.new_child(0)
        if coord is not None:
            newnode.set_move(colour, coord)
        #print 'newnode is',newnode
        if jump:
            instructions = self.jump_to_node(newnode)
            instructions.update({'unsaved': True})
            return instructions
        else:
            return {}

    def replace_next_node(self, coord, colour):
        if self.curnode in self.varcache:
            newnode = self.curnode[self.varcache[curnode]]
        else:
            newnode = self.curnode[0]
        newnode.set_move(colour, coord)
        self.recursively_destroy_boards_from(newnode)
        return self.jump_to_node(newnode)

    def insert_before_next_node(self, coord, colour):
        if self.curnode in self.varcache:
            reparentnode = self.curnode[self.varcache[curnode]]
        else:
            reparentnode = self.curnode[0]

        self.add_new_node(coord, colour, jump=False)
        reparentnode.reparent(self.curnode[-1])
        self.recursively_destroy_boards_from(reparentnode)
        return self.jump_to_node(self.curnode[-1])

    def recursively_destroy_boards_from(self, node):
        if node in self.boards:
            deadboard = self.boards.pop(node)
        for child in node:
            self.recursively_destroy_boards_from(child)

    def build_varcache_to_node(self, node, height=1):
        while node.parent is not None and height > 0:
            newnode = node.parent
            if len(newnode) > 1:
                nodeind = newnode.index(node)
                self.varcache[newnode] = nodeind
            node = newnode
            height -= 1

    def get_next_coords(self):
        curnode = self.curnode
        if len(curnode) < 1:
            return (None, None)
        if curnode in self.varcache:
            newnode = curnode[varcache[curnode]]
        else:
            newnode = curnode[0]
        return newnode.get_move()[1]

    def get_or_build_board(self, node):
        if node not in self.boards:
            self.build_boards_to_node(node)
        return self.boards[node]

    def build_boards_to_node(self, node, replace=False):
        #print 'build_boards_to_node called'
        precursor_nodes = self.game.get_sequence_above(node)
        board = boards.Board(self.game.size)
        board, instructions = apply_node_to_board(board, precursor_nodes[0])
        self.boards[precursor_nodes[0]] = board

        for i in range(1, len(precursor_nodes)):
            curnode = precursor_nodes[i]
            if (curnode not in self.boards) or replace:
                board, instructions = apply_node_to_board(board, curnode)
                self.boards[curnode] = board
            else:
                board = self.boards[curnode]

        curnode = node
        board, instructions = apply_node_to_board(board, node)
        self.boards[node] = board

    def get_result(self):
        return get_result_from_sgf(self.game)

    def get_player_names(self):
        wname = self.game.get_player_name('w')
        bname = self.game.get_player_name('b')
        if wname is not None:
            wname = ''.join(wname.splitlines())
        else:
            wname = 'Unknown'
        if bname is not None:
            bname = ''.join(bname.splitlines())
        else:
            bname = 'Unknown'
        return (wname, bname)

    def get_player_ranks(self):
        try:
            wrank = self.game.root.find_property('WR')
        except KeyError:
            wrank = None
        try:
            brank = self.game.root.find_property('BR')
        except KeyError:
            brank = None
        if wrank is not None:
            wrank = '(' + ''.join(wrank.splitlines()) + ')'
        else:
            wrank = ''
        if brank is not None:
            brank = '(' + ''.join(brank.splitlines()) + ')'
        else:
            brank = ''
        return (wrank, brank)

    def do_children_exist(self):
        if len(self.curnode) > 0:
            return True
        else:
            return False
