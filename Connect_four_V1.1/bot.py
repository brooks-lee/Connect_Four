import ConnectFour
from sys import stdin, stdout
import random
import time


class Bot(object):

    settings = dict()
    round = -1
    board = [[0]*7]*6#np.zeros((6, 7), dtype=np.uint8)  # Access with [row_nr, col_nr]. [0,0] is on the top left.
    timeout = -1

    def make_turn(self):
        """ This method is for calculating and executing the next play.
            Make the play by calling place_disc exactly once.
        """
        raise NotImplementedError()

    def place_disc(self, column):
        """ Writes your next play in stdout. """
        stdout.write("place_disc %d\n" % column)
        stdout.flush()

    def simulate_place_disc(self, board, col_nr, curr_player):
        """ Returns a board state after curr_player placed a disc in col_nr.
            This is a simulation and doesn't update the actual playing board. """
        if board[0, col_nr] != 0:
            raise Bot.ColumnFullException()
        new_board = board#np.copy(board)
        for row_nr in reversed(range(self.rows())):
            if new_board[row_nr, col_nr] == 0:
                new_board[row_nr, col_nr] = curr_player
                return new_board

    def id(self):
        """ Returns own bot id. """
        return self.settings['your_botid']

    def rows(self):
        """ Returns amount of rows. """
        return self.settings['field_height']

    def cols(self):
        """ Returns amount of columns. """
        return self.settings['field_width']

    def current_milli_time(self):
        """ Returns current system time in milliseconds. """
        return int(round(time.time() * 1000))

    def set_timeout(self, millis):
        """ Sets time left until timeout in milliseconds. """
        self.timeout = self.current_milli_time() + millis

    def time_left(self):
        """ Get how much time is left until a timeout. """
        return self.timeout - self.current_milli_time()

    def run(self):
        """ Main loop.
        """
        while not stdin.closed:
            try:
                rawline = stdin.readline()

                # End of file check
                if len(rawline) == 0:
                    break

                line = rawline.strip()

                # Empty lines can be ignored
                if len(line) == 0:
                    continue

                parts = line.split()

                command = parts[0]

                self.parse_command(command, parts[1:])

            except EOFError:
                return

    def parse_command(self, command, args):
        if command == 'settings':
            key, value = args
            if key in ('timebank', 'time_per_move', 'your_botid', 'field_columns', 'field_rows'):
                value = int(value)
            self.settings[key] = value

        elif command == 'update':
            sub_command = args[1]
            args = args[2:]

            if sub_command == 'round':
                self.round = int(args[0])
            elif sub_command == 'field':
                self.parse_field(args[0])

        elif command == 'action':
            self.set_timeout(int(args[1]))
            self.make_turn()

    def parse_field(self, str_field):
        #self.board = np.fromstring(str_field.replace(';', ','), sep=',', dtype=np.uint8).reshape(self.rows(), self.cols())
        
        board = str_field.split(',')
        for i in range(0,int(self.rows())):
            for j in range(0,int(self.cols())):
                self.board[i][j] = board[i*int(self.cols())+j]
        
                

    class ColumnFullException(Exception):
        """ Raised when attempting to place disk in full column. """


class StarterBot(Bot):
    def solve_for_move(self,board):
        g = ConnectFour.Game(1,2,self.timeout)
        return g.Solve(board)


    def make_turn(self):
        #print self.board
        move = self.solve_for_move(self.board)
        self.place_disc(move)


if __name__ == '__main__':
    """ Run the bot! """

    StarterBot().run()
