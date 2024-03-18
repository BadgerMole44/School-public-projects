# Author: Keegan Forsythe
# GitHub username: BadgerMole44
# Date: 3/17/2024
# Description: This file contains the ChessVar class and its supporting classes ChessBoard, ChessPiece and chess pieces
#   subclasses. Together these classes simulate a variation of a game of chess where the game ends when a king is
#   captured. There is no check or checkmate, and there is no castling, en passant, or pawn promotion. There are two
#   fairy pieces that can be utilized.
#       Falcon: moves forward like a bishop, and backward like a rook
#       Hunter: moves forward like a rook and backward like a bishop
#   fairy pieces can enter the board once a player loses their queen, a rook, a bishop, or a knight, they may, on any
#   subsequent move. The fairy pieces enter the board on an empty square of their two home ranks.
#   Doing so constitutes a turn. The player becomes eligible to enter their remaining fairy piece (falcon or hunter)
#   after losing a second piece (queen, rook, bishop, or knight)(could be anytime after losing the first piece, don’t
#   need to be losing after entering the first fairy piece).


class ChessPiece:
    """Represents a piece on a chess board. Every piece has a color, starting position, and
    current position """
    def __init__(self, color):
        self._color = color                     # 'w' = white 'b' = black
        self._start_pos = None                  # The position of the piece when it was initially set on a chess board
        self._cur_pos = None                    # The current position of the piece on a chess board

    def get_color(self):
        """Returns the color of the piece"""
        return self._color

    def get_start_pos(self):
        """Returns the starting position of the piece"""
        return self._start_pos

    def get_cur_pos(self):
        """Returns the current position of the piece"""
        return self._cur_pos

    def set_start_pos(self, pos):
        """Sets the starting position"""
        self._start_pos = pos

    def set_cur_pos(self, pos):
        """Sets the current position"""
        self._cur_pos = pos


class Pawn(ChessPiece):
    """Represents a black or white pawn piece with a name, image, and method for validating moves."""
    def __init__(self, color):
        super().__init__(color)
        self._name = 'pawn'
        self._image = None

    def get_name(self):
        """Returns the piece name"""
        return self._name

    def get_image(self):
        """Returns the pawn image. Checks to see if the image has been set by self.set_image. if not, the method is
         called"""
        if self._image is None:  # check if the image is set
            self.set_image()

        return self._image

    def set_image(self):
        """Sets self._image to be a black or white piece based on self._color"""
        if self.get_color() == 'w':                     # white
            self._image = '\u265F'
        if self.get_color() == 'b':                     # black
            self._image = '\u2659'

    def validate_move_for_piece(self, destination):
        """
        Calculates if the destination is a valid move for the piece based on its current location. If it is a valid move
        fills a list with positions between the pieces current location and the destination.

        :param destination: destination to validate. (EX. 'a1', 'H5')
        :return: a tuple (True or False , [list of positions between the current position and the destination])
                True:
                    this is a valid move for the piece based on its current location.
                False:
                    this is not a valid move for the piece based on its current location.
        """
        # initialize the list of positions to an empty list
        positions_between = []
        cur_pos = self.get_cur_pos()
        # is it a white pawn
        if self.get_color() == 'w':
            # check if the column is the same
            if cur_pos[0] == destination[0]:
                # is the row one above
                if destination[1] == chr(ord(cur_pos[1]) + 1):
                    return True, positions_between
                # is the row two above and has the pawn moved yet
                elif destination[1] == chr(ord(cur_pos[1]) + 2) and cur_pos == self.get_start_pos():
                    positions_between.append(cur_pos[0] + chr(ord(cur_pos[1]) + 1))
                    return True, positions_between
                # only move 1 or two positions forward
                else:
                    return False, positions_between
            # if the column is not the same the destination could be a diagonal capture
            if cur_pos[1] != destination[1]:
                # is the destination one row up
                if destination[1] == chr(ord(cur_pos[1]) + 1):
                    # is the destination to one column left or right
                    if destination[0] == chr(ord(cur_pos[0]) - 1) or destination[0] == chr(ord(cur_pos[0]) + 1):
                        return True, positions_between

            return False, positions_between

        # is it a black pawn
        # check if the row is the same
        if cur_pos[0] == destination[0]:
            # is the row one below
            if destination[1] == chr(ord(cur_pos[1]) - 1):
                 return True, positions_between
                # is the row two below and has the pawn moved yet
            elif destination[1] == chr(ord(cur_pos[1]) - 2) and cur_pos == self.get_start_pos():
                positions_between.append(cur_pos[0] + chr(ord(cur_pos[1]) - 1))
                return True, positions_between
            # only move 1 or two positions forward
            else:
                 return False, positions_between
            # if the column is not the same the destination could be a diagonal capture
        if cur_pos[1] != destination[1]:
            # is the destination one row down
            if destination[1] == chr(ord(cur_pos[1]) - 1):
                # is the destination to one column left or right
                if destination[0] == chr(ord(cur_pos[0]) - 1) or destination[0] == chr(ord(cur_pos[0]) + 1):
                    return True, positions_between

        return False, positions_between

