import pexpect
from functools import wraps
import threading

import kivy

from os import path
if kivy.platform == 'android':
    leelaz_binary = 'leelaz_binary_android'
else:
    leelaz_binary = 'leelaz_binary'

assert path.exists(leelaz_binary)
print('Found LZ binary {}'.format(leelaz_binary))

import os
import stat
st = os.stat(leelaz_binary)
print('current stat is', st)
os.chmod(leelaz_binary, st.st_mode | stat.S_IEXEC | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
os.chmod(leelaz_binary, 33261)

os.environ['LD_LIBRARY_PATH'] = path.abspath('./')


class LeelaZeroWrapper(object):

    def __init__(self):
        self.pondering = False
        self.process = None

        self.current_analysis = []

        # LZ data to be read from the process
        self.lz_name = None
        self.lz_version = None
        self.lz_output = []  # list of output lines
        self.lz_up_to_date = True

        self.command_number = 1
        self.command_queue = []
        self.commands_awaiting_response = {}

        self.connect_to_leela_zero()

        self.begin_reading()

    def begin_reading(self):
        self.read_thread = threading.Thread(
            target=self.read,
            name='lz-thread')

        self.read_thread.start()

    def send_command(self, command):
        """Add a command to the queue, it will not be sent to LZ immediately."""
        self.command_queue.append(command)

        # If not already waiting for something, send the new command
        if self.lz_up_to_date:
            self.send_command_from_queue()

    def send_command_from_queue(self):
        """Pop the first command from the queue, and send it to LZ."""
        if not self.command_queue:
            return

        while True:
            command = self.command_queue.pop(0)
            print(command, command.startswith('lz-analyze'))
            if command.startswith('lz-analyze') and any([c.startswith('lz-analyze') for c in self.command_queue]):
                # skip this command, it is redundant
                continue
            break
        print('command is "{}", remaining queue "{}"'.format(command, self.command_queue))
        self.send_command_to_leelaz(command)
        
    def send_command_to_leelaz(self, command):
        """Send a command to the LZ process, tagged with a number so we can get its output."""
        command_string = '{number} {command}'.format(number=self.command_number,
                                                     command=command)
        self.commands_awaiting_response[self.command_number] = command
        self.command_number += 1

        self.lz_up_to_date = False

        self.process.sendline(command_string)
        print('Sent command "{}", currently alive {}'.format(command_string, self.process.isalive()))

    def read(self):
        while True:
            if not self.process.isalive():
                print('LZ process is not alive, stopping read')
                print('Remaining lines to read were:')
                for line in self.process.readlines():
                    print('  ' + line.decode('utf-8'))
                break  # if the LZ process ended, stop reading from it

            line = self.process.readline()
            self.parse_line(line.decode('utf-8'))

    def parse_line(self, line):
        """Read and interpret a line of output from the LZ process"""
        print('Received line: "{}"'.format(line.strip()))

        if line.startswith('info'):
            self.parse_lz_analysis(line)

        elif ' -> ' in line:
            # parse best move info
            pass

        elif line.startswith('play'):
            # interpret an LZ move
            pass

        elif line.startswith('=') or line.startswith('?'):
            # this line is a response to a command we sent
            # line has the format "=$NUM $RESPONSE"
            number = int(line.strip().split(' ')[0][1:])

            if len(line.strip().split(' ')) == 1:
                response = ''
            else:
                response = ' '.join(line.strip().split(' ')[1:])

            # we are ready to send the next command
            self.send_command_from_queue()

            self.handle_command_response(number, response)

        # also add the line to our log
        if line.strip():
            self.lz_output.append(line.strip())
        
    def parse_lz_analysis(self, line):
        moves = line.split('info')
        moves = [m.strip() for m in moves][1:]

        self.current_analysis = [self.parse_lz_analysis_move(m) for m in moves]

        # Add relative values to the analysis
        max_visits = max([move.visits for move in self.current_analysis])
        for move in self.current_analysis:
            move.relative_visits = move.visits / max_visits

    def parse_lz_analysis_move(self, move):
        return MoveAnalysis(move)

    def handle_command_response(self, number, response):
        command = self.commands_awaiting_response.pop(number)

        print('# command "{}" received response "{}"'.format(command, response))
        
        if command.startswith('lz-analyze'):
            self.pondering = True
            self.current_analysis = []
        else:
            self.pondering = False
        if command == 'version':
            self.lz_version = response
        elif command == 'name':
            self.lz_name = response
        else:
            print('Nothing to do with response "{}" to command "{}"'.format(response, command))

        if number == (self.command_number - 1):
            self.lz_up_to_date = True
        else:
            self.lz_up_to_date = False

    def is_ready(self):
        """Returns True if the LZ process is alive, and has finished initialising."""
        return self.process.isalive() and all([self.lz_name is not None,
                                               self.lz_version is not None])

    def play_move(self, colour, coordinates):
        assert colour in ('black', 'white')

        colour_string = {'black': 'B', 'white': 'W'}[colour]

        self.send_command('play {colour} {coordinates}'.format(
            colour=colour_string,
            coordinates=coordinates))

        if self.pondering:
            self.send_command('lz-analyze 25')

        self.current_analysis = []

    def undo_move(self):
        self.send_command('undo')

        if self.pondering:
            self.send_command('lz-analyze 25')

        self.current_analysis = []

    def toggle_ponder(self, active):
        if not active and self.pondering:
            self.send_command('name')  # sending a command cancels the pondering

        elif active and not self.pondering:
            self.send_command('lz-analyze 25')

    def connect_to_leela_zero(self):
        if self.process is not None:
            return

        print('ready to connect to LZ')
        self.process = pexpect.spawn(
            './{} --gtp --lagbuffer 0 --weights network.gz'.format(leelaz_binary),
            timeout=None)
        print('self.process is {}, alive {}'.format(self.process, self.process.isalive()))
        assert self.process.isalive()

        self.send_command('name')
        self.send_command('version')

    def kill(self):
        self.process.kill(9)


class MoveAnalysis(dict):
    def __init__(self, move):
        move_info = self
        words = move.split(' ')

        word = words.pop(0)
        assert word == 'move'

        word = words.pop(0)
        self.lz_coordinates = word

        word = words.pop(0)
        assert word == 'visits'

        word = words.pop(0)
        self.visits = int(word)

        word = words.pop(0)
        assert word == 'winrate'

        word = words.pop(0)
        self.winrate = float(word) / 100.0

        self.relative_visits = 0  # must be set elsewhere

    @property
    def is_pass(self):
        return self.lz_coordinates == 'pass'

    @property
    def numeric_coordinates(self):
        if self.is_pass:
            return None

        letter = self.lz_coordinates[0]
        number = self.lz_coordinates[1:]

        assert ord('A') <= ord(letter) <= ord('Z')
        horiz_coord = ord(letter) - ord('A')
        if horiz_coord > 8:
            horiz_coord -= 1  # correct for absence of I from coordinates
        vert_coord = int(number)
        vert_coord -= 1  # convert from 1-indexed to 0-indexed

        return (horiz_coord, vert_coord)
