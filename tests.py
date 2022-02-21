from game import *

def test_valid_word():
    assert(valid_word('hello', dictionary) == True)
    assert(valid_word('heLLo', dictionary) == True)

def test_invalid_word():
    assert(valid_word('Christina', dictionary) == False)

def test_find_words():
    valid_add_words = ['AD', 'ADD', 'DAD']
    valid_blah_words = ['AB', 'AH', 'AL', 'ALB', 'BA', 'BAH', 'BAL', 'BLAH', 'HA', 'LA', 'LAB']

    assert(find_words(['D', 'A', 'D'], dictionary) == valid_add_words)
    assert(find_words(['B', 'L', 'A', 'H'], dictionary) == valid_blah_words)

def test_valid_board():
    test_board = []
    for i in range(15):
        test_board.append([None] * 15)

    test_board[7][7] = 'A'
    test_board[7][8] = 'H'

    assert(validate_board(test_board) == True)

def test_invalid_board():
    def gen_empty_board():
        empty_board = []
        for i in range(15):
            empty_board.append([None] * 15)

        return empty_board

    one_tile = gen_empty_board()
    one_tile[7][7] = 'A'
    assert(validate_board(one_tile) == False)

    disconnected = gen_empty_board()
    disconnected[7][7] = 'A'
    disconnected[10][10] = 'B'
    assert(validate_board(disconnected) == False)

    no_tiles = gen_empty_board()
    assert(validate_board(no_tiles) == False)
