import pytest
from board import Board
from pieces import *
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/./')


def test_piece_creation(board):
  b = board.matrix
  King(1,4,4,board)
  Queen(-1,3,3,board)
  Bishop(1,5,2,board)
  Knight(1,6,4,board)
  Rook(-1,0,0,board)
  Pawn(1,1,3,board)
  assert isinstance(b[4][4],King)
  assert b[4][4].color==1
  assert isinstance(b[3][3],Queen)
  assert b[3][3].color==-1
  assert isinstance(board.matrix[5][2], Bishop)
  assert isinstance(b[6][4],Knight)
  assert isinstance(b[0][0],Rook)
  assert isinstance(b[1][3],Pawn)

def test_illegal_king_moves(board):
  b = board.matrix
  King(1,4,4,board)
  board.move(4,4,7,4)
  assert isinstance(b[4][4],King)
  assert b[7][4]==0
  board.move(4,4,2,2)
  assert isinstance(b[4][4],King)
  assert b[2][2]==0

def test_king_moves_down(board):
  b = board.matrix
  King(1,4,4,board)
  board.move(4,4,5,4)
  assert b[4][4]==0
  assert isinstance(b[5][4],King)

def test_king_moves_up(board):
  b = board.matrix
  King(1,4,4,board)
  board.move(4,4,3,4)
  assert b[4][4]==0
  assert isinstance(b[3][4],King)

def test_king_moves_diag(board):
  b= board.matrix
  King(1,4,4,board)
  board.move(4,4,5,5)
  assert b[4][4]==0
  assert isinstance(b[5][5],King)
  board.player_to_move*=-1
  board.move(5,5,4,4)
  assert b[5][5]==0
  assert isinstance(b[4][4],King)
  board.player_to_move*=-1
  board.move(4,4,5,3)
  assert b[4][4]==0
  assert isinstance(b[5][3],King)
  board.player_to_move*=-1
  board.move(5,3,4,4)
  assert b[5][3]==0
  assert isinstance(b[4][4],King)

def test_illegal_queen_moves(board):
  b = board.matrix
  Queen(1,4,4,board)
  Queen(1,4,2,board)
  Queen(1,3,3,board)
  Queen(1,6,2,board)

  moves = [(4,4,7,5),
    (4,4,5,1),
    (4,4,4,1),
    (3,3,5,4),
    (4,4,2,2),
    (4,4,7,1),
    (6,2,5,0),
    (4,4,6,5),
    ]

  for squares in moves:
    board.move(squares[0],squares[1],squares[2],squares[3])
    assert b[squares[2]][squares[3]] == 0
    assert isinstance(b[squares[0]][squares[1]],Queen)
    assert board.player_to_move == 1


  board.move(4,4,3,3)
  assert isinstance(b[3][3],Queen)
  assert isinstance(b[4][4],Queen)
  assert board.player_to_move == 1

  board.move(6,2,2,6)
  assert b[2][6]==0
  assert isinstance(b[6][2],Queen)
  assert board.player_to_move == 1

def test_valid_queen_moves(board):
  b = board.matrix
  Queen(1,4,4,board)

  moves = [(4,4,0,0),
    (0,0,7,7),
    (7,7,6,6),
    (6,6,7,7),
    (7,7,3,7),
    (3,7,5,7),
    (5,7,3,7),
    (3,7,0,4),
    (0,4,4,4)
    ]

  for squares in moves:
    board.player_to_move=1
    board.move(squares[0],squares[1],squares[2],squares[3])
    assert isinstance(b[squares[2]][squares[3]],Queen)
    assert 0 == b[squares[0]][squares[1]]
    assert board.player_to_move == -1

  Queen(-1,2,6,board)
  board.move(2,6,4,4)
  assert isinstance(b[4][4],Queen)
  assert b[2][6]==0
  assert board.player_to_move==1

def test_illegal_rook_moves(board):
  b = board.matrix
  Rook(1,4,4,board)
  Queen(1,4,2,board)
  Queen(1,6,4,board)
  Queen(1,1,4,board)

  moves = [(4,4,7,5),
    (4,4,5,1),
    (4,4,4,1),
    (4,4,5,5),
    (4,4,2,2),
    (4,4,7,1),
    (4,4,0,4),
    (4,4,4,0),
    ]

  for squares in moves:
    board.move(squares[0],squares[1],squares[2],squares[3])
    assert b[squares[2]][squares[3]] == 0
    assert isinstance(b[squares[0]][squares[1]],Rook)
    assert board.player_to_move == 1

