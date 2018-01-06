import pygame, board

def in_bounds(ra, fi):
	return (ra > 0 and ra < 9 and fi > 0 and fi < 9)

class Piece(pygame.sprite.Sprite):
	PAWN = 0
	ROOK = 1
	KNGH = 2
	BSHP = 3
	KING = 4
	QUEN = 5
	images = []
	# --------------------------------------------------------------------------------
	def __init__(self, ra, fi, color):
		pygame.sprite.Sprite.__init__(self, self.containers)
		self.hasMoved = False
		self.color = color
		self.ra = ra
		self.fi = fi
		self.en_passant_able = False
		self.valid = True
		
	def set_rect(self, x, y, height):
		self.rect = pygame.Rect(x, y, height, height)
		
	def set_containers(self, containers):
		self.containers = containers
		
	# --------------------------------------------------------------------------------
	def load_image(n, height):
		return (pygame.transform.scale(Piece.images[n], (int(height), int(height))))

	# --------------------------------------------------------------------------------
	def get_position(self):
		return (self.ra, self.fi)
		
	def take_to_str(self, ra, fi):
		return self.shorthand + "x" + board.space_to_str(ra, fi)

	def pos_to_str(ra, fi):
		pos = str(Board.file_[fi]) + str(ra)
		return pos

	def direction(self, my_board):
		if self.color == my_board.plyr1_color:
			return -1
		else:
			return 1

	# --------------------------------------------------------------------------------	
	# RETURNS whether a POSITION is ON the BOARD and NOT the CURRENT POSITION
	def possible_move(self, ra, fi):
		if in_bounds(ra, fi) and (ra, fi) != self.get_position():
			return True
		else:
			return False
			
	# --------------------------------------------------------------------------------
	# RETURNS whether the TAKE SATISFIES the piece's TAKE RULE and is attempted on a piece of OPPOSITE COLOR
	def valid_take(self, my_board, ra, fi):
		if self.valid and my_board.has_piece(ra, fi) and self.possible_move(ra, fi) and self.takeRule(my_board, ra, fi) and self.is_opp(my_board, ra ,fi):
			return True
		else: return False
			
	# --------------------------------------------------------------------------------
	# RETURNS whether the MOVE SATISFIES the piece's MOVE RULE and is attempted on an EMPTY SPACE
	def valid_move(self, my_board, ra, fi):
		if self.valid and self.possible_move(ra, fi) and self.moveRule(my_board, ra, fi) and not my_board.has_piece(ra, fi):
			return True
		else: return False
		
	# RETURNS MOVE STRING for PGN	
	def move_str(self, ra, fi):
		return self.shorthand + board.space_to_str(ra, fi)
	
	# RETURNS whether a TAKE is POSSIBLE
	def can_take(self, my_board, ra, fi):
		return(in_bounds(ra, fi) and my_board.has_piece(ra, fi) and self.is_opp(my_board, ra, fi))
		
	# RETURNS whether a PIECE is of the OPPOSITE COLOR
	def is_opp(self, my_board, ra, fi):
		return self.color != my_board.get_piece_color(ra, fi)

	# PROCESSES SPECIAL MOVES for a piece and APPENDS MOVE to PGN
	def moveRule(self, my_board, ra, fi):
		if ((ra, fi) in self.moves):
			my_board.last_move = self.move_str(ra, fi)
			return True
		else:
			return False
			
	# PROCESSES SPECIAL TAKES for a piece and APPENDS MOVE to PGN		
	def takeRule(self, my_board, ra, fi):
		if ((ra,fi) in self.takes):
			my_board.last_move = self.take_to_str(ra, fi)
			return True
		else:
			return False