class Rook(ChessPiece):
    """Represents a black or white rook piece with a name, image, and method for validating moves."""
    def __init__(self, color):
        super().__init__(color)
        self._name = 'Rook'
        self._image = None

    def get_name(self):
        """Returns the piece name"""
        return self._name

    def get_image(self):
        """Returns the pawn image. Checks to see if the image has been set by self.set_image. if not, the method is
         called"""
        if self._image is None:  # check if the image is set
            self.set_image()

        return self._image

    def set_image(self):
        """Sets self._image to be a black or white piece based on self,_color"""
        if self.get_color() == 'w':                 # white
            self._image = '\u265C'
        if self.get_color() == 'b':                 # black
            self._image = '\u2656'

    def validate_move_for_piece(self, destination):
        """
        Calculates if the destination is a valid move for the piece based on its current location. If it is a valid move
        fills a list with positions between the pieces current location and the destination.

        :param destination: destination to validate. (EX. 'a1', 'H5')
        :return: a tuple (True or False , [list of positions between the current position and the destination])
                True:
                    this is a valid move for the piece based on its current location.
                False:
                    this is not a valid move for the piece based on its current location.
        """
        # initialize the list of positions to an empty list
        positions_between = []
        cur_pos = self.get_cur_pos()

        # is it a vertical move
        if destination[0] == cur_pos[0]:
                # is it a move up
                if destination[1] > cur_pos[1]:
                    # place positions between destination and cur_pos in list
                    tmp = destination
                    distance = ord(destination[1]) - ord(cur_pos[1]) - 1
                    for pos in range(distance):
                        tmp = tmp[0] + chr(ord(tmp[1]) - 1)
                        positions_between.append(tmp)
                    return True, positions_between
                # is it a move down
                if destination[1] < cur_pos[1]:
                    # place positions between destination and cur_pos in list
                    tmp = destination
                    distance = ord(cur_pos[1]) - ord(destination[1]) - 1
                    for pos in range(distance):
                        tmp = tmp[0] + chr(ord(tmp[1]) + 1)
                        positions_between.append(tmp)
                    return True, positions_between
        # is it a horizontal move
        if destination[1] == cur_pos[1]:
                # is it a move right
                if destination[0] > cur_pos[0]:
                    # place positions between destination and cur_pos in list
                    tmp = destination
                    distance = abs(ord(destination[0]) - ord(cur_pos[0]) - 1)
                    for pos in range(distance):
                        tmp = chr(ord(tmp[0]) - 1) + tmp[1]
                        positions_between.append(tmp)
                    return True, positions_between
                # is it a move left
                if destination[0] < cur_pos[0]:
                    # place positions between destination and cur_pos in list
                    tmp = destination
                    distance = ord(cur_pos[0]) - ord(destination[0]) - 1
                    for pos in range(distance):
                        tmp = chr(ord(tmp[0]) + 1) + tmp[1]
                        positions_between.append(tmp)
                    return True, positions_between
        # rooks can only move horizontally and vertically
        else:
            return False, positions_between

class Knight(ChessPiece):
    """Represents a black or white knight piece with a name, image, and method for validating moves."""
    def __init__(self, color):
        super().__init__(color)
        self._name = 'Knight'
        self._image = None

    def get_name(self):
        """Returns the piece name"""
        return self._name

    def get_image(self):
        """Returns the pawn image. Checks to see if the image has been set by self.set_image. if not, the method is
         called"""
        if self._image is None:  # check if the image is set
            self.set_image()

        return self._image

    def set_image(self):
        """Sets self._image to be a black or white piece based on self,_color"""
        if self.get_color() == 'w':                     # white
            self._image = '\u265E'
        if self.get_color() == 'b':                     # black
            self._image = '\u2658'

    def validate_move_for_piece(self, destination):
        """
        Calculates if the destination is a valid move for the piece based on its current location. If it is a valid move
        fills a list with positions between the pieces current location and the destination.

        :param destination: destination to validate. (EX. 'a1', 'H5')
        :return: a tuple (True or False , [list of positions between the current position and the destination])
                the list of positions between will always be empty because knights jump
                True:
                    this is a valid move for the piece based on its current location.
                False:
                    this is not a valid move for the piece based on its current location.
        """
        # initialize the list of positions to an empty list
        positions_between = []
        cur_pos = self.get_cur_pos()

        # up two
        if destination[1] == chr(ord(cur_pos[1]) + 2):
            # left one
            if destination[0] == chr(ord(cur_pos[0]) - 1):
                return True, positions_between
            # right one
            if destination[0] == chr(ord(cur_pos[0]) + 1):
                return True, positions_between
        # up one
        if destination[1] == chr(ord(cur_pos[1]) + 1):
            # left two
            if destination[0] == chr(ord(cur_pos[0]) - 2):
                return True, positions_between
            # right two
            if destination[0] == chr(ord(cur_pos[0]) + 2):
                return True, positions_between
        # down two
        if destination[1] == chr(ord(cur_pos[1]) - 2):
            # left one
            if destination[0] == chr(ord(cur_pos[0]) - 1):
                return True, positions_between
            # right one
            if destination[0] == chr(ord(cur_pos[0]) + 1):
                return True, positions_between
            else:
                return False, positions_between
        # down one
        if destination[1] == chr(ord(cur_pos[1]) - 1):
            # left two
            if destination[0] == chr(ord(cur_pos[0]) - 2):
                return True, positions_between
            # right two
            if destination[0] == chr(ord(cur_pos[0]) + 2):
                return True, positions_between

        return False, positions_between # knights only have 8 possible destinations based on their current position

class Bishop(ChessPiece):
    """Represents a black or white Bishop piece with a name, image, and method for validating moves."""
    def __init__(self, color):
        super().__init__(color)
        self._name = 'bishop'
        self._image = None

    def get_name(self):
        """Returns the piece name"""
        return self._name

    def get_image(self):
        """Returns the pawn image. Checks to see if the image has been set by self.set_image. if not, the method is
         called"""
        if self._image is None:  # check if the image is set
            self.set_image()

        return self._image

    def set_image(self):
        """Sets self._image to be a black or white piece based on self,_color"""
        if self.get_color() == 'w':                     # white
            self._image = '\u265D'
        if self.get_color() == 'b':                     # black
            self._image = '\u2657'

    def validate_move_for_piece(self, destination):
        """
        Calculates if the destination is a valid move for the piece based on its current location. If it is a valid move
        fills a list with positions between the pieces current location and the destination.

        :param destination: destination to validate. (EX. 'a1', 'H5')
        :return: a tuple (True or False , [list of positions between the current position and the destination])
                True:
                    this is a valid move for the piece based on its current location.
                False:
                    this is not a valid move for the piece based on its current location.
        """
        # initialize the list of positions to an empty list
        positions_between = []
        cur_pos = self.get_cur_pos()

        # confirm the destination is a diagonal move from the current position
        abs_vertical_difference = abs(ord(cur_pos[1]) - ord(destination[1]))
        abs_horizontal_difference = abs(ord(cur_pos[0]) - ord(destination[0]))
        if abs_vertical_difference != abs_horizontal_difference:
            return False, positions_between

        tmp = destination
        distance = abs_vertical_difference - 1

        # up
        if destination[1] > cur_pos[1]:
            # left
            if destination[0] < cur_pos[0]:
                # add positions inbetween to list
                for pos in range(distance):
                    tmp = chr(ord(tmp[0]) + 1) + chr(ord(tmp[1]) - 1)
                    positions_between.append(tmp)
                return True, positions_between
            # right
            if destination[0] > cur_pos[0]:
                # add positions inbetween to list
                for pos in range(distance):
                    tmp = chr(ord(tmp[0]) - 1) + chr(ord(tmp[1]) - 1)
                    positions_between.append(tmp)
                return True, positions_between
        # down
        if destination[1] < cur_pos[1]:
            # left
            if destination[0] < cur_pos[0]:
                # add positions inbetween to list
                for pos in range(distance):
                    tmp = chr(ord(tmp[0]) + 1) + chr(ord(tmp[1]) + 1)
                    positions_between.append(tmp)
                return True, positions_between
            # right
            if destination[0] > cur_pos[0]:
                # add positions inbetween to list
                for pos in range(distance):
                    tmp = chr(ord(tmp[0]) - 1) + chr(ord(tmp[1]) + 1)
                    positions_between.append(tmp)
                return True, positions_between

