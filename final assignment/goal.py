"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Goal class hierarchy.
"""

from typing import List, Tuple
from block import Block


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError

class PerimeterGoal(Goal):
    """A goal to alocate the largest amount of units of a specific colour at
    the outer perimeter of the board.
    """

    def description(self) -> str:
        """It returns what the player must do for this goal.
        """
        return "You must alocate the largest amount of units of the target \
                colour at the outer perimeter of the board."

    def score(self, board: Block) -> int:
        """ This is an override to the method on the parent class. It returns
        the score for this goal, given a board.
        """
        flat_board = board.flatten()
        # This variable represent the number of squares the board have in
        # in either dimension (since it is square, its the same).
        edge = len(flat_board)
        points = 0
        for row in range(edge):
            if flat_board[row][0] == self.colour:
                points += 1
            if flat_board[row][edge - 1] == self.colour:
                points += 1
        for col in range(edge):
            if flat_board[0][col] == self.colour:
                points += 1
            if flat_board[edge - 1][col] == self.colour:
                points += 1

        return points


class BlobGoal(Goal):
    """A goal to create the largest connected blob of this goal's target
    colour, anywhere within the Block.
    """

    def description(self) -> str:
        """It returns what the player must do for this goal.
        """
        return "You must create the largest connected blob of the target \
               colour."

    def score(self, board: Block) -> int:
        """ This is an override to the method on the parent class. It returns
        the score for this goal, given a board.
        """
        return 148

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
           -1  if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        pass


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer'
        ],
        'max-attributes': 15
    })
