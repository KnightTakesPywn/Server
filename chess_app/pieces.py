class Piece:
  def __init__(self,color, val, typee, row,column, board_obj):
    """White pieces have a color of 1, black have a color of -1.  Val of 1 for pawn, 3 for knight, 4 for bishop, 5 for rook, 8 for king and 9 for queen.   Row and Column are the piece's position in the board matrix (bottom left being 7,0)"""
    self.val = val
    self.typee = typee
    self.color = color
    self.row=row
    self.column=column
    board_obj.matrix[row][column] = self


  def __str__(self):
    s=("w", "b")[self.color != 1]
    if self.val ==1 : s+= "p"
    if self.val ==3 : s+= "n"
    if self.val ==4 : s += "b"
    if self.val ==5 : s += "r"
    if self.val ==8 : s += "k"
    if self.val ==9 : s += "q"
    return s

  def move(self,row,column,board_obj):
    """ Default move function for all pieces."""
    board = board_obj.matrix
    legal_move = self._move(row,column,board_obj) # Does the move inputted comply with the piece's _move function?

    ## Logic for en-passant was initially handled here because the board object iteself was out of scope in the pawn's move function.  This should be refactored into the pawn's move function, but lack of time prevented it.
    EP = False
    if legal_move:
      if isinstance(self,Pawn) and abs (column-self.column)==1 and board[row][column] == 0: # Pawn is attempting to capture a piece
        legal_move = board[row][column] != 0  # Returns true in the event of a regular capture
        if not legal_move:  #  Handling for an en-passant capture
          if self.color==1:
            i = -1
          else:
            i =1
          legal_move = board_obj.moves[-1]=(row+i,column,row-i,column,0,False)
          if legal_move:
            board[row-i][column]=0
            EP = True ##  EP is added later ot board_obj.moves to make undoing an EP capture possible.

      if isinstance(self,King) and column-self.column==2: # when true, player is attempting to castle kingside
        board_obj.moves+= [("0-0", row, self.color)]

        legal_move = not board_obj._is_check(TestKingForCastling(self.color,self.row,self.column+1)) and not board_obj._is_check(TestKingForCastling(self.color,self.row,self.column))  # Castling rules are convoluted.  Can't castle if your king is in check, if it would put you in check, or even if the square your king jumps over would BE a check if your king stopped on it.
      elif isinstance(self,King) and column-self.column==-2: # Queenside castling is handled in a similar fashion.
        board_obj.moves +=[("0-0-0", row, self.color)]
        legal_move = not board_obj._is_check(TestKingForCastling(self.color,self.row,self.column-1)) and not board_obj._is_check(TestKingForCastling(self.color,self.row,self.column))
      else:
        board_obj.moves+=[(self.row,self.column,row,column,board[row][column],EP)]  ##  If not a castling, append to list of moves in usual fashion

      piece = self
      if isinstance(self,Pawn):  #this block of code handles pawn promotion.   At the moment pawns auto-promote to queens.  At some point this should be updated to give the user a choice of pieces to promote to.
        if (self.color == 1 and row == 0) or (self.color==-1 and row ==7):
          piece = Queen(self.color,row,column)

      # move the piece
      board[self.row][self.column] = 0
      self.row, self.column, board[row][column] = row, column, piece

      #Update the board's saved king positions if king move
      if isinstance(self,King):
        if self.color == 1:
          board_obj.white_king = self
        else:
          board_obj.black_king = self

      #After making the move, am I in check?
      king = board_obj.white_king
      if self.color == -1: king = board_obj.black_king
      if legal_move: legal_move = not board_obj._is_check(king)

      if not legal_move:
        board_obj.undo_move()
        return False
    return legal_move


  def _ok_destination_square(self, square):
    """Validates the destination square is one the piece can move to, either because it's empty, or because an enemy piece is on it.  Function un-usable by pawns, because they can't capture by moving 1 square forward"""
    if square == 0:
      return True
    elif square.color != self.color:
      return True
    return False

  def can_move(self,row,column,board):
    """draws a straight line from the piece's current postion to the target square(non-inclusive).  Returns False if another piece is in the way, and true otherwise."""
    r, c = self.row, self.column
    x_vector = 0 if r==row else int((row-r)/abs(row-r))  # producing unit-vectors of -1, 0 or 1 to indicate nothing but direction of movement
    y_vector = 0 if c==column else int((column-c)/abs(column-c))
    while r+x_vector is not row or c + y_vector is not column:
      r, c = r + x_vector, c + y_vector
      if board[r][c] != 0:
        return False  ##  There's a piece on the board between where you are and the square you're trying to get to
    return True