class Pawn(Piece):
	def __init__(self, ra, fi, color):
		Piece.__init__(self, ra, fi, color)
		self.en_passant_able = False
		self.shorthand = ""
		self.index = 0
		
	def set_image(self, height):
		self.image = Piece.load_image(board.colorKey(self.color, 0), height)
		

	# RETURNS a list of POSSIBLE MOVES in the form of [(ra1, fi1), (ra2, fi2), ...]
	def gen_moves(self, my_board):
	
		# IF SELF is NOT VALID, generate NO MOVES
		if not self.valid: return
	
		self.moves = []
		self.takes = []
		
		# TWO SPACES FORWARD if NOT MOVED
		two_fwd = (self.ra + self.direction(my_board) * 2)
		one_fwd = (self.ra + self.direction(my_board))
		
		if not self.hasMoved:
			if in_bounds(two_fwd, self.fi): 
				if my_board.is_empty(one_fwd, self.fi) and my_board.is_empty(two_fwd, self.fi):
					self.moves.append((two_fwd, self.fi))
			
		# ONE SPACE FORWARD
		if in_bounds((self.ra + self.direction(my_board) * 1), self.fi) and my_board.is_empty(one_fwd, self.fi):
			self.moves.append(((self.ra + self.direction(my_board) * 1), self.fi))

		
		# EN PASSANT
		ra = self.ra + self.direction(my_board)
		fi = self.fi - 1
		if in_bounds(ra, fi):
			if my_board.is_empty(ra, fi) and isinstance(my_board.board[self.ra][self.fi - 1], Piece) and my_board.board[self.ra][self.fi - 1].en_passant_able:
				self.moves.append(((self.ra + self.direction(my_board) * 1), (self.fi - 1)))
				
		ra = self.ra + self.direction(my_board)
		fi = self.fi + 1
		if in_bounds(ra, fi):
			if my_board.is_empty(ra, fi) and isinstance(my_board.board[self.ra][self.fi + 1], Piece) and my_board.board[self.ra][self.fi + 1].en_passant_able:
				self.moves.append((ra, fi))
				
		# REGULAR TAKES
		if self.can_take(my_board, one_fwd, self.fi - 1):
			self.takes.append(((self.ra + self.direction(my_board) * 1), (self.fi - 1 )))
		if self.can_take(my_board, one_fwd, self.fi + 1):
			self.takes.append(((self.ra + self.direction(my_board) * 1), (self.fi + 1 )))

		
	# TODO: RENAME to move()
	
	def moveRule(self, my_board, ra, fi):
		if ((ra, fi) in self.moves):
			# EN PASSANT SPECIAL CASE
			if ra == (self.ra + (self.direction(my_board) * 1)) and abs(fi - self.fi) == 1:
				other_piece = my_board.board[self.ra][fi]
				if isinstance(other_piece,Pawn) and other_piece.en_passant_able:
					other_piece.kill()
					my_board.board[self.ra][fi] = 0
					my_board.last_move = board.Board.file_[self.fi] + self.take_to_str(ra, fi) +"e.p."
					return True
		
			else:
				my_board.last_move = board.space_to_str(ra,fi)
				if (ra, fi) == ((self.ra + self.direction(my_board) * 2), self.fi):
					self.en_passant_able = True
				else:
					self.en_passant_able = False
				return True
	
	# TODO: RENAME to take()
	def takeRule(self, my_board, ra, fi):
		if ((ra,fi) in self.takes):
			my_board.last_move = board.Board.file_[self.fi] + self.take_to_str(ra, fi)
			return True
		else:
			return False	
			
	def move_str(self, ra, fi):
		return board.space_to_str(ra,fi)
	
	def take_to_str(self, ra, fi):
		return board.Board.file_[self.fi] + self.shorthand + "x" + board.space_to_str(ra, fi)

class Rook(Piece):
	def __init__(self, ra, fi, color):
		Piece.__init__(self, ra, fi, color)
		self.shorthand = "R"
		self.index = 1
		
	def set_image(self, height):
		self.image = Piece.load_image(board.colorKey(self.color, 1), height)
		
	def gen_moves(self, my_board):
		if not self.valid: return
		self.moves = []
		self.takes = []
	
		for ra in range(self.ra - 1, 0, -1):
			if self.can_take(my_board, ra, self.fi):
				self.takes.append((ra, self.fi))
				break
			elif my_board.has_piece(ra, self.fi):
				break
			else: self.moves.append((ra, self.fi))
			
		for ra in range(self.ra + 1, 9):
			if self.can_take(my_board, ra, self.fi):
				self.takes.append((ra, self.fi))
				break
			elif my_board.has_piece(ra, self.fi):
				break
			else: self.moves.append((ra, self.fi))
			
			
			
		for fi in range(self.fi - 1, 0, -1):
			if self.can_take(my_board, self.ra, fi):
				self.takes.append((self.ra, fi))
				break
			elif my_board.has_piece(self.ra, fi):
				break
			else: self.moves.append((self.ra, fi))
		for fi in range(self.fi + 1, 9):
			if self.can_take(my_board, self.ra, fi):
				self.takes.append((self.ra, fi))
				break
			elif my_board.has_piece(self.ra, fi):
				break
			else: self.moves.append((self.ra, fi))