class Queen(ChessPiece):
    """Represents a black or white queen piece with a name, image, and method for validating moves."""
    def __init__(self, color):
        super().__init__(color)
        self._name = 'queen'
        self._image = None

    def get_name(self):
        """Returns the piece name"""
        return self._name

    def get_image(self):
        """Returns the pawn image. Checks to see if the image has been set by self.set_image. if not, the method is
         called"""
        if self._image is None:  # check if the image is set
            self.set_image()

        return self._image

    def set_image(self):
        """Sets self._image to be a black or white piece based on self,_color"""
        if self.get_color() == 'w':                     # white
            self._image = '\u265B'
        if self.get_color() == 'b':                     # black
            self._image = '\u2655'

    def validate_move_for_piece(self, destination):
        """
        Calculates if the destination is a valid move for the piece based on its current location. If it is a valid move
        fills a list with positions between the pieces current location and the destination.

        :param destination: destination to validate. (EX. 'a1', 'H5')
        :return: a tuple (True or False , [list of positions between the current position and the destination])
                True:
                    this is a valid move for the piece based on its current location.
                False:
                    this is not a valid move for the piece based on its current location.
        """
        # initialize the list of positions to an empty list
        positions_between = []
        cur_pos = self.get_cur_pos()

        # is it a vertical move
        if destination[0] == cur_pos[0]:
            # is it a move up
            if destination[1] > cur_pos[1]:
                # place positions between destination and cur_pos in list
                tmp = destination
                distance = ord(destination[1]) - ord(cur_pos[1]) - 1
                for pos in range(distance):
                    tmp = tmp[0] + chr(ord(tmp[1]) - 1)
                    positions_between.append(tmp)
                return True, positions_between
            # is it a move down
            if destination[1] < cur_pos[1]:
                # place positions between destination and cur_pos in list
                tmp = destination
                distance = ord(cur_pos[1]) - ord(destination[1]) - 1
                for pos in range(distance):
                    tmp = tmp[0] + chr(ord(tmp[1]) + 1)
                    positions_between.append(tmp)
                return True, positions_between
        # is it a horizontal move
        if destination[1] == cur_pos[1]:
            # is it a move right
            if destination[0] > cur_pos[0]:
                # place positions between destination and cur_pos in list
                tmp = destination
                distance = abs(ord(destination[0]) - ord(cur_pos[0]) - 1)
                for pos in range(distance):
                    tmp = chr(ord(tmp[0]) - 1) + tmp[1]
                    positions_between.append(tmp)
                return True, positions_between
            # is it a move left
            if destination[0] < cur_pos[0]:
                # place positions between destination and cur_pos in list
                tmp = destination
                distance = ord(cur_pos[0]) - ord(destination[0]) - 1
                for pos in range(distance):
                    tmp = chr(ord(tmp[0]) + 1) + tmp[1]
                    positions_between.append(tmp)
                return True, positions_between

        # diagonal moves
        # confirm the destination is a diagonal move from the current position
        abs_vertical_difference = abs(ord(cur_pos[1]) - ord(destination[1]))
        abs_horizontal_difference = abs(ord(cur_pos[0]) - ord(destination[0]))
        if abs_vertical_difference != abs_horizontal_difference:
            return False, positions_between         # not a vertical, horizontal, or diagonal move

        tmp = destination
        distance = abs_vertical_difference - 1

        # up
        if destination[1] > cur_pos[1]:
            # left
            if destination[0] < cur_pos[0]:
                # add positions inbetween to list
                for pos in range(distance):
                    tmp = chr(ord(tmp[0]) + 1) + chr(ord(tmp[1]) - 1)
                    positions_between.append(tmp)
                return True, positions_between
            # right
            if destination[0] > cur_pos[0]:
                # add positions inbetween to list
                for pos in range(distance):
                    tmp = chr(ord(tmp[0]) - 1) + chr(ord(tmp[1]) - 1)
                    positions_between.append(tmp)
                return True, positions_between
        # down
        if destination[1] < cur_pos[1]:
            # left
            if destination[0] < cur_pos[0]:
                # add positions inbetween to list
                for pos in range(distance):
                    tmp = chr(ord(tmp[0]) + 1) + chr(ord(tmp[1]) + 1)
                    positions_between.append(tmp)
                return True, positions_between
            # right
            if destination[0] > cur_pos[0]:
                # add positions inbetween to list
                for pos in range(distance):
                    tmp = chr(ord(tmp[0]) - 1) + chr(ord(tmp[1]) + 1)
                    positions_between.append(tmp)
                return True, positions_between


class King(ChessPiece):
    """Represents a black or white king piece with a name, image, and method for validating moves."""
    def __init__(self, color):
        super().__init__(color)
        self._name = 'king'
        self._image = None

    def get_name(self):
        """Returns the piece name"""
        return self._name

    def get_image(self):
        """Returns the pawn image. Checks to see if the image has been set by self.set_image. if not, the method is
         called"""
        if self._image is None:  # check if the image is set
            self.set_image()

        return self._image

    def set_image(self):
        """Sets self._image to be a black or white piece based on self,_color"""
        if self.get_color() == 'w':                     # white
            self._image = '\u265A'
        if self.get_color() == 'b':                     # black
            self._image = '\u2654'

    def validate_move_for_piece(self, destination):
        """
        Calculates if the destination is a valid move for the piece based on its current location. If it is a valid move
        fills a list with positions between the pieces current location and the destination.

        :param destination: destination to validate. (EX. 'a1', 'H5')
        :return: a tuple (True or False , [list of positions between the current position and the destination])
                True:
                    this is a valid move for the piece based on its current location.
                False:
                    this is not a valid move for the piece based on its current location.
        """
        # initialize the list of positions to an empty list
        positions_between = []
        cur_pos = self.get_cur_pos()

        cur_pos_col_val = ord(cur_pos[0])
        cur_pos_row_val = ord(cur_pos[1])
        dest_col_val = ord(destination[0])
        dest_row_val = ord(destination[1])


        if dest_col_val == cur_pos_col_val + 1:
            # left one
            if dest_row_val == cur_pos_row_val - 1:
                return True, positions_between
            # right one
            if dest_row_val == cur_pos_row_val + 1:
                return True, positions_between
            # up one
            if dest_row_val == cur_pos_row_val:
                return True, positions_between
            else:
                return False, positions_between

        if dest_col_val == cur_pos_col_val - 1:
            # left one
            if dest_row_val == cur_pos_row_val - 1:
                return True, positions_between
            # right one
            if dest_row_val == cur_pos_row_val + 1:
                return True, positions_between
            # down one
            if dest_row_val == cur_pos_row_val:
                return True, positions_between
            else:
                return False, positions_between

        if dest_col_val == cur_pos_col_val:
            # left one
            if dest_row_val == cur_pos_row_val - 1:
                return True, positions_between
            # right one
            if dest_row_val == cur_pos_row_val + 1:
                return True, positions_between
            else:
                return False, positions_between
        else:
            return False, positions_between