class Pawn(Piece):
  def __init__ (self, color, row, column, board_obj):
    super().__init__(color,1, "pawn",row,column,board_obj)

  def _move(self,row,column, board_obj):
    board=board_obj.matrix
    legal_move = False
    rows_moved = self.row - row
    if column - self.column == 0: #pawn is not moved sideways
      if rows_moved == self.color and board[row][column] == 0:  #pushed 1 square forward in correct direction onto empty square
        legal_move = True
      if rows_moved == 2 * self.color: #pawn moved 2 squares
        if (self.color == -1 and self.row == 1) or (self.color == 1 and self.row ==6): #pawn on it's starting square
          legal_move = self.can_move(row,column,board)

    if abs(column - self.column) == 1 and rows_moved == self.color:  # capture attempted
      if self._ok_destination_square(board[row][column]):
        legal_move=True  #  Further handling for captures done in the piece.move function
    return legal_move

class Knight(Piece):
  def __init__ (self, color, row, column, board_obj):
    super().__init__(color,3,"knight",row,column,board_obj)

  def _move(self,row,column,board_obj):
    board=board_obj.matrix
    legal_move = False
    tup = (abs(self.row-row), abs(self.column - column))
    if tup == (2,1) or tup == (1,2):
      legal_move = self._ok_destination_square(board[row][column])
    return legal_move

class Rook(Piece):
  def __init__ (self, color, row, column, board_obj):
    super().__init__(color,5, "rook",row,column,board_obj)

  def _move(self,row,column,board_obj):
    board=board_obj.matrix
    legal_move = False
    if (self.row-row or self.column-column) and not (self.row-row and self.column - column): #moving on a row or a column, but not both:
      if self.can_move(row,column,board):
        legal_move = self._ok_destination_square(board[row][column])
    if legal_move:
      tup = ("b000","b00","w000","w00")
      index = int(2*self.row/7 + self.column/7)
      board_obj.can_castle[tup[index]]=False
    return legal_move

class  Bishop(Piece):
  def __init__ (self, color, row, column, board_obj):
    super().__init__(color,4, "bishop",row,column,board_obj)

  def _move(self,row,column,board_obj):
    board=board_obj.matrix
    legal_move=False
    if abs(self.row-row) == abs(self.column-column):
      if self.can_move(row,column,board):
        legal_move = self._ok_destination_square(board[row][column])
    return legal_move

class Queen(Piece):
  def __init__(self,color,row,column,board_obj):
    super().__init__(color,9,"queen",row,column,board_obj)

  def _move(self,row,column,board_obj):  ##copy-paste of logic for rook and Bishop
    board=board_obj.matrix
    legal_move=False
    if abs(self.row-row) == abs(self.column-column):
      if self.can_move(row,column,board):
        legal_move = self._ok_destination_square(board[row][column])

    if (self.row-row or self.column-column) and not (self.row-row and self.column - column):
      if self.can_move(row,column,board):
        legal_move = self._ok_destination_square(board[row][column])
    return legal_move

class King(Piece):
  def __init__(self,color,row,column,board_obj):
    super().__init__(color,8,"king",row,column,board_obj)

  def _move(self,row,column,board_obj):
    board=board_obj.matrix
    legal_move=False
    index = self.color+1
    index_modifier=0
    tup = ("b000","b00","w000","w00")
    if abs(self.row-row) <2 and abs(self.column-column) <2:
      legal_move = self._ok_destination_square(board[row][column])

    if self.row-row == 0 and abs (self.column - column) ==2: #castling attempted
      direction = int(0.5*(column-self.column))
      rook=(board[row][7], board[row][0])[direction == -1]
      if not isinstance(rook, Rook) or rook.color is not self.color:
        return False  ## If there's not  rook where we expect one, then you can't castle
      lm = board[row][column] == 0
      lm1 = board[row][column - direction] == 0
      lm2 = 0
      if direction == -1: #qside
        lm2 = board[row][self.column+3*direction]
        index_modifier=1
      can_castle = board_obj.can_castle[tup[index+index_modifier]]
      print (lm,lm1,lm2==0,can_castle)
      legal_move = lm and lm1 and lm2==0 and can_castle
      if legal_move:
        ## move the Rook
        board[rook.row][rook.column]=0
        board[row][column-direction]=rook
    if legal_move:
      board_obj.can_castle[tup[index]]=False
      board_obj.can_castle[tup[index+1]]=False
    return legal_move

class TestKingForCastling():
  def __init__(self,color,row,column):
    self.color=color
    self.row=row
    self.column=column
