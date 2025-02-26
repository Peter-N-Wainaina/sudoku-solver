import numpy as np
from math import floor

class Sudoku(object):
    
    def __init__(self, board, box_dims):
        """
        board: n by n matrix of Ints or None 
        box_dims: (k, m), the dimensions of the boxes within the board eg 3 by 3
                  for a 9 by 9 board.
        Precondition: k and m must fully divide n 
        """
        assert len(board) % box_dims[0] == 0 and len(board)% box_dims[1] == 0
        if self._is_valid_board(board, box_dims): #TODO:Maybe change to a try block 
            self.board = board
            self.size = len(board)
            self.box_width,self.box_height = box_dims
            self.row_bags = [set() for _ in range(self.size)]
            self.col_bags = [set() for _ in range( self.size)] 
            self.box_bags = [set() for _ in range ( int((self.size / self.box_height) * (self.size / self.box_width)))]  
            self._fill_bags()
        else:
            raise self.InvalidBoard
        
    class InvalidBoard(Exception):
        pass

    class UnsolvableBoard(Exception):
        pass

    def _get_box(self, cell):
        r, c = cell
        boxes_across = self.size / self.box_width
        boxes_down = self.size / self.box_height
        return int((floor(r / boxes_down)) * boxes_across) + floor(c / boxes_across) #We first get the layer of boxes the cell is in, then how deep into the layer it is.

    def _fill_bags(self):
        for row in range(self.size):
            for col in range(self.size):
                cell = self.board[row][col]
                if cell is not None: 
                    self.row_bags[row].add(cell)
                    self.col_bags[col].add(cell)
                    box_idx = self._get_box((row, col))
                    self.box_bags[box_idx].add(cell)
                    
    def possible_moves(self):
        """
        Returns a list of triples (i, j, k). (i,j) is the position in board where
        k is a valid move.
        """
        valid_moves = {x for x in range(1, self.size + 1)}
        pos_moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] is None:
                    box = self._get_box((row, col))
                    r_bag = self.row_bags[row] 
                    c_bag = self.col_bags[col]
                    b_bag = self.box_bags[box]
                    cell_moves = valid_moves - (r_bag | c_bag | b_bag)
                    for move in cell_moves:
                        pos_moves.append((row, col, move))
        return pos_moves
    
    def make_move(self, move):
        i, j, k = move 
        assert self.board[i][j] is None  

        self.board[i][j] = k
        b_idx = self._get_box((i,j))
        self.row_bags[i].add(k)
        self.col_bags[j].add(k)
        self.box_bags[b_idx].add(k)

    def undo_move(self, move):
        i, j, k = move 
        assert self.board[i][j] is not None 

        self.board[i][j] = None
        b_idx = self._get_box((i,j))
        self.row_bags[i].remove(k)
        self.col_bags[j].remove(k)
        self.box_bags[b_idx].remove(k)

    def is_solved(self):
        """
        Returns True if board is solved 
        """
        #Main Insight: If board is full, all bags (row, col or box)
        #are of length SIZE, then it is solved. This assumes that 
        #it was filled correctly to beging with. 
        for bag in self.col_bags: # can also check row, or box
            if len(bag) != self.size:
                return False
        return True


    def solve(self):
        """
        Solves self.board
        """
        if self.is_solved():
            return self.board
        
        moves = self.possible_moves()
        if moves == []:
            return None
        
        for move in moves:
            self.make_move(move)
            if self.solve() is not None:
                return self.board
            self.undo_move(move)
        return None


    def _is_valid_board(self, board, box_dims):
        """
        Returns True if board is a valid board, false otherwise.
        """
        n = len(board)
        box_row, box_col = box_dims

        def invalid_cell(cell, bag):
           return not ( (type(cell) == int and (cell in range (1, n + 1)) and cell not in bag )  or cell is None)
            
        def check_rows(board):
            for row in board:
                r_bag = set()
                for cell in row:
                    if invalid_cell(cell,r_bag):
                        return False
                    r_bag.add(cell)
            return True
                    
        def check_boxes(board):
            for start_row in range(0, n, box_row):
                for start_col in range(0, n, box_col):
                    box_bag = set()
                    
                    for row in range(start_row, start_row + box_row):
                        for col in range(start_col, start_col + box_col):
                            cell = board[row][col]
                            if invalid_cell(cell,box_bag):
                                return False
                            box_bag.add(cell)
            return True
        b_transposed = [[row[i] for row in board] for i in range(len(board[0]))]
        return check_rows(board) and check_rows(b_transposed) and check_boxes(board)

    def print_board(self):
        """
        Prints a formatted  n by n board to terminal
        """
        n = self.size
        b_str = ""
        for i in range(n):
            row = "|"
            for j in range(n):
                cell = str(self.board[i][j])
                row +=  cell + " |"
            b_str += (row  + "\n")
            b_str += ("_"*len(row) + "\n")
        print(b_str)
            












        