class Falcon(ChessPiece):
    """Represents a black or white fairy Falcon piece with a name, image, and method for validating moves."""
    def __init__(self, color):
        super().__init__(color)
        self._name = 'falcon'
        self._image = None

    def get_name(self):
        """Returns the piece name"""
        return self._name

    def get_image(self):
        """Returns the pawn image. Checks to see if the image has been set by self.set_image. if not, the method is
         called"""
        if self._image is None:  # check if the image is set
            self.set_image()

        return self._image

    def set_image(self):
        """Sets self._image to be a black or white piece based on self,_color"""
        if self.get_color() == 'w':                     # white
            self._image = '\u2660'
        if self.get_color() == 'b':                     # black
            self._image = '\u2664'

    def validate_move_for_piece(self, destination):
        """
        Calculates if the destination is a valid move for the piece based on its current location. If it is a valid move
        fills a list with positions between the pieces current location and the destination.

        :param destination: destination to validate. (EX. 'a1', 'H5')
        :return: a tuple (True or False , [list of positions between the current position and the destination])
                True:
                    this is a valid move for the piece based on its current location.
                False:
                    this is not a valid move for the piece based on its current location.
        """
        # initialize the list of positions to an empty list
        positions_between = []
        cur_pos = self.get_cur_pos()

        # is the falcon white
        if self.get_color() == 'w':
            # down like a rook
            # is it a downward vertical move
            if destination[0] == cur_pos[0] and destination[1] < cur_pos[1]:
                # place positions between destination and cur_pos in list
                tmp = destination
                distance = ord(cur_pos[1]) - ord(destination[1]) - 1
                for pos in range(distance):
                    tmp = tmp[0] + chr(ord(tmp[1]) + 1)
                    positions_between.append(tmp)
                return True, positions_between

            # up like a bishop
            # confirm the destination is a diagonal move from the current position
            abs_vertical_difference = abs(ord(cur_pos[1]) - ord(destination[1]))
            abs_horizontal_difference = abs(ord(cur_pos[0]) - ord(destination[0]))
            if abs_vertical_difference != abs_horizontal_difference:
                return False, positions_between  # not a vertical or diagonal move

            tmp = destination
            distance = abs_vertical_difference - 1

            # up
            if destination[1] > cur_pos[1]:
                # left
                if destination[0] < cur_pos[0]:
                    # add positions inbetween to list
                    for pos in range(distance):
                        tmp = chr(ord(tmp[0]) + 1) + chr(ord(tmp[1]) - 1)
                        positions_between.append(tmp)
                    return True, positions_between
                # right
                if destination[0] > cur_pos[0]:
                    # add positions inbetween to list
                    for pos in range(distance):
                        tmp = chr(ord(tmp[0]) - 1) + chr(ord(tmp[1]) - 1)
                        positions_between.append(tmp)
                    return True, positions_between

            else:
                return False, positions_between # no valid movement for white falcon

        # otherwise if the falcon is black
        # up like a rook
        if destination[0] == cur_pos[0] and destination[1] > cur_pos[1]:
                # place positions between destination and cur_pos in list
                tmp = destination
                distance = ord(destination[1]) - ord(cur_pos[1]) - 1
                for pos in range(distance):
                    tmp = tmp[0] + chr(ord(tmp[1]) - 1)
                    positions_between.append(tmp)
                return True, positions_between

        # down like a bishop
        # diagonal moves
        # confirm the destination is a diagonal move from the current position
        abs_vertical_difference = abs(ord(cur_pos[1]) - ord(destination[1]))
        abs_horizontal_difference = abs(ord(cur_pos[0]) - ord(destination[0]))
        if abs_vertical_difference != abs_horizontal_difference:
            return False, positions_between         # not a vertical, horizontal, or diagonal move

        tmp = destination
        distance = abs_vertical_difference - 1

        # down
        if destination[1] < cur_pos[1]:
            # left
            if destination[0] < cur_pos[0]:
                # add positions inbetween to list
                for pos in range(distance):
                    tmp = chr(ord(tmp[0]) + 1) + chr(ord(tmp[1]) + 1)
                    positions_between.append(tmp)
                return True, positions_between
            # right
            if destination[0] > cur_pos[0]:
                # add positions inbetween to list
                for pos in range(distance):
                    tmp = chr(ord(tmp[0]) - 1) + chr(ord(tmp[1]) + 1)
                    positions_between.append(tmp)
                return True, positions_between
        else:
            return False, positions_between  # no valid movement for black falcon