def test_valid_rook_moves(board):
  b = board.matrix
  Rook(1,4,4,board)

  squares = [
    (4,4),
    (0,4),
    (0,0),
    (6,0),
    (6,6),
    (6,0),
    (0,0),
    (0,3),
    (5,3),
    (0,3),
    (0,0),
    (4,0),
    (4,4),
    ]

  for i in range (1,len(squares)):
    board.player_to_move = 1
    r1, c1 = squares[i-1][0],  squares[i-1][1]
    r2, c2 = squares[i][0],  squares[i][1]
    board.move(r1,c1,r2,c2)
    assert isinstance(b[r2][c2],Rook)
    assert 0 == b[r1][c1]
    assert board.player_to_move == -1

def test_illegal_knight_moves(board):
  b = board.matrix
  Knight(1,4,4,board)

  moves = [(7,5),
    (3,3),
    (6,6),
    (5,4),
    (4,5),
    (6,2),
    (6,1),
    (6,4),
    (6,7),
    (4,2),
    (4,1),
    (0,0),
    (7,7)
    ]

  for squares in moves:
    board.move(4,4,squares[0],squares[1])
    assert b[squares[0]][squares[1]] == 0
    assert isinstance(b[4][4],Knight)
    assert board.player_to_move == 1


def test_valid_knight_moves(board):
  b = board.matrix
  Knight(1,4,4,board)

  squares = [
    (4,4),
    (5,6),
    (3,7),
    (1,6),
    (0,4),
    (1,2),
    (0,0),
    (2,1),
    (4,2),
    (5,4),
    (3,3),
    (5,2),
    (4,4)
    ]

  for i in range (1,len(squares)):
    board.player_to_move = 1
    r1, c1 = squares[i-1][0],  squares[i-1][1]
    r2, c2 = squares[i][0],  squares[i][1]
    board.move(r1,c1,r2,c2)
    assert isinstance(b[r2][c2],Knight)
    assert 0 == b[r1][c1]
    assert board.player_to_move == -1


def test_illegal_bishop_moves(board):
  b = board.matrix
  Bishop(1,4,4,board)

  moves = [
    (7,5),
    (0,1),
    (0,2),
    (0,5),
    (3,4),
    (6,7),
    (7,6),
    (7,0),
    (0,7),
    ]

  for squares in moves:
    board.move(4,4,squares[0],squares[1])
    assert b[squares[0]][squares[1]] == 0
    assert isinstance(b[4][4],Bishop)
    assert board.player_to_move == 1

def test_valid_bishop_moves(board):
  b = board.matrix
  Bishop(1,4,4,board)

  squares = [
    (4,4),
    (3,3),
    (0,0),
    (2,2),
    (4,0),
    (0,4),
    (3,1),
    (5,3),
    (6,4),
    (3,7),
    (1,5),
    (0,6),
    ]

  for i in range (1,len(squares)):
    board.player_to_move = 1
    r1, c1 = squares[i-1][0],  squares[i-1][1]
    r2, c2 = squares[i][0],  squares[i][1]
    board.move(r1,c1,r2,c2)
    assert isinstance(b[r2][c2],Bishop)
    assert 0 == b[r1][c1]
    assert board.player_to_move == -1


def test_illegal_pawn_moves(board):
  b = board.matrix
  Pawn(1,6,4,board)

  moves = [
    (7,5),
    (0,1),
    (0,2),
    (0,5),
    (3,4),
    (6,7),
    (7,6),
    (7,0),
    (0,7),
    (3,4),
    (6,3),
    ]

  for squares in moves:
    board.move(6,4,squares[0],squares[1])
    assert b[squares[0]][squares[1]] == 0
    assert isinstance(b[6][4],Pawn)
    assert board.player_to_move == 1

  Pawn(-1,5,4,board)
  board.move(6,4,4,4)
  assert isinstance(b[6][4],Pawn)

