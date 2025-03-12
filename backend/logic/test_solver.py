import pytest 
from copy import deepcopy
from sudoku import Sudoku
import numpy as np

from exceptions import InvalidBoard, UnsolvableBoard
from solver import SudokuSolver

# Fix a valid board
valid_board = [
    [5, 3, None, None, 7, None, None, None, None],
    [6, None, None, 1, 9, 5, None, None, None],
    [None, 9, 8, None, None, None, None, 6, None],
    [8, None, None, None, 6, None, None, None, 3],
    [4, None, None, 8, None, 3, None, None, 1],
    [7, None, None, None, 2, None, None, None, 6],
    [None, 6, None, None, None, None, 2, 8, None],
    [None, None, None, 4, 1, 9, None, None, 5],
    [None, None, None, None, 8, None, None, 7, 9]
]

solved_board = [
    [5, 8, 4, 1, 3, 7, 6, 2, 9],
    [2, 1, 7, 8, 6, 9, 3, 5, 4],
    [3, 9, 6, 2, 5, 4, 7, 1, 8],
    [4, 7, 2, 9, 8, 6, 1, 3, 5],
    [6, 3, 8, 4, 1, 5, 2, 9, 7],
    [9, 5, 1, 3, 7, 2, 4, 8, 6], 
    [7, 4, 3, 5, 9, 1, 8, 6, 2],
    [8, 2, 5, 6, 4, 3, 9, 7, 1],
    [1, 6, 9, 7, 2, 8, 5, 4, 3]
]

unsolvable_board = [
    [5, 8, 9, 1, 3, 7, 6, 2, None], # Should be 9, but it wouldn't be a valid move
    [2, 1, 7, 8, 6, 9, 3, 5, None], # 4
    [3, None, 6, 2, 5, 4, 7, 1, 8],
    [4, 7, 2, 9, 8, 6, 1, 3, 5],
    [6, 3, 8, 4, 1, 5, 2, 9, 7],
    [9, 5, 1, 3, 7, 2, 4, 8, 6], 
    [7, 4, 3, 5, 9, 1, 8, 6, 2],
    [8, 2, 5, 6, 4, 3, 9, 7, 1],
    [1, 6, None, 7, 2, 8, 5, 4, 3]
]

box_dims = (3, 3)
seed = 100

@pytest.fixture
def sudoku():
    """Fixture to create a Sudoku instance before each test"""
    return SudokuSolver(valid_board, box_dims)

# Test board validation
def test_valid_board():
    assert SudokuSolver(valid_board, box_dims)

def test_invalid_board():
    invalid_board = [row[:] for row in valid_board]
    invalid_board[0][1] = 5
    with pytest.raises(InvalidBoard):
        SudokuSolver(invalid_board, box_dims)

@pytest.mark.parametrize("cell, size, expected",[
    (None, 9, True), 
    (5, 9, True), 
    (1, 9, True), 
    (9, 9, True), 
    (0, 9, False), 
    ("X", 9, False)
])
def test_is_valid_cell(sudoku, cell, size, expected):
    assert sudoku.is_valid_cell(cell, size) == expected

def test_check_rows(sudoku):
    valid_rows = [
        [1, 2, 3, 4],
        [4, 3, 2, 1],
        [None, 1, None, 2]
    ]
    invalid_rows_1 = [
        [1, 2, 3, 3],
        [4, 3, 2, 1],
    ]
    invalid_rows_2 = [
        [1, 2, 3, 4],
        [4, 3, 2, "X"],
    ]
    assert sudoku.check_rows(valid_rows)
    assert sudoku.check_rows(invalid_rows_1) is False
    assert sudoku.check_rows(invalid_rows_2) is False

@pytest.mark.parametrize("box ,expected", [
    ([[1,None,3],[4,5,6],[7,8,9]],True), 
    ([[1,2,3],[4,5,6],[7,8,9]],True), 
    ([[1,2,3],[4,10,6],[7,8,9]],False), 
    ([[1,2,3],[4,10,6],[7,8,9]],False), 
    (valid_board, True)
])
def test_check_boxes(sudoku, box, expected):
    assert sudoku.check_boxes(box, box_dims) == expected