class Hunter(ChessPiece):
    """Represents a black or white hunter fairy piece with a name, image, and method for validating moves."""
    def __init__(self, color):
        super().__init__(color)
        self._name = 'hunter'
        self._image = None

    def get_name(self):
        """Returns the piece name"""
        return self._name

    def get_image(self):
        """Returns the pawn image. Checks to see if the image has been set by self.set_image. if not, the method is
        called"""
        if self._image is None:     # check if the image is set
            self.set_image()

        return self._image

    def set_image(self):
        """Sets self._image to be a black or white piece based on self,_color"""
        if self.get_color() == 'w':                     # white
            self._image = '\u2665'
        if self.get_color() == 'b':                     # black
            self._image = '\u2661'

    def validate_move_for_piece(self, destination):
        """
        Calculates if the destination is a valid move for the piece based on its current location. If it is a valid move
        fills a list with positions between the pieces current location and the destination.

        :param destination: destination to validate. (EX. 'a1', 'H5')
        :return: a tuple (True or False , [list of positions between the current position and the destination])
                True:
                    this is a valid move for the piece based on its current location.
                False:
                    this is not a valid move for the piece based on its current location.
        """
        # initialize the list of positions to an empty list
        positions_between = []
        cur_pos = self.get_cur_pos()

        # if the hunter is white move up like a rook and down like a bishop
        if self.get_color() == 'w':
            # up like a rook

            if destination[0] == cur_pos[0] and destination[1] > cur_pos[1]:
                # place positions between destination and cur_pos in list
                tmp = destination
                distance = ord(destination[1]) - ord(cur_pos[1]) - 1
                for pos in range(distance):
                    tmp = tmp[0] + chr(ord(tmp[1]) - 1)
                    positions_between.append(tmp)
                return True, positions_between

            # down like a bishop
            # confirm the destination is a diagonal move from the current position
            abs_vertical_difference = abs(ord(cur_pos[1]) - ord(destination[1]))
            abs_horizontal_difference = abs(ord(cur_pos[0]) - ord(destination[0]))
            if abs_vertical_difference != abs_horizontal_difference:
                return False, positions_between  # not a vertical or diagonal move

            tmp = destination
            distance = abs_vertical_difference - 1

            # down
            if destination[1] < cur_pos[1]:
                # left
                if destination[0] < cur_pos[0]:
                    # add positions inbetween to list
                    for pos in range(distance):
                        tmp = chr(ord(tmp[0]) + 1) + chr(ord(tmp[1]) + 1)
                        positions_between.append(tmp)
                    return True, positions_between
                # right
                if destination[0] > cur_pos[0]:
                    # add positions inbetween to list
                    for pos in range(distance):
                        tmp = chr(ord(tmp[0]) - 1) + chr(ord(tmp[1]) + 1)
                        positions_between.append(tmp)
                    return True, positions_between
            else:
                return False, positions_between # no valid movement for white hunter
        # if it is black
        # down like a rook
        # is it a downward vertical move
        if destination[0] == cur_pos[0] and destination[1] < cur_pos[1]:
            # place positions between destination and cur_pos in list
            tmp = destination
            distance = ord(cur_pos[1]) - ord(destination[1]) - 1
            for pos in range(distance):
                tmp = tmp[0] + chr(ord(tmp[1]) + 1)
                positions_between.append(tmp)
            return True, positions_between

        # up like a bishop
        # confirm the destination is a diagonal move from the current position
        abs_vertical_difference = abs(ord(cur_pos[1]) - ord(destination[1]))
        abs_horizontal_difference = abs(ord(cur_pos[0]) - ord(destination[0]))
        if abs_vertical_difference != abs_horizontal_difference:
            return False, positions_between  # not a vertical or diagonal move

        tmp = destination
        distance = abs_vertical_difference - 1

        # up
        if destination[1] > cur_pos[1]:
            # left
            if destination[0] < cur_pos[0]:
                # add positions inbetween to list
                for pos in range(distance):
                    tmp = chr(ord(tmp[0]) + 1) + chr(ord(tmp[1]) - 1)
                    positions_between.append(tmp)
                return True, positions_between
            # right
            if destination[0] > cur_pos[0]:
                # add positions inbetween to list
                for pos in range(distance):
                    tmp = chr(ord(tmp[0]) - 1) + chr(ord(tmp[1]) - 1)
                    positions_between.append(tmp)
                return True, positions_between

        else:
            return False, positions_between  # no valid movement for black hunter

