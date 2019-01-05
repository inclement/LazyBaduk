import pexpect
from functools import wraps
import threading

def assert_connected(func):
    @wraps(func)
    def new_func(self, *args, **kwargs):
        assert self.process is not None, "Can't call func as Leela Zero connection not open"
        assert self.process.isalive()
        return func(self, *args, **kwargs)
    return new_func

def assert_not_pondering(func):
    @wraps(func)
    def new_func(self, *args, **kwargs):
        assert not self.pondering
        return func(self, *args, **kwargs)
    return new_func

class LeelaZeroWrapper(object):

    def __init__(self):
        self.pondering = False
        self.process = None

        # LZ data to be read from the process
        self.lz_name = None
        self.lz_version = None
        self.lz_output = []  # list of output lines

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
        self.send_command_from_queue()

    def send_command_from_queue(self):
        """Pop the first command from the queue, and send it to LZ."""
        if not self.command_queue:
            return
        command = self.command_queue.pop(0)
        self.send_command_to_leelaz(command)
        
    def send_command_to_leelaz(self, command):
        """Send a command to the LZ process, tagged with a number so we can get its output."""
        command_string = '{number} {command}'.format(number=self.command_number,
                                                     command=command)
        self.commands_awaiting_response[self.command_number] = command
        self.command_number += 1

        self.process.sendline(command_string)
        print('Sent command "{}"'.format(command_string))

    def read(self):
        while True:
            if not self.process.isalive():
                break  # if the LZ process ended, stop reading from it

            line = self.process.readline()
            self.parse_line(line.decode('utf-8'))

    def parse_line(self, line):
        """Read and interpret a line of output from the LZ process"""
        print('Received line: "{}"'.format(line.strip()))

        if line.startswith('info'):
            # parse analysis
            pass

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

    def handle_command_response(self, number, response):
        command = self.commands_awaiting_response.pop(number)

        print('# command "{}" received response "{}"'.format(command, response))
        
        if command.startswith('lz-analyze'):
            self.pondering = True
        else:
            self.pondering = False
        if command == 'version':
            self.lz_version = response
        elif command == 'name':
            self.lz_name = response
        else:
            print('Nothing to do with response "{}" to command "{}"'.format(response, command))

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

    def toggle_ponder(self, active):
        if not active and self.pondering:
            self.send_command('name')  # sending a command cancels the pondering

        elif active and not self.pondering:
            self.send_command('lz-analyze 10')

    def connect_to_leela_zero(self):
        if self.process is not None:
            return

        self.process = pexpect.spawn('./leelaz_binary --gtp --lagbuffer 0 --weights network.gz',
                                     timeout=None)
        assert self.process.isalive()

        self.send_command('name')
        self.send_command('version')

    def kill(self):
        self.process.kill(9)
        
