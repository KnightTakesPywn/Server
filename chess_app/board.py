import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/./')

from pieces import Rook,Knight,Bishop,Queen,King,Pawn

class Board:
  def __init__(self):
    self.player_to_move = 1 # as per custom for app, 1 is white, and -1 is black.
    self.moves = []
    self.matrix = [[0 for j in range (8)] for i in range (8)]
    pieces = (Rook,Knight,Bishop,Queen,King,Bishop,Knight,Rook)
    for i in range (8):
      for j in range (2):
        if j == 0:
          color = 1
          row1 = 6
          row2 = 7
        else:
          color = -1
          row1=1
          row2 = 0
        self.matrix[row1][i] = Pawn(color,row1,i,self)
        self.matrix[row2][i] = pieces[i](color,row2,i,self)
    self.EP=False
    self.white_king=self.matrix[7][4]
    self.black_king=self.matrix[0][4]
    self.can_castle = {"w00":True,"b00":True,"w000":True,"b000":True} ##  00 and 000 are chess shorthand for castling kingside and queenside, respectively


  def __repr__(self):
    s = ""

    # for i in range(7, -1, -1):
    for i in range (8):
      s += f"c={i}  "
    s += "\n"
    for i in range(8):
      for j in range (8):
        s += str(self.matrix[i][j])
        s += "   "
        if self.matrix[i][j] == 0:# or abs(self.matrix[i][j].color) == self.matrix[i][j].color:
          s+= " "
      s += f"  r={i} \n"
    return s

  #################################################

  def undo_move(self):
    self.player_to_move *= -1
    move = self.moves.pop()
    if move[6] == "0-0" or move[6]== "0-0-0":  ##  Undoing castling requires a good deal of special logic
      row = move[1]
      color = move[2]
      if move[6] == "0-0": #kingside
        squares = (King(color,row,4,self),0,0,Rook(color,row,7,self))
        def col_func (j): ## a quick helper function to grab the appropriate columns on the matrix
          return 4+j
        rangee=4
      else:
        squares =(King(color,row,4,self),0,0,0,Rook(color,row,0,self)) #queenside
        def col_func(j):
          return 4-j
        rangee=5
      for i in range (rangee):
        self.matrix[row][col_func(i)]=squares[i]
    else:  #  If the last move wasn't castling, undo the piece move, and if it captured something, put the captured piece back on the board.
      self.matrix[move[0]][move[1]] = self.matrix[move[2]][move[3]]
      self.matrix[move[2]][move[3]] = move[4]
      if move[5] == True: #If there was an EnPassant capture, put a pawn on the appropriate square
        color = self.matrix[move[0]][move[1]].color
        self.matrix[move[0]][move[3]] = Pawn(-1*color,move[0],move[3])


  def clear(self):
    """blanks the board.   Mostly for testing purposes, but could also be used for a potential future setup-board feature"""
    self.matrix = [[0 for j in range (8)] for i in range (8)]

  def move (self, r1,c1,r2=None,c2=None):
    """moves a piece from r1,c1 to r2,c2.  Modifies board matrix and player to move appropriately, and returns True if a legal move was successfully made"""
    if r2 == None:
      r1, c1, r2, c2 = r1[0], r1[1], c1[0], c1[1]
    piece = self.matrix[r1][c1]
    if piece == 0 or piece.color != self.player_to_move:
      return False
    moved = self.matrix[r1][c1].move(r2,c2,self)
    if moved:
      self.player_to_move *= -1
      return True
    return False

  def _is_check(self,king):
    """returns true if the king is in check, and false if it isn't"""
    results = False
    def in_bounds(row,column):  ##  A quick helper function to avoid index out of bounds errors
      return -1<row<8 and -1<column<8
    direction = (0,0)
    possible_directions = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)] ## all possible unit vectors when looking for checks from bishops, rooks, and queens
    for j in range (8):
      direction = possible_directions[j]
      for i in range (1,8):
        r = king.row+direction[0]*i
        c = king.column+direction[1]*i
        if not in_bounds(r, c):
          break  ##  If we're off the board in our given direction, we don't need to proceed further
        else:
          if self.matrix[r][c] !=0:
            if self.matrix[r][c].color != king.color: #we've found a piece, but is it hostile?
              piece = self.matrix[r][c]
              if j < 4:  ## our first 4 unit vectors look for rook moves
                if isinstance(piece,Rook) or isinstance(piece,Queen):
                  results = True
                else:
                  break
              else:  ## our last 4 unit vectors look for bishop moves.
                if isinstance(piece,Bishop) or isinstance(piece,Queen):
                  results = True
                else:
                  break
            else:
              break # all of the breaks here indicate that we've found the first piece on the rank/file/diagonal, and it's not a threat to capture the king.  No need to continue looking in that direction.

      ##looking for Knight checks.  (Note:  we're still inside the j for loop.)
      knight_moves = [(2,1),(2,-1),(1,2),(1,-2),(-1,2),(-1,-2),(-2,1),(-2,-1)]
      move = knight_moves[j]
      x,y = move[0],move[1]
      if in_bounds(king.row+x,king.column+y):
        piece = self.matrix[king.row+x][king.column+y]
        if isinstance(piece,Knight) and piece.color != king.color:
          results = True

    ##looking for pawn checks
    for i in range (2):
      if in_bounds(king.row-king.color,king.column + 2*i -1):
        piece = self.matrix[king.row-king.color][king.column + 2*i -1]
        if isinstance(piece,Pawn) and piece.color != king.color:
          results = True

    ##looking for illegal king checks
    for i in range (-1,2):
      for j in range (-1,2):
        if in_bounds(king.row+i,king.column+j):
          piece = self.matrix[king.row+i][king.column+j]
          if isinstance(piece,King) and piece.color != king.color:
            results = True
    if results == True:
      self.player_to_move *= -1
    return results  # no checks have been found.

  def objectify(self):
    def objectify_piece(piece):
      if piece == 0:
        results = None
      else:
        results = {}
        results['name']=str(piece)
        results['type']=piece.typee
        results['color']=('white', 'black')[piece.color == -1]
        results['pos_row']=piece.row
        results['pos_col']=piece.column
      return results

    results = [[objectify_piece(self.matrix[i][j]) for j in range(8)] for i in range(8)]
    return results



  def pack(self):
    results = {}
    results["board"]=self.objectify()
    results["player_to_move"]=self.player_to_move
    results["moves"]=str(self.moves)
    results["can_castle"]=str(self.can_castle)
    return results

def unpack(packed_board):
  board = Board()
  board.clear()
  board.moves = eval(packed_board["moves"])
  board.can_castle = eval(packed_board["can_castle"])
  b = packed_board["board"]
  board.player_to_move = packed_board['player_to_move']
  m = board.matrix
  for i in range (8):
    for j in range (8):
      square = b[i][j]
      if square==None:
        m[i][j]=0
      else:
        color=(square["color"]=="white")*2-1
        row=square["pos_row"]
        column=square["pos_col"]
        if square["type"]=="rook":
          Rook(color,row,column,board)
        elif square["type"]=="knight":
          Knight(color,row,column,board)
        elif square["type"]=="bishop":
          Bishop(color,row,column,board)
        elif square["type"]=="queen":
          Queen(color,row,column,board)
        elif square["type"]=="pawn":
          Pawn(color,row,column,board)
        elif square["type"]=="king":
          kk=King(color,row,column,board)
          if color == 1:
            board.white_king=kk
          else:
            board.black_king=kk
  return board