class ChessBoard:
    """Represents a board in chess composed of Pieces. A position is identified by algebraic notation. Columns 1-8 and
    rows a-h.
    Methods:
            get_board
            get_sidelined_white_fairy_pieces
            get_sidelined_black_fairy_pieces
            get_pieces
            get_captured_white_pieces
            get_captured_black_pieces
            get_pos
            initialize_pieces
            validate_pos
            move_piece
            set_piece_on_board
            clear_board
            set_board
            display_board
    """
    def __init__(self):
        self._board = {
            '8': {'a': None, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': None, 'h': None},
            '7': {'a': None, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': None, 'h': None},
            '6': {'a': None, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': None, 'h': None},
            '5': {'a': None, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': None, 'h': None},
            '4': {'a': None, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': None, 'h': None},
            '3': {'a': None, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': None, 'h': None},
            '2': {'a': None, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': None, 'h': None},
            '1': {'a': None, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': None, 'h': None},
        }
        self._pieces = []
        self._sidelined_white_fairy_pieces = []
        self._sidelined_black_fairy_pieces = []
        self._captured_white_pieces = []
        self._captured_black_pieces = []

    def get_board(self):
        """Returns the board"""
        return self._board

    def get_sidelined_white_fairy_pieces(self):
        """Returns the list of sidelined white fairy pieces"""
        return self._sidelined_white_fairy_pieces

    def get_sidelined_black_fairy_pieces(self):
        """Returns the list of sidelined black fairy pieces"""
        return self._sidelined_black_fairy_pieces

    def get_pieces(self):
        """Returns the list of all chess pieces"""
        return self._pieces

    def get_captured_white_pieces(self):
        """Returns the list of captured white pieces"""
        return self._captured_white_pieces

    def get_captured_black_pieces(self):
        """Returns the list of captured black pieces"""
        return self._captured_black_pieces

    def get_pos(self, pos):
        """Returns the contents of a position on the _board. If the position is invalid returns None"""
        # validate the position
        if self.validate_pos(pos) is False:
            return None

        pos = pos[0].lower() + pos[1]               # make sure the column is lower case

        return self._board[pos[1]][pos[0]]          # return the position contents

    def initialize_pieces(self):
        """Creates all pieces for a VarChess game, set their starting position, and places them in the pieces list.
        If the pieces list is already populated return false. Otherwise, return true."""
        if not self._pieces:

            white_pawn_row = '2'
            col = 'a'
            black_pawn_row = '7'

            # create 8 white and 8 black pawns, set their starting position, and add them to the pieces list.
            for pawn in range(8):
                white_pawn = Pawn('w')
                black_pawn = Pawn('b')
                white_pawn.set_start_pos(f'{col + white_pawn_row}')
                black_pawn.set_start_pos(f'{col + black_pawn_row}')
                self._pieces.append(white_pawn)
                self._pieces.append(black_pawn)

                col = chr(ord(col) + 1)  # move to the next column

            black_special_row = '8'
            white_special_row = '1'
            col = 'a'

            # create 2 white rooks, knights, and bishops and 2 black rooks, knights, and bishops
            for piece in range(2):
                white_rook = Rook('w')
                black_rook = Rook('b')
                white_rook.set_start_pos(f'{col + white_special_row}')
                black_rook.set_start_pos(f'{col + black_special_row}')

                # move to the next column to the left or right depending on the iteration
                if col > 'c':
                    col = chr(ord(col) - 1)  # move left one column

                else:
                    col = chr(ord(col) + 1)  # move to the right one column


                white_knight = Knight('w')
                black_knight = Knight('b')
                white_knight.set_start_pos(f'{col + white_special_row}')
                black_knight.set_start_pos(f'{col + black_special_row}')

                # move to the next column to the left or right depending on the iteration
                if col > 'c':
                    col = chr(ord(col) - 1)  # move left one column
                else:
                    col = chr(ord(col) + 1)  # move to the right one column

                white_bishop = Bishop('w')
                black_bishop = Bishop('b')
                white_bishop.set_start_pos(f'{col + white_special_row}')
                black_bishop.set_start_pos(f'{col + black_special_row}')

                col = 'h'                           # move to column h

                self._pieces.append(white_rook)
                self._pieces.append(black_rook)
                self._pieces.append(white_knight)
                self._pieces.append(black_knight)
                self._pieces.append(white_bishop)
                self._pieces.append(black_bishop)

            # create 1 white king, queen, hunter, falcon and 1 black king, queen, hunter, falcon
            white_king = King('w')
            white_king.set_start_pos('e1')

            black_king = King('b')
            black_king.set_start_pos('e8')

            white_queen = Queen('w')
            white_queen.set_start_pos('d1')

            black_queen = Queen('b')
            black_queen.set_start_pos('d8')

            white_hunter = Hunter('w')          # hunter starting positions are none
            black_hunter = Hunter('b')

            white_falcon = Falcon('w')          # falcon starting positions are none
            black_falcon = Falcon('b')

            self._pieces.append(white_king)
            self._pieces.append(black_king)
            self._pieces.append(white_queen)
            self._pieces.append(black_queen)
            self._pieces.append(white_hunter)
            self._pieces.append(black_hunter)
            self._pieces.append(white_falcon)
            self._pieces.append(black_falcon)

            return True         # the pieces list was populated

        return False           # the pieces list was already populated

    def validate_pos(self, pos):
        """
        Validates that the position is a valid position on a chess board. A valid position would be str two char
            long where the first char is between a - h inclusive (capitalization does not matter) and the second char
            is between 1 - 8 inclusive.
        :param pos: the (hopefully str) chess board position to be evaluated
        :return: True if the position is valid. False otherwise.
        """
        # check that the position is a str and is only two characters long.
        if isinstance(pos, str) and len(pos) <= 2:

            # check that the row is between 1 and 8 inclusive and the column is between a and h inclusive
            if pos[0].lower() >= 'a' and pos[0].lower() <= 'h' and pos[1] >= '0' and pos[1] <= '8':
                return True

        # the position is not a valid position on a chess board
        return False

    def move_piece(self, piece_location, destination):
        """
        Moves a chess Piece object on a ChessBoard object. Updates the Board and the pieces current location. If there
        is a piece at the destination, and it is a valid capture then that piece is moved to the captured pieces
        list that corresponds to their color. The captured pieces current location is updated to none.
        :param piece_location: A string the location of the piece to be moved formatted like 'a1'
        :param destination: A string the location the piece if to be moved to formatted like 'a1'
        :return:
                False:
                    the piece at the destination is not a valid capture (it's the came color).
                True:
                    The piece is moved to an unoccupied location at the destination position.
                    The piece at the destination is captured and then the piece is moved to its destination position.
        """
        initial_pos_piece = self._board[piece_location[1]][piece_location[0]]

        # Is there a piece at the destination
        destination_pos_piece = self._board[destination[1]][destination[0]]
        if destination_pos_piece is None:

            self._board[destination[1]][destination[0]] = initial_pos_piece        # move piece on the board
            initial_pos_piece.set_cur_pos(destination)                     # update the pieces current position
            self._board[piece_location[1]][piece_location[0]] = None            # set its previous location to None
            return True

        # Is the piece at the destination the same or different color as the piece at the initial position
        if initial_pos_piece.get_color() == destination_pos_piece.get_color():
            return False  # a piece cannot capture a piece of the same color

        # the initial piece is capturing the piece at the destination
        # move piece at destination into the correct captured list
        if destination_pos_piece.get_color() == 'w':
            self._captured_white_pieces.append(destination_pos_piece)
        else:
            self._captured_black_pieces.append(destination_pos_piece)

        destination_pos_piece.set_cur_pos(None)     # update the current location of the captured piece to None
        self._board[destination[1]][destination[0]] = initial_pos_piece  # move piece on the board
        initial_pos_piece.set_cur_pos(destination)  # update the pieces current position
        self._board[piece_location[1]][piece_location[0]] = None  # set its previous location to None
        return True

    def set_piece_on_board(self, piece, piece_destination):
        """
        Sets a piece on a chess board. Validates the position and the piece checks if the position is already occupied.
            updates the board position and piece current position.
        :param piece: chess piece to be placed on the board.
        :param piece_destination: position the piece is to be placed in on the chess board
        :return: return True if the piece is set in the destination and its starting and current positions are updated.
        """
        # if the destination is a valid position and is the piece is a chess Piece.
        if self.validate_pos(piece_destination) is True and isinstance(piece, ChessPiece):
            col = piece_destination[0]
            row = piece_destination[1]

            # go to the correct row and column and check if the position is empty
            if self._board[row][col] is None:
                self._board[row][col] = piece       # set the piece on the board
                piece.set_cur_pos(piece_destination)
                return True     # the piece has been set on the board and the pieces current position has been updated

        return False        # the destination is invalid or the position on the board is already occupied

    def clear_board(self):
        """Removes all pieces from the board, sidelines, and captured lists. Return True when finished. Pieces
        remain in the pieces list."""

        # remove pieces from all positions on the board setting them to None
        for row in self._board:
            for col in self._board[row]:
                self._board[row][col] = None

        # clear sideline and captured lists
        self._sidelined_white_fairy_pieces.clear()
        self._sidelined_black_fairy_pieces.clear()
        self._captured_white_pieces.clear()
        self._captured_black_pieces.clear()

        return True

    def set_board(self):
        """Sets all pieces on the board in their starting positions, sets fairy pieces in their sidelines, removes
        pieces from captured lists. returns nothing"""
        # Make sure the pieces are in the pieces list
        if not self._pieces:
            self.initialize_pieces()

        # check that the board, sidelines, and captured lists are cleared
        if self.clear_board() is True:

            for piece in self._pieces:     # set each piece in the list on the board in starting positions

                if piece.get_start_pos() is not None:   # excluding fairy positions

                    self.set_piece_on_board(piece, piece.get_start_pos())

                # place fairy pieces in their sideline according to their color
                elif piece.get_color() == 'w':
                    self._sidelined_white_fairy_pieces.append(piece)
                else:
                    self._sidelined_black_fairy_pieces.append(piece)

    def display_board(self):
        """Displays the ChessBoard using unicode and ASCII art."""
        for row in range(8):        # for the top of the board and down

            cur_row = str(8 - row)  # current row number

            # print the horizontal lines for this column
            print('   ', end='')
            for col in range(8):
                print(f'-------', end='')
            print(f'-', end='')
            print()

            print(f'{cur_row}  ', end='')   # print the row number

            # print the vertical line and piece for this column
            for col in range(9):
                print(f'|', end='')

                cur_col = chr(ord('a') + col)       # current column letter

                # if there is a piece at the current position get the image and print it.
                if cur_col <= 'h' and isinstance(self._board[cur_row][cur_col], ChessPiece):
                        print(f'  {self._board[cur_row][cur_col].get_image()}  ', end='')

                # otherwise print 3 spaces
                else:
                    print('      ', end='')

            # display captured white pieces
            # if on the second row and captured white pieces list is not empty
            if row == 1 and self._captured_white_pieces:
                print("Captured White Pieces: ", end='')
                for piece in self._captured_white_pieces:
                    print(f'{piece.get_image()} ', end='')

            # display captured black pieces
            # if on the second to last row and captured black pieces list is not empty
            if row == 6 and self._captured_black_pieces:
                print("Captured Black Pieces: ", end='')
                for piece in self._captured_black_pieces:
                    print(f'{piece.get_image()} ', end='')

            # display white fairy pieces
            # if on the last row and white fairy pieces list is not empty
            if row == 7 and self._sidelined_white_fairy_pieces:
                print("Available White Fairy Pieces: ", end='')
                for piece in self._sidelined_white_fairy_pieces:
                    print(f'{piece.get_image()} ', end='')

            # display black fairy pieces
            # if on the first row and black fairy pieces list is not empty
            if row == 0 and self._sidelined_black_fairy_pieces:
                print("Available black Fairy Pieces: ", end='')
                for piece in self._sidelined_black_fairy_pieces:
                    print(f'{piece.get_image()} ', end='')

            print()     # move to next row

        # print the last horizontal lines
        print('   ', end='')
        for lines in range(8):
            print(f'-------', end='')
        print(f'-', end='')
        print()

        # print the column letters
        print('      a      b      c      d      e      f      g      h')



class ChessVar:
    """The ChessVar class represents a variation of a game of chess and is composed of a ChessBoard and chess Pieces.
    The ChessVar class is a game it tracks who's turn it is and the game state"""
    def __init__(self):
        self._game = ChessBoard()
        self._current_turn = 'w'                    # white pieces move first
        self._game_state = None                     # set to unfinished when the game has started

    def get_current_turn(self):
        return self._current_turn
    def get_game_state(self):
        """Returns the state of the game"""
        if self._game_state is None:                # make sure the game is started
            self.start_or_restart_game()

        return self._game_state

    def start_or_restart_game(self):
        """Start the ChessVar game by 'setting the board' by using ChessBoard method .set_board. This clears the board,
         sets the pieces on the board, and sets the fairy pieces in their lists. Also updates the game state to
         indicate a game is UNFINISHED"""
        self._game.set_board()
        self._game_state = 'UNFINISHED'


    def check_for_winner(self):
        """
        Call this after each valid move.
        checks if white won or if black won by looking at the last piece added to the captured pieces lists.
        updates the game state to indicate winner.
        :return: True if a winner is detected. False otherwise.
        """
        # check if white won
        if self._game.get_captured_black_pieces():                              # have any black pieces been captured
            captured_black_pieces = self._game.get_captured_black_pieces()
            last_piece = captured_black_pieces[len(captured_black_pieces) - 1]  # look at the last captured piece
            if isinstance(last_piece, King):   # is the last piece a king
                self._game_state = 'WHITE_WON'
                return True

        # check if black won
        if self._game.get_captured_white_pieces():                               # have any white pieces been captured
            captured_white_pieces = self._game.get_captured_white_pieces()
            last_piece = captured_white_pieces[len(captured_white_pieces) - 1]   # look at the last captured piece
            if isinstance(last_piece, King):   # is the last piece a king
                self._game_state = 'BLACK_WON'
                return True

        return False                                                            # no winner detected

    def flip_turn(self):
        """Any time a valid move is made (including entering a fairy piece to the board) method is called to flip the
        turn to the other color"""
        if self._current_turn == 'w':
            self._current_turn = 'b'
        else:
            self._current_turn = 'w'

    def make_move(self, piece_pos, destination):
        """
            Move a chess piece at the piece_pos to the destination. If there is a piece at the destination of the
        opposite color capture it. Check if the game has been won. if the game has not been won flip the turn to the
        other color.
        :param piece_pos: the position of the position to be moved. (EX. 'a1', 'H6')
        :param destination: the position the piece is to be moved to. (EX. 'a1', 'H6')
        :return:
            True:
                The piece at piece_pos is moved to an unoccupied position
                The piece at destination is captured and the piece at piece_pos is moved to the now unoccupied position.
            False:
                The piece_pos or destination are not valid chess board coordinates.
                The game has already been won.
                There is no piece at piece_pos.
                The color of the piece to be moved is not the same as the color of the current turn.
                The piece at destination is the same color as the piece at piece_pos.
                The destination is not a valid move for the type of piece. (EX. a Pawn cannot move more than 1 space
            forward after its first move)
                There are pieces inbetween the pieces and the destination.
        """
        # confirm the game has started and pieces are set
        if self._game_state is None:
            self.start_or_restart_game()

        # confirm the game has not already been won
        if self._game_state != 'UNFINISHED':
            return False

        # confirm the piece_pos and piece_destination are valid chessboard coordinates
        if self._game.validate_pos(piece_pos) is False or self._game.validate_pos(destination) is False:
            return False

        # make sure that the row letter is lowercase for both
        piece_pos = piece_pos[0].lower() + piece_pos[1]
        destination = destination[0].lower() + destination[1]

        # look at the piece_pos
        piece_to_move = self._game.get_pos(piece_pos)
        if piece_to_move is None:                            # is there a piece at the location
            return False

        if piece_to_move.get_color() != self._current_turn:  # does the color of the piece match the color for the turn
            return False

        # is the destination a valid move for the type of piece and what positions are inbetween the piece and the destination
        valid_move_and_positions_between = piece_to_move.validate_move_for_piece(destination)

        if valid_move_and_positions_between[0] is False:    # the destination is not valid for the piece.
            return False

        # edge cases for pawns
        if isinstance(piece_to_move, Pawn):
            destination_pos = self._game.get_pos(destination)
            if piece_pos[0] != destination[0]:             # if the move is diagonal
                # the move must capture a piece
                if destination_pos is None:
                    return False
                if piece_to_move.get_color() == destination_pos.get_color():
                    return False

            # if the move is not diagonal no captures are valid
            elif destination_pos is not None:
                return False


        # are there any pieces in the positions between the pieces location and its destination
        for position_between in valid_move_and_positions_between[1]:
            if self._game.get_pos(position_between) is not None:
                return False

        # Move the piece to the destination, capture a piece if necessary, update current positions of pieces
        if self._game.move_piece(piece_pos, destination) is False:
            return False                                    # attempted to capture a piece of the same color

        # if the king has not been captured flip the turn
        if self.check_for_winner() is False:
            self.flip_turn()

        return True                                         # the piece has been moved to the destination



    def enter_fairy_piece(self, piece, destination):
        """
        Enters a fairy piece on the board at the destination.
        :param piece: h for hunter f for falcon. Capital for white and lower case for black.
        :param destination: a valid chess board coordinate among the colors two home ranks. (ex. 'A1', 'g7')
        :return:
            True:
                    the piece has been placed at the destination, has its current position updated, has
                been removed from its sideline, and the turn has been flipped.
            False:
                    the game has already been won.
                    the destination is not a valid chess board coordinate.
                    the destination is not among the colors two hme ranks
                    the color of the fairy piece being entered is not the same as the color of self._current_turn
                    no special pieces have been lost to allow the first fairy piece to enter.
                    only 1 special piece has been lost so the second fairy piece cannot be entered.
                    the fairu piece that the user wants to enter is no longer in the sideline because it has already
                been entered.
        """

        if self._game_state is None:                                # confirm the game has started and pieces are set
            self.start_or_restart_game()
        if self._game_state != 'UNFINISHED':                        # has the game already been won
            return False
        if self._game.validate_pos(destination) is False:           # confirm the destination is valid
            return False
        destination = destination[0].lower() + destination[1]       # make sure the destination column is in lower case

        # if its whites turn
        if self._current_turn == 'w':
            if piece != 'F' and piece != 'H':                         # is the piece param valid for a white fairy piece
                return False
            if not self._game.get_sidelined_white_fairy_pieces():        # are there any fairy pieces remaining to add
                return False

            # count how many white rooks, knights, bishops, and queens have been captured
            num_special_pieces_captured = 0
            for pieces in self._game.get_captured_white_pieces():
                if isinstance(pieces, (Rook, Knight, Bishop, Queen)):
                    num_special_pieces_captured += 1

            # at least one special piece has to be captured for one fairy piece to be entered
            if num_special_pieces_captured < 1:
                return False

            # at least 2 special pieces must be captured to enter the second fairy piece
            if len(self._game.get_sidelined_white_fairy_pieces()) == 1:     # has one fairy piece already been entered
                if num_special_pieces_captured < 2:
                    return False

            # is the destination for the fairy piece valid
            if destination[1] != '1' and destination[1] != '2':                  # is it among the two white home ranks
                return False
            if self._game.get_pos(destination) is not None:                     # is the position occupied
                return False


            for fairy_piece in self._game.get_sidelined_white_fairy_pieces():

                # if the user wants to enter a white hunter is there a white hunter available
                if isinstance(fairy_piece, Hunter) and piece == 'H':
                    # place the white hunter in the destination
                    self._game.set_piece_on_board(fairy_piece, destination)
                    self._game.get_sidelined_white_fairy_pieces().remove(fairy_piece) # remove the hunter from the sideline
                    self.flip_turn()
                    return True

                # if the user wants to enter the white falcon is a white falcon available
                if isinstance(fairy_piece, Falcon) and piece == 'F':
                    # place the white hunter in the destination
                    self._game.set_piece_on_board(fairy_piece, destination)
                    self._game.get_sidelined_white_fairy_pieces().remove(fairy_piece) # remove the falcon from the sideline
                    self.flip_turn()
                    return True

            return False                                     # the piece the user wants to enter is not in the list

        # if it's blacks turn confirm piece is valid
        else:
            if piece != 'f' and piece != 'h':  # is the piece param valid for a white fairy piece
                return False
            if not self._game.get_sidelined_black_fairy_pieces():  # are there any fairy pieces remaining to add
                return False

            # count how many black rooks, knights, bishops, and queens have been captured
            num_special_pieces_captured = 0
            for pieces in self._game.get_captured_black_pieces():
                if isinstance(pieces, (Rook, Knight, Bishop, Queen)):
                    num_special_pieces_captured += 1

            # at least one special piece has to be captured for one fairy piece to be entered
            if num_special_pieces_captured < 1:
                return False

            # at least 2 special pieces must be captured to enter the second fairy piece
            if len(self._game.get_sidelined_black_fairy_pieces()) == 1:  # has one fairy piece already been entered
                if num_special_pieces_captured < 2:
                    return False

            # is the destination for the fairy piece valid
            if destination[1] != '8' and destination[1] != '7':  # is it among the two black home ranks
                return False
            if self._game.get_pos(destination) is not None:  # is the position occupied
                return False

            for fairy_piece in self._game.get_sidelined_black_fairy_pieces():

                # if the user wants to enter a black hunter is there a black hunter available
                if isinstance(fairy_piece, Hunter) and piece == 'h':
                    # place the black hunter in the destination
                    self._game.set_piece_on_board(fairy_piece, destination)
                    self._game.get_sidelined_black_fairy_pieces().remove(fairy_piece)  # remove the hunter from the sideline
                    self.flip_turn()
                    return True

                # if the user wants to enter the black falcon is there a black falcon available
                if isinstance(fairy_piece, Falcon) and piece == 'f':
                    # place the black hunter in the destination
                    self._game.set_piece_on_board(fairy_piece, destination)
                    self._game.get_sidelined_black_fairy_pieces().remove(fairy_piece)  # remove the falcon from the sideline
                    self.flip_turn()
                    return True

            return False  # the piece the user wants to enter is not in the list

    def display_board(self):
        """calls ChessBoard.display_board to print the board to the screen"""
        self._game.display_board()


def main():
    pass

if __name__ == '__main__':
    main()