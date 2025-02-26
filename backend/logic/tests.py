from sudoku import Sudoku
import solver

def read_board(text_file):
    try: 
        with open(text_file) as file:
            contents = file.readlines()
            return contents
    except Exception as e:
        print(f"File Open Failed: {e}")

def create_board_from_file(file_name,board_size):
    contents = read_board(file_name)
    board = [[None for _ in range(board_size)] for _ in range(board_size)]
    for line in contents:
        line = line.replace(",","").strip()
        i,j,k = int(line[0]),int(line[1]),int(line[2])
        board[i][j] = k
    return board

def compare_lists(list1, list2):
    """
    Returns True if the lists have the same elements. 
    Order doesn't matter
    """
    return set(list1)== set(list2)

valid_1 = create_board_from_file("data/valid_board_1.txt", 9)
valid_1 = solver.Sudoku(valid_1, (3,3))
assert valid_1.possible_moves() == []
assert valid_1._get_box((0,3)) == 1
assert valid_1._get_box((8,7)) == 8
assert valid_1._get_box((5,5)) == 4
assert valid_1.is_solved()

valid_2 = create_board_from_file("data/valid_board_2.txt", 9)
valid_2 = solver.Sudoku(valid_2, (3,3))
moves = valid_2.possible_moves()
assert  compare_lists(moves, [ (8,7,7), (8,8,9), (5,5,4)])
row = [1,2,3,4,5,6,8]
assert compare_lists(row, valid_2.row_bags[8])

valid_2.make_move((8,8,9))
moves = valid_2.possible_moves()
assert  compare_lists(moves, [ (8,7,7), (5,5,4)])
row = [1,2,3,4,5,6,8,9]
box = [1,2,3,4,5,6,8,9]
assert compare_lists(row, valid_2.row_bags[8])
assert compare_lists(box, valid_2.box_bags[8])

valid_2.undo_move((0,0,5))
moves = valid_2.possible_moves()
assert  compare_lists(moves, [ (8,7,7), (0,0,5), (5,5,4)])
assert not valid_2.is_solved()


assert valid_2.solve() is not None
valid_3 = create_board_from_file("data/valid_board_2.txt", 9)
valid_3 = solver.Sudoku(valid_3, (3,3))
valid_3.make_move((8,7,7))
valid_3.make_move((8,8,9))
valid_3.make_move((5,5,4))
assert valid_3.board == valid_2.board

# puzzle = Sudoku(3).difficulty(0.5)
# puzzle.show()
# print(puzzle.board)

# valid_3 = solver.Sudoku(puzzle.board, (3,3))
# valid_3.solve()