# Test Logic
@pytest.mark.parametrize("cell, expected",[
    ((0,0), 0),
    ((1,4), 1), 
    ((2,8), 2),
    ((3,0), 3),
    ((4,4), 4), 
    ((5,6), 5),
    ((7,1), 6),
    ((8,5), 7), 
    ((7,6), 8)
])
def test_get_box_index(sudoku, cell, expected):
    assert sudoku.get_box_idx(cell) == expected

def test_fill_bags(sudoku):
    r_bags = sudoku.row_bags
    c_bags = sudoku.col_bags
    b_bags = sudoku.box_bags
    assert len(r_bags[0]) == 3
    assert len(r_bags[7]) == 4
    assert len(c_bags[0]) == 5
    assert len(c_bags[6]) == 1
    assert len(b_bags[4]) == 4
    assert len(b_bags[8]) == 5

def test_make_and_undo_move(sudoku):
    initial_board = deepcopy(sudoku.board)

    sudoku.make_move((0,2,2))
    assert sudoku.board[0][2] == 2
    assert 2 in sudoku.row_bags[0]
    assert 2 in sudoku.col_bags[2]
    assert 2 in sudoku.box_bags[0]


    sudoku.make_move((8,5,1))
    assert sudoku.board[8][5] == 1
    assert 1 in sudoku.row_bags[8]
    assert 1 in sudoku.col_bags[5]
    assert 1 in sudoku.box_bags[7]

    sudoku.undo_move((8,5,1))
    sudoku.undo_move((0,2,2))
    assert sudoku.board[8][5] is None
    assert sudoku.board[0][2] is None

    assert 1 not in sudoku.row_bags[8]
    assert 1 not in sudoku.col_bags[5]
    assert 1 not in sudoku.box_bags[7]
    assert 2 not in sudoku.row_bags[0]
    assert 2 not in sudoku.col_bags[2]
    assert 2 not in sudoku.box_bags[0]

    assert initial_board == sudoku.board

def test_get_valid_moves(sudoku):
    valid_moves = sudoku.get_all_valid_moves()

    num_none_cells = sum(cell is None for row in sudoku.board for cell in row)
    assert len(valid_moves) == num_none_cells

    assert len(valid_moves[(2,0)]) == 2
    assert len(valid_moves[(8,2)]) == 5
    assert (0,0) not in valid_moves
    assert (7,5) not in valid_moves

    # Making moves changes available moves
    sudoku.make_move((6,0,1))
    sudoku.make_move((7,0,2))
    valid_moves = sudoku.get_all_valid_moves()
    assert (2,0) not in valid_moves

    # Undoing moves changes available moves
    sudoku.undo_move((6,0,1))
    valid_moves = sudoku.get_all_valid_moves()
    assert len(valid_moves[(2,0)]) == 1

def is_valid_solution(board, box_dims):
    """
    Returns whether board is correctly solved
    """
    b_size = len(board)
    box_width, box_height = box_dims
    
    board = np.array(board, dtype=object)
    b_transpose = board.T
    expected_numbers = set(range(1, b_size + 1))

    def is_expected(numbers):
        return set(numbers) == expected_numbers

    # Check rows and cols
    for i in range(b_size):
        row = board[i]
        col = b_transpose[i]
        if not (is_expected(row) and is_expected(col)):
            return False
        
    # Check boxes
    for start_row in range(0, b_size, box_height):
        for start_col in range(0, b_size, box_height):
            box = board[start_row: start_row + box_height, start_col: start_col + box_width].flatten()
            if not is_expected(box):
                return False
    
    return True


def test_solve():
    # Test solvable boards
    board = Sudoku(3).difficulty(0.5).board
    sudoku_solver = SudokuSolver(board, box_dims)
    solution = sudoku_solver.get_solution()
    assert is_valid_solution(solution, box_dims)

    board = Sudoku(3).difficulty(0.5).board
    sudoku_solver = SudokuSolver(board, box_dims)
    solution = sudoku_solver.get_solution()
    assert is_valid_solution(solution, box_dims)

    sudoku_solver = SudokuSolver(solved_board, box_dims)
    solution = sudoku_solver.get_solution()
    assert is_valid_solution(solution, box_dims)

    # Test unsolvable board
    sudoku = SudokuSolver(unsolvable_board, box_dims)
    with pytest.raises(UnsolvableBoard):
        sudoku.get_solution()
