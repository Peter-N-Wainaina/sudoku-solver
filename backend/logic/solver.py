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
        self.board_size = len(board)
        self.box_width,self.box_height = box_dims
        assert self.board_size == self.box_height * self.box_width, "Board size must be valid (perfect square)"
        if not self.is_valid_board(board, box_dims):
            raise InvalidBoard("Invalid Board")

        self.board = board
        self.move_options= set(range(1, self.board_size + 1))
        self.row_bags = [set() for _ in range(self.board_size)]
        self.col_bags = [set() for _ in range( self.board_size)] 
        self.box_bags = [set() for _ in range ( int((self.board_size / self.box_height) * (self.board_size / self.box_width)))] 
        self.fill_bags()

    def get_box_idx(self, cell):
        r, c = cell
        boxes_across = self.board_size / self.box_width
        boxes_down = self.board_size / self.box_height
        return int((floor(r // boxes_down)) * boxes_across) + floor(c // boxes_across)

    def fill_bags(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
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

    def is_valid_board(self, board, box_dims):
        """
        Returns True if board is a valid board, false otherwise.
        """
        b_transposed = np.array(board, dtype=object).T
        return (self.check_rows(board) and
                self.check_rows(b_transposed) and
                self.check_boxes(board, box_dims)
        )

    def make_move(self, move):
        i, j, digit = move
        box_idx = self.get_box_idx((i,j))

        self.board[i][j] = digit
        self.row_bags[i].add(digit)
        self.col_bags[j].add(digit)
        self.box_bags[box_idx].add(digit)
        
    def undo_move(self, move):
        i, j, digit = move
        box_idx = self.get_box_idx((i,j))

        self.board[i][j] = None
        self.row_bags[i].remove(digit)
        self.col_bags[j].remove(digit)
        self.box_bags[box_idx].remove(digit)

    def get_valid_cell_moves(self, cell):
        i, j = cell
        box_idx = self.get_box_idx((i,j))

        row_bag = self.row_bags[i]
        col_bag = self.col_bags[j]
        box_bag = self.box_bags[box_idx]
        moves = set(self.move_options - (row_bag | col_bag | box_bag))
        return moves

    def get_all_valid_moves(self):
        valid_moves = {}
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] is None:
                    moves = self.get_valid_cell_moves((i,j))
                    if moves:
                        valid_moves[(i,j)] = moves
        return valid_moves

    def get_sorted_valid_moves(self):
        valid_moves = list(self.get_all_valid_moves().items())
        return sorted(valid_moves, key=lambda x: len(x[1]))

    def is_solved(self):
        expected_numbers = self.move_options  
        if any(None in row for row in self.board):
            return False
        
        return (all(bag == expected_numbers for bag in self.row_bags) and
                all(bag == expected_numbers for bag in self.col_bags) and
                all(bag == expected_numbers for bag in self.box_bags))

    def get_solution(self):
        """Finds a solution for the Sudoku board and returns it."""
        def _backtrack():
            if self.is_solved():
                return True
        
            for cell, moves_list in  self.get_sorted_valid_moves():
                row, col = cell
                for number in moves_list:
                    move = (row, col, number)
                    self.make_move(move)
                    if _backtrack():
                        return True
                    self.undo_move(move)
            return False

        if not _backtrack():
            raise UnsolvableBoard("This board is unsolvable")
        
        return self.board
           
    def print_board(self, board=None):
        if board is None:
            board = self.board
        
        n = len(board)
        b_str = ""  
        for i in range(n):
            row = "|"
            for j in range(n):
                cell = str(board[i][j])
                row +=  cell + " |"
            b_str += (row  + "\n")
            b_str += ("_"*len(row) + "\n")
        print(b_str)                  