class Knight(Piece):
	def __init__(self, ra, fi, color):
		Piece.__init__(self, ra, fi, color)
		self.shorthand = "N"
		self.index = 2
		
	def set_image(self, height):
		self.image = Piece.load_image(board.colorKey(self.color, 2), height)

	def gen_moves(self, my_board):
		if not self.valid: return
		self.moves = []
		self.takes = []

		ra = self.ra + 1
		fi = self.fi + 2
		if in_bounds(ra, fi):
			if self.can_take(my_board, ra, fi):
				self.takes.append((ra,fi))
			elif not my_board.has_piece(ra, fi): 
				self.moves.append((ra, fi))
			
		ra = self.ra - 1
		if in_bounds(ra, fi):
			if self.can_take(my_board, ra, fi):
				self.takes.append((ra,fi))
			elif not my_board.has_piece(ra, fi): 
				self.moves.append((ra, fi))
		
		fi = self.fi - 2
		if in_bounds(ra, fi):
			if self.can_take(my_board, ra, fi):
				self.takes.append((ra,fi))
			elif not my_board.has_piece(ra, fi): 
				self.moves.append((ra, fi))
			
		ra = self.ra + 1
		if in_bounds(ra, fi):
			if self.can_take(my_board, ra, fi):
				self.takes.append((ra,fi))
			elif not my_board.has_piece(ra, fi): 
				self.moves.append((ra, fi))
		
		ra = self.ra + 2
		fi = self.fi + 1
		if in_bounds(ra, fi):
			if self.can_take(my_board, ra, fi):
				self.takes.append((ra,fi))
			elif not my_board.has_piece(ra, fi): 
				self.moves.append((ra, fi))
			
		ra = self.ra - 2
		if in_bounds(ra, fi):
			if self.can_take(my_board, ra, fi):
				self.takes.append((ra,fi))
			elif not my_board.has_piece(ra, fi): 
				self.moves.append((ra, fi))
		
		fi = self.fi - 1
		if in_bounds(ra, fi):
			if self.can_take(my_board, ra, fi):
				self.takes.append((ra,fi))
			elif not my_board.has_piece(ra, fi): 
				self.moves.append((ra, fi))
			
		ra = self.ra + 2
		if in_bounds(ra, fi):
			if self.can_take(my_board, ra, fi):
				self.takes.append((ra,fi))
			elif not my_board.has_piece(ra, fi): 
				self.moves.append((ra, fi))
		
	
		

class Bishop(Piece):
	def __init__(self, ra, fi, color):
		Piece.__init__(self, ra, fi, color)
		self.shorthand = "B"
		self.index = 3
		
	def set_image(self, height):
		self.image = Piece.load_image(board.colorKey(self.color, 3), height)

	def gen_moves(self, my_board):
		if not self.valid: return
		self.moves = []
		self.takes = []
		
		rinc = 1
		finc = 1
		
		for i in range(1, 9):
			if in_bounds(self.ra + i * rinc, self.fi + i * finc):
				if self.can_take(my_board, self.ra + i * rinc, self.fi + i * finc):
					self.takes.append((self.ra + i * rinc, self.fi + i * finc))
					break
				elif my_board.has_piece(self.ra + i * rinc, self.fi + i * finc):
					break
				else:
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
		
		rinc = -1
		
		for i in range(1, 9):
			if in_bounds(self.ra + i * rinc, self.fi + i * finc):
				if self.can_take(my_board, self.ra + i * rinc, self.fi + i * finc):
					self.takes.append((self.ra + i * rinc, self.fi + i * finc))
					break
				elif my_board.has_piece(self.ra + i * rinc, self.fi + i * finc):
					break
				else:
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
		
		finc = -1
		
		for i in range(1, 9):
			if in_bounds(self.ra + i * rinc, self.fi + i * finc):
				if self.can_take(my_board, self.ra + i * rinc, self.fi + i * finc):
					self.takes.append((self.ra + i * rinc, self.fi + i * finc))
					break
				elif my_board.has_piece(self.ra + i * rinc, self.fi + i * finc):
					break
				else:
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
		
		rinc = 1
		
		for i in range(1, 9):
			if in_bounds(self.ra + i * rinc, self.fi + i * finc):
				if self.can_take(my_board, self.ra + i * rinc, self.fi + i * finc):
					self.takes.append((self.ra + i * rinc, self.fi + i * finc))
					break
				elif my_board.has_piece(self.ra + i * rinc, self.fi + i * finc):
					break
				else:
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
					

	


