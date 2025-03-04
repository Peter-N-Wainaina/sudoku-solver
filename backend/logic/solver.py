import numpy as np
from math import floor
from exceptions import InvalidBoard, UnsolvableBoard

class SudokuSolver(object):
    def __init__(self, board, box_dims):
        """
        board: n by n matrix of Ints or None 
        box_dims: (k, m), the dimensions of the boxes within the board eg 3 by 3
                  for a 9 by 9 board.
        Precondition: k and m must fully divide n 
        """
        self.size = len(board)
        self.box_width,self.box_height = box_dims
        assert self.size == self.box_height * self.box_width, "Board size must be valid (perfect square)"
        if not self._is_valid_board(board, box_dims):
            raise InvalidBoard("Invalid Board")

        self.board = board
        self.row_bags = [set() for _ in range(self.size)]
        self.col_bags = [set() for _ in range( self.size)] 
        self.box_bags = [set() for _ in range ( int((self.size / self.box_height) * (self.size / self.box_width)))]  
        self.fill_bags()

    def get_box_idx(self, cell):
        r, c = cell
        boxes_across = self.size / self.box_width
        boxes_down = self.size / self.box_height
        return int((floor(r // boxes_down)) * boxes_across) + floor(c // boxes_across)

    def fill_bags(self):
        for row in range(self.size):
            for col in range(self.size):
                cell = self.board[row][col]
                if cell is not None: 
                    self.row_bags[row].add(cell)
                    self.col_bags[col].add(cell)
                    box_idx = self.get_box_idx((row, col))
                    self.box_bags[box_idx].add(cell)

    def is_valid_cell(self, cell, size):
        return cell is None or \
        (isinstance(cell,int) and cell in range (1, size + 1))
                    
    def check_rows(self, board):
        for row in board:
            row_length = len(row)
            seen = set()
            for cell in row:
                if cell is not None:
                    if cell in seen or not self.is_valid_cell(cell, row_length):
                        return False
                    seen.add(cell)
        return True
    
    def check_boxes(self, board, box_dims):
        board_np = np.array(board, dtype=object)
        board_size = len(board)
        box_width, box_height = box_dims
        max_num = box_width * box_height

        for start_row in range(0, board_size, box_height):
            for start_col in range(0, board_size, box_width):
                box = board_np[start_row: start_row + box_height, start_col: start_col + box_width].flatten()
                box_values = [cell for cell in box if cell is not None]
                has_dups = len(box_values) != len(set(box_values))
                has_invalids = not all(self.is_valid_cell(cell, max_num) for cell in box_values)

                if has_dups or has_invalids:
                    return False
        return True

    def _is_valid_board(self, board, box_dims):
        """
        Returns True if board is a valid board, false otherwise.
        """
        b_transposed = np.array(board).T
        return (self.check_rows(board) and
                self.check_rows(b_transposed) and
                self.check_boxes(board, box_dims)
        )
    
