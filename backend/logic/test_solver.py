import pytest 
from exceptions import InvalidBoard
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
box_dims = (3, 3)


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