def test_valid_pawn_moves(board):
  b = board.matrix
  Pawn(1,6,4,board)
  Pawn(-1,2,5,board)
  Pawn(-1,1,4,board)
  Pawn(-1,1,7,board)
  Queen(1,4,6,board)
  Queen(1,5,7,board)

  path = [[(6,4),
    (4,4),
    (3,4),
    (2,5),
    (1,4)
      ],[
    (1,7),
    (2,7),
    (3,7),
    (4,6),
    (5,7),
    (6,7)]]


  for squares in path:
    board.player_to_move *= -1
    for i in range (1,len(squares)):
      board.player_to_move *= -1
      r1, c1 = squares[i-1][0],  squares[i-1][1]
      r2, c2 = squares[i][0],  squares[i][1]
      board.move(r1,c1,r2,c2)
      print (r2,c2)
      assert isinstance(b[r2][c2],Pawn)
      assert 0 == b[r1][c1]

def test_en_passant(board):
  b = board.matrix
  Pawn(-1,4,5,board)
  Pawn(1,6,4,board)

  board.move(6,4,4,4)
  board.move(4,5,5,4)
  assert 0 == b[4][5]
  assert 0 == b[4][4]
  assert isinstance(b[5][4],Pawn)

  Pawn(1,6,0,board)
  Pawn(-1,4,1,board)
  board.move(6,0,4,0)
  board.move(4,1,5,0)
  assert 0 == b[4][1]
  assert 0 == b[4][0]
  assert isinstance(b[5][0],Pawn)

def test_kingside_castling_legal(board):
  b = board.matrix
  King(1,7,4,board)
  King(-1,0,4,board)
  Rook(1,7,7,board)
  Rook(-1,0,7,board)
  Pawn(1,6,5,board)  #otherwise white's rook will make black castling illegal

  board.move(7,4,7,6)
  board.move(0,4,0,6)

  assert 0 == b[7][4]
  assert 0 == b[0][4]
  assert 0 == b[7][7]
  assert 0 == b[0][7]
  assert isinstance(b[7][6],King)
  assert isinstance(b[0][6],King)
  assert isinstance(b[7][5],Rook)
  assert isinstance(b[0][5],Rook)

def test_qside_castling_legal(board):
  b = board.matrix
  King(1,7,4,board)
  King(-1,0,4,board)
  Rook(1,7,0,board)
  Rook(-1,0,0,board)
  Pawn(1,6,3,board)

  board.move(7,4,7,2)
  board.move(0,4,0,2)

  assert 0 == b[7][4]
  assert 0 == b[0][4]
  assert 0 == b[7][0]
  assert 0 == b[0][0]
  assert isinstance(b[7][2],King)
  assert isinstance(b[0][2],King)
  assert isinstance(b[7][3],Rook)
  assert isinstance(b[0][3],Rook)

def test_castling_illegal(board):
  b = board.matrix
  King(1,7,4,board)
  Rook(1,7,7,board)
  Knight(-1,5,4,board)
  board.move(7,4,7,6)
  assert b[7][6]==0
  b[5][4]=0
  Rook(-1,2,4,board)
  board.move(7,4,7,6)
  assert b[7][6]==0


  board.move(7,4,7,5)
  board.player_to_move=1
  board.move(7,5,7,4)
  board.player_to_move=1
  board.move(7,4,7,6)
  assert b[7][6]==0

  b[7][4].moved=False
  board.move(7,7,5,7)
  board.player_to_move=1
  board.move(5,7,7,7)
  board.player_to_move=1
  assert b[7][6]==0

def test_undo_move():
  board=Board()
  b=board.matrix

  board.move(6,4,4,4)
  board.move(1,4,3,4)
  board.move(7,6,5,5)
  board.move(0,1,2,2)
  board.move(7,5,4,2)
  board.move(0,6,2,5)
  board.move(7,4,7,6)

  assert board.player_to_move == -1
  board.undo_move()
  assert b[7][6]==0
  assert b [7][5]==0
  assert board.player_to_move == 1
  board.undo_move()
  assert b[2][5] ==0
  assert board.player_to_move ==-1
  assert isinstance(b[0][6],Knight)

@pytest.fixture()
def board():
  b = Board()
  b.clear()
  return b