class King(Piece):
	def __init__(self, ra, fi, color):
		Piece.__init__(self, ra, fi, color)
		self.shorthand = "K"
		self.index = 4
		
	def set_image(self, height):
		self.image = Piece.load_image(board.colorKey(self.color, 4), height)
		
	def gen_moves(self, my_board):
		if not self.valid: return
		self.moves = []
		self.takes = []
	
		for i in range(-1, 2):
			for j in range(-1, 2):
				if (i, j) == (0, 0):
					continue
				ra = self.ra + i
				fi = self.fi + j
				if in_bounds(ra, fi):
					if self.can_take(my_board, ra, fi):
						self.takes.append((ra, fi))
					elif not my_board.has_piece(ra, fi):
						self.moves.append((ra, fi))
		castle = True
		
		if not self.hasMoved and my_board.board[self.ra][1] != 0 and not my_board.board[self.ra][1].hasMoved:
			for i in range(2, self.fi):
				if my_board.board[self.ra][i] != 0: castle = False
			if castle: self.moves.append((self.ra, self.fi - 2))
			
		castle = True
		
		if not self.hasMoved and my_board.board[self.ra][8] != 0 and not my_board.board[self.ra][8].hasMoved:
			for i in range(self.fi + 1, 8):
				if my_board.board[self.ra][i] != 0: castle = False
			if castle: self.moves.append((self.ra, self.fi + 2))
			


	def moveRule(self, my_board, ra, fi):
		self.gen_moves(my_board)
		
		if ra == self.ra and fi - self.fi == -2:
			if ((ra, fi) in self.moves):
				piece = my_board.get_piece(ra, 1)
				piece.rect = pygame.Rect(my_board.file_to_x(fi + 1), my_board.rank_to_y(ra), my_board.space_height, my_board.space_height)
				my_board.set_space(ra, 1, 0)
				piece.ra = ra
				piece.fi = fi + 1
				piece.hasMoved = True
				my_board.set_space(ra, fi + 1, piece)
				
				my_board.last_move = "O-O"
				return True
				
		if ra == self.ra and fi - self.fi == 2:
			if ((ra, fi) in self.moves):
				piece = my_board.get_piece(ra, 8)
				piece.rect = pygame.Rect(my_board.file_to_x(fi - 1), my_board.rank_to_y(ra), my_board.space_height, my_board.space_height)
				my_board.set_space(ra, 8, 0)
				piece.ra = ra
				piece.fi = fi - 1
				piece.hasMoved = True
				my_board.set_space(ra, fi - 1, piece)
				
				my_board.last_move = "O-O-O"
				return True
				
		if ((ra, fi) in self.moves):
			my_board.last_move = self.shorthand + board.space_to_str(ra,fi)
			return True
		else: return False
			
		

class Queen(Piece):
	def __init__(self, ra, fi, color):
		Piece.__init__(self, ra, fi, color)
		self.shorthand = "Q"
		self.index = 5

	def set_image(self, height):
		self.image = Piece.load_image(board.colorKey(self.color, 5), height)
		
	def gen_moves(self, my_board):
		if not self.valid: return
		self.moves = []
		self.takes = []
		
		rinc = 1
		finc = 1
		
		for i in range(1, 9):
			if in_bounds(self.ra + i * rinc, self.fi + i * finc):
				if self.can_take(my_board, self.ra + i * rinc, self.fi + i * finc):
					self.takes.append((self.ra + i * rinc, self.fi + i * finc))
					break
				elif my_board.has_piece(self.ra + i * rinc, self.fi + i * finc):
					break
				else:
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
		
		rinc = -1
		
		for i in range(1, 9):
			if in_bounds(self.ra + i * rinc, self.fi + i * finc):
				if self.can_take(my_board, self.ra + i * rinc, self.fi + i * finc):
					self.takes.append((self.ra + i * rinc, self.fi + i * finc))
					break
				elif my_board.has_piece(self.ra + i * rinc, self.fi + i * finc):
					break
				else:
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
		
		finc = -1
		
		for i in range(1, 9):
			if in_bounds(self.ra + i * rinc, self.fi + i * finc):
				if self.can_take(my_board, self.ra + i * rinc, self.fi + i * finc):
					self.takes.append((self.ra + i * rinc, self.fi + i * finc))
					break
				elif my_board.has_piece(self.ra + i * rinc, self.fi + i * finc):
					break
				else:
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
		
		rinc = 1
		
		for i in range(1, 9):
			if in_bounds(self.ra + i * rinc, self.fi + i * finc):
				if self.can_take(my_board, self.ra + i * rinc, self.fi + i * finc):
					self.takes.append((self.ra + i * rinc, self.fi + i * finc))
					break
				elif my_board.has_piece(self.ra + i * rinc, self.fi + i * finc):
					break
				else:
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
					

					
		for ra in range(self.ra - 1, 0, -1):
			if self.can_take(my_board, ra, self.fi):
				self.takes.append((ra, self.fi))
				break
			elif my_board.has_piece(ra, self.fi):
				break
			else: self.moves.append((ra, self.fi))
			
		for ra in range(self.ra + 1, 9):
			if self.can_take(my_board, ra, self.fi):
				self.takes.append((ra, self.fi))
				break
			elif my_board.has_piece(ra, self.fi):
				break
			else: self.moves.append((ra, self.fi))
			
			
			
		for fi in range(self.fi - 1, 0, -1):
			if self.can_take(my_board, self.ra, fi):
				self.takes.append((self.ra, fi))
				break
			elif my_board.has_piece(self.ra, fi):
				break
			else: self.moves.append((self.ra, fi))
		for fi in range(self.fi + 1, 9):
			if self.can_take(my_board, self.ra, fi):
				self.takes.append((self.ra, fi))
				break
			elif my_board.has_piece(self.ra, fi):
				break
			else: self.moves.append((self.ra, fi))