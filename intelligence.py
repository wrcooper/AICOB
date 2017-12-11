import pygame

def values = [50, 500,  300,   300,  1000, 5000]
#            pawn rook knight bishop queen king

class Intelligence():
	def __init__(self, board, color, player):
		self.board = board
		self.color = color
		self.player = player # side of the board that this character is on, 1 = bottom, 2 = top
	
	def move(self, board):
		predict_board = copy.deepcopy(board)
		move = self.check_moves(predict_board, 0, 1)
		board.move_piece(move[0], move[1], move[2], move[3])
		
	def check_moves(self, board, depth, player):
		depth += 1
		for ra in range(1, 9):
			for fi in range(1, 9):

		'''
		move(board):
		iterate through list of valid moves:
			try move in a copy of the board
			result = pieces gained/lost
			move_opponent(newBoard)
			
		'''
				
			
		# check all possible moves for self, return best outcome
		# pawn capture = 50
		# rook capture = 500
		# knight capture = 300
		# bishop capture = 300
		# queen capture = 1000
		# king capture = 5000

	def generate_moves(self, board):
		movelist = []
		for ra in range(1, 9):
			for fi in range(1, 9):
				piece = board.board[ra][fi]
				for ra1 in range(1, 9):
					for fi1 in range(1, 9):
	
	def imprint(self, board):
		v_board = new V_Board()
		for ra in range(1, 9):
			for fi in range(1, 9):
				piece = board.board[ra][fi]
				v_piece = v_board.convert_piece(piece)
				v_board[ra][fi] = v_piece
				v_board.sort_piece(v_piece)
					
		return v_board
	
	def update_board(self, v_board):
		#TODO: update v_board with player moves

class V_Move():
	def __init__(self, piece, ra, fi, v_board):
		if ra < 1 or ra > 8 or fi < 1 or fi > 8:
			return 0
		self.value = v_board.check_value(ra, fi)
		self.ra1 = piece.ra
		self.fi1 = piece.fi
		self.ra2 = ra
		self.fi2 = fi


class V_Board():
	def __init__(self, my_color):
		self.board = [[0 for ra in range(9)] for y in range(9)]
		self.my_pieces = []
		self.opp_pieces = []
	
	def check_value(self, ra, fi):
		piece = self.board[ra][fi]
		if piece != 0:
			if piece.color == self.my_color:
				return -1 * piece.value
			else: 	
				return piece.value
			
	
	def sort_piece(self, piece):
		if piece == 0:
			return
		elif piece.color == self.my_color:
			self.my_pieces.append(piece)
		else:
			self.opp_pieces.append(piece)
	
	def has_piece(self, ra, fi):
		if self.board[ra][fi] = 0
			return False
		else:
			return True
			
	
	def convert_piece(self, piece):
		ra = piece.ra
		fi = piece.fi
		if piece == 0:
			return 0
		elif piece == Pawn():
			return V_Pawn(ra, fi)
		elif piece == Rook():
			return V_Rook(ra, fi)
		elif piece == Knight():
			return V_Knight(ra, fi)
		elif piece == Bishop():
			return V_Bishop(ra, fi)
		elif piece == King():
			return V_King(ra, fi)
		elif piece == Queen():
			return V_Queen(ra, fi)


class V_Piece():
	def __init__(self, ra, fi):
		self.ra = ra
		self.fi = fi
		# set value of piece
	
	def moves
		# return list of valid moves with associated values

class V_Pawn(V_Piece):
	def __init__(self, ra, fi):
		V_Piece.__init__(ra, fi)
		self.value = 50
		self.has_moved = False
	
	def moves(self, v_board):
		moves = []
		ra2 = self.ra + (self.direction * 1)
		fi2 = self.fi - 1
	
		moves.append(V_Move(self, ra2, self.fi))

		if not self.has_moved:
			moves.append(V_Move(self, self.ra + (self.direction * 2), self.fi))

		if v_board.hasPiece(ra2, self.fi + 1):
			moves.append(V_Move(self, ra2, self.fi + 1)

		if v_board.hasPiece(ra2, self.fi - 1):
			moves.append(V_Move(self, ra2, self.fi + 1))
			
class V_Rook(V_Piece):
	def __init__(self, ra, fi):
		V_Piece.__init__(ra, fi)
		self.value = 500
		self.has_moved = False
	
	def moves(self, v_board):
		moves = []
		
		for ra in range(self.ra, 0, -1):
			if stop:
				break
			moves.append(V_Move(self, ra, self.fi))
			if v_board.has_piece(ra)(self.fi):
				stop = True
				
		for ra in range(self.ra, 9):
			if stop:
				break
			moves.append(V_Move(self, ra, self.fi))
			if v_board.has_piece(ra)(self.fi):
				stop = True

		for fi in range(self.fi, 0, -1):
			if stop:
				break
			moves.append(V_Move(self, self.ra, fi))
			if v_board.has_piece(self.ra)(fi):
				stop = True

		for fi in range(self.fi, 9):
			if stop:
				break
			moves.append(V_Move(self, self.ra, fi))
			if v_board.has_piece(self.ra)(fi)
				stop = True


			


