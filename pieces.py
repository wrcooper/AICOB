import pygame, board, sys, inspect

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
		self.has_moved = False
		self.color = color
		self.ra = ra
		self.fi = fi
		self.en_passant_able = False
		self.valid = True
		self.moves = []
		
	def set_rect(self, x, y, height):
		self.rect = pygame.Rect(x, y, height, height)
		
	def set_containers(self, containers):
		self.containers = containers
		
	# --------------------------------------------------------------------------------
	def load_image(n, height):
		return (pygame.transform.smoothscale(Piece.images[n], (int(height), int(height))))

	# --------------------------------------------------------------------------------
	def get_position(self):
		return (self.ra, self.fi)
		
	def take_to_str(self, ra, fi):
		return self.shorthand + "x" + board.space_to_str(ra, fi)

	def pos_to_str(ra, fi):
		pos = str(Board.file_[fi]) + str(ra)
		return pos

	def direction(self, my_board):
		if self.color == my_board.plyr1.color:
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
	# RETURNS whether the MOVE SATISFIES the piece's MOVE RULE
	def valid_move(self, ra, fi):
		if self.valid and self.possible_move(ra, fi): return True
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
		
	def print_moves(self):
		for move in self.moves:
			print(board.move_to_str((self.ra, self.fi, move[0], move[1])))
		
	def move(self, my_board, ra, fi):
		result = self.move_rule(my_board, ra, fi)
		
		if not result: return False
		
		
		if result == True:
			self.append_move_hist(my_board, ra, fi)
		
			self.take_piece(my_board, ra, fi)
				
			my_board.set_space(ra, fi, self)
			my_board.set_space(self.ra, self.fi, 0)
			
			self.has_moved = True
			self.set_pos(my_board, ra, fi)
			
			return True
		else: return False
		
	def append_move_hist(self, my_board, ra2, fi2):
		piece2 = my_board.get_piece(ra2, fi2)
		
		if piece2 == False:
			piece2 = 0
		
		my_board.hist.append([piece2, [self.ra, self.fi, ra2, fi2, self.has_moved, self.en_passant_able]])
		
			
	def take_piece(self, my_board, ra, fi):
		piece2 = my_board.get_piece(ra, fi)
		
		if piece2:
			my_board.last_move = self.take_to_str(ra, fi)
			piece2.kill()
			return True
		else:
			my_board.last_move = self.move_str(ra, fi)
			return False

	def set_pos(self, my_board, ra, fi):
		self.ra = ra
		self.fi = fi
		
		self.rect = pygame.Rect(my_board.file_to_x(fi), my_board.rank_to_y(ra), my_board.space_height, my_board.space_height)

	# PROCESSES SPECIAL MOVES for a piece and APPENDS MOVE to PGN
	def move_rule(self, my_board, ra, fi):
		if self.valid_move(ra, fi) and ((ra, fi) in self.moves): return True
		else: return False

class Pawn(Piece):
	def __init__(self, ra, fi, color):
		Piece.__init__(self, ra, fi, color)
		self.en_passant_able = False
		self.shorthand = ""
		self.index = Piece.PAWN
		
	def set_image(self, height):
		self.image = Piece.load_image(board.colorKey(self.color, 0), height)
	
	# RETURNS a list of POSSIBLE MOVES in the form of [(ra1, fi1), (ra2, fi2), ...]
	def gen_moves(self, my_board):
		self.moves = []
	
		# IF SELF is NOT VALID, generate NO MOVES
		if not self.valid: return
	
		
		# TWO SPACES FORWARD if NOT MOVED
		two_fwd = (self.ra + self.direction(my_board) * 2)
		one_fwd = (self.ra + self.direction(my_board))
		
		if not self.has_moved:
			if in_bounds(two_fwd, self.fi): 
				if my_board.is_empty(one_fwd, self.fi) and my_board.is_empty(two_fwd, self.fi):
					self.moves.append((two_fwd, self.fi))
		
		# ONE SPACE FORWARD
		if in_bounds(one_fwd, self.fi) and my_board.is_empty(one_fwd, self.fi):
			self.moves.append((one_fwd, self.fi))

		
		# EN PASSANT
		fi = self.fi - 1
		if in_bounds(one_fwd, fi):
			if my_board.is_empty(one_fwd, fi) and self.can_take(my_board, one_fwd, fi) and isinstance(my_board.board[self.ra][fi], Piece) and my_board.board[self.ra][fi].en_passant_able:
				self.moves.append((one_fwd, (self.fi - 1)))
				
		ra = self.ra + self.direction(my_board)
		fi = self.fi + 1
		if in_bounds(ra, fi):
			if my_board.is_empty(one_fwd, fi) and self.can_take(my_board, self.ra, fi) and isinstance(my_board.board[self.ra][fi], Piece) and my_board.board[self.ra][fi].en_passant_able:
				self.moves.append((one_fwd, fi))
				
		# REGULAR TAKES
		if self.can_take(my_board, one_fwd, self.fi - 1):
			self.moves.append((one_fwd, (self.fi - 1 )))
		if self.can_take(my_board, one_fwd, self.fi + 1):
			self.moves.append((one_fwd, (self.fi + 1 )))
			
	def append_move_hist_ep(self, my_board, ra2, fi2):
		piece2 = my_board.get_piece(self.ra, fi2)
		
		my_board.hist.append([piece2, [self.ra, self.fi, ra2, fi2, self.has_moved, self.en_passant_able]])

	def move(self, my_board, ra, fi):
		result = self.move_rule(my_board, ra, fi)
		
		if not self.valid_move(ra, fi): return False
		
		# EN PASSANT
		if result == "ep":
			self.append_move_hist_ep(my_board, ra, fi)
			other_piece = my_board.get_piece(self.ra, fi)
			other_piece.kill()
			
			my_board.set_space(self.ra, fi, 0) 
			my_board.set_space(self.ra, self.fi, 0) 
			my_board.set_space(ra, fi, self)
			
			self.has_moved = True
			
			self.set_pos(my_board, ra, fi)
			
			my_board.last_move = self.take_to_str(ra, fi) +"e.p."
			return True
			
		# SETTING EN PASSANT
		elif result == "set_ep":
			Piece.append_move_hist(self, my_board, ra, fi)
			
			my_board.set_space(self.ra, self.fi, 0) 
			my_board.set_space(ra, fi, self)
			
			self.en_passant_able = True
			self.has_moved = True
			
			self.set_pos(my_board, ra, fi)
			
			my_board.last_move = board.space_to_str(ra,fi)
			return True
			
		# STANDARD MOVE
		elif result == True:
			Piece.append_move_hist(self, my_board, ra, fi)
			
			self.take_piece(my_board, ra, fi)
		
			my_board.set_space(self.ra, self.fi, 0) 
			my_board.set_space(ra, fi, self)
			
			self.en_passant_able = False
			self.has_moved = True
			
			self.set_pos(my_board, ra, fi)
			
			my_board.last_move = board.space_to_str(ra,fi)
			return True
		else: 
			return False

	
	def move_rule(self, my_board, ra, fi):
		if ((ra, fi) in self.moves):
			# EN PASSANT SPECIAL CASE
			if not my_board.has_piece(ra, fi) and ra == (self.ra + (self.direction(my_board) * 1)) and abs(fi - self.fi) == 1:
				other_piece = my_board.get_piece(self.ra, fi)
				if isinstance(other_piece, Pawn) and other_piece.en_passant_able and self.is_opp(my_board, self.ra, fi):
					return "ep"
					
			# STANDARD MOVES
			else:
				# IF MOVED TWO RANKS FORWARD, set EN PASSANT ABLE
				if (ra, fi) == ((self.ra + self.direction(my_board) * 2), self.fi):
					return "set_ep"
				
				# ELSE MOVE is ONE FORWARD or a TAKE
				else:
					return True
					
		else: 
			#print("pawn moves: " + str(self.moves))
			return False
			
	def move_str(self, ra, fi):
		return board.space_to_str(ra,fi)
	
	def take_to_str(self, ra, fi):
		return board.Board.file_[self.fi] + self.shorthand + "x" + board.space_to_str(ra, fi)

class Rook(Piece):
	def __init__(self, ra, fi, color):
		Piece.__init__(self, ra, fi, color)
		self.shorthand = "R"
		self.index = Piece.ROOK
		
	def set_image(self, height):
		self.image = Piece.load_image(board.colorKey(self.color, 1), height)
		
	def gen_moves(self, my_board):
		self.moves = []
		if not self.valid: return
	
		for ra in range(self.ra - 1, 0, -1):
			if self.can_take(my_board, ra, self.fi):
				self.moves.append((ra, self.fi))
				break
			elif my_board.has_piece(ra, self.fi):
				break
			else: self.moves.append((ra, self.fi))
			
		for ra in range(self.ra + 1, 9):
			if self.can_take(my_board, ra, self.fi):
				self.moves.append((ra, self.fi))
				break
			elif my_board.has_piece(ra, self.fi):
				break
			else: self.moves.append((ra, self.fi))
			
			
			
		for fi in range(self.fi - 1, 0, -1):
			if self.can_take(my_board, self.ra, fi):
				self.moves.append((self.ra, fi))
				break
			elif my_board.has_piece(self.ra, fi):
				break
			else: self.moves.append((self.ra, fi))
		for fi in range(self.fi + 1, 9):
			if self.can_take(my_board, self.ra, fi):
				self.moves.append((self.ra, fi))
				break
			elif my_board.has_piece(self.ra, fi):
				break
			else: self.moves.append((self.ra, fi))


class Knight(Piece):
	def __init__(self, ra, fi, color):
		Piece.__init__(self, ra, fi, color)
		self.shorthand = "N"
		self.index = Piece.KNGH
		
	def set_image(self, height):
		self.image = Piece.load_image(board.colorKey(self.color, 2), height)

	def gen_moves(self, my_board):
		self.moves = []
		if not self.valid: return

		ra = self.ra + 1
		fi = self.fi + 2
		if in_bounds(ra, fi):
			if self.can_take(my_board, ra, fi):
				self.moves.append((ra,fi))
			elif not my_board.has_piece(ra, fi): 
				self.moves.append((ra, fi))
			
		ra = self.ra - 1
		if in_bounds(ra, fi):
			if self.can_take(my_board, ra, fi):
				self.moves.append((ra,fi))
			elif not my_board.has_piece(ra, fi): 
				self.moves.append((ra, fi))
		
		fi = self.fi - 2
		if in_bounds(ra, fi):
			if self.can_take(my_board, ra, fi):
				self.moves.append((ra,fi))
			elif not my_board.has_piece(ra, fi): 
				self.moves.append((ra, fi))
			
		ra = self.ra + 1
		if in_bounds(ra, fi):
			if self.can_take(my_board, ra, fi):
				self.moves.append((ra,fi))
			elif not my_board.has_piece(ra, fi): 
				self.moves.append((ra, fi))
		
		ra = self.ra + 2
		fi = self.fi + 1
		if in_bounds(ra, fi):
			if self.can_take(my_board, ra, fi):
				self.moves.append((ra,fi))
			elif not my_board.has_piece(ra, fi): 
				self.moves.append((ra, fi))
			
		ra = self.ra - 2
		if in_bounds(ra, fi):
			if self.can_take(my_board, ra, fi):
				self.moves.append((ra,fi))
			elif not my_board.has_piece(ra, fi): 
				self.moves.append((ra, fi))
		
		fi = self.fi - 1
		if in_bounds(ra, fi):
			if self.can_take(my_board, ra, fi):
				self.moves.append((ra,fi))
			elif not my_board.has_piece(ra, fi): 
				self.moves.append((ra, fi))
			
		ra = self.ra + 2
		if in_bounds(ra, fi):
			if self.can_take(my_board, ra, fi):
				self.moves.append((ra,fi))
			elif not my_board.has_piece(ra, fi): 
				self.moves.append((ra, fi))
		
	
		

class Bishop(Piece):
	def __init__(self, ra, fi, color):
		Piece.__init__(self, ra, fi, color)
		self.shorthand = "B"
		self.index = Piece.BSHP
		
	def set_image(self, height):
		self.image = Piece.load_image(board.colorKey(self.color, 3), height)

	def gen_moves(self, my_board):
		self.moves = []
		if not self.valid: return
		
		rinc = 1
		finc = 1
		
		for i in range(1, 9):
			if in_bounds(self.ra + i * rinc, self.fi + i * finc):
				if self.can_take(my_board, self.ra + i * rinc, self.fi + i * finc):
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
					break
				elif my_board.has_piece(self.ra + i * rinc, self.fi + i * finc):
					break
				else:
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
		
		rinc = -1
		
		for i in range(1, 9):
			if in_bounds(self.ra + i * rinc, self.fi + i * finc):
				if self.can_take(my_board, self.ra + i * rinc, self.fi + i * finc):
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
					break
				elif my_board.has_piece(self.ra + i * rinc, self.fi + i * finc):
					break
				else:
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
		
		finc = -1
		
		for i in range(1, 9):
			if in_bounds(self.ra + i * rinc, self.fi + i * finc):
				if self.can_take(my_board, self.ra + i * rinc, self.fi + i * finc):
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
					break
				elif my_board.has_piece(self.ra + i * rinc, self.fi + i * finc):
					break
				else:
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
		
		rinc = 1
		
		for i in range(1, 9):
			if in_bounds(self.ra + i * rinc, self.fi + i * finc):
				if self.can_take(my_board, self.ra + i * rinc, self.fi + i * finc):
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
					break
				elif my_board.has_piece(self.ra + i * rinc, self.fi + i * finc):
					break
				else:
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
					

	


class King(Piece):
	def __init__(self, ra, fi, color):
		Piece.__init__(self, ra, fi, color)
		self.shorthand = "K"
		self.index = Piece.KING
		
	def set_image(self, height):
		self.image = Piece.load_image(board.colorKey(self.color, 4), height)
		
	def gen_moves(self, my_board):
		self.moves = []
		if not self.valid: return
	
		for i in range(-1, 2):
			for j in range(-1, 2):
				if (i, j) == (0, 0):
					continue
				ra = self.ra + i
				fi = self.fi + j
				if in_bounds(ra, fi):
					if self.can_take(my_board, ra, fi):
						self.moves.append((ra, fi))
					elif not my_board.has_piece(ra, fi):
						self.moves.append((ra, fi))
						
		castle = True
		
		if not my_board.is_check(self.color) and not self.has_moved and my_board.board[self.ra][1] != 0 and not my_board.board[self.ra][1].has_moved:
			for i in range(2, self.fi):
				if my_board.board[self.ra][i] != 0: castle = False
			if castle: self.moves.append((self.ra, self.fi - 2))
			
		castle = True
		
		if not my_board.is_check(self.color) and not self.has_moved and my_board.board[self.ra][8] != 0 and not my_board.board[self.ra][8].has_moved:
			for i in range(self.fi + 1, 8):
				if my_board.board[self.ra][i] != 0: castle = False
			if castle: self.moves.append((self.ra, self.fi + 2))
			
	def append_move_hist_castle(self, my_board, ra2, fi2, rook, rook_ra2, rook_fi2):
		my_board.hist.append([0, [self.ra, self.fi, ra2, fi2, self.has_moved, self.en_passant_able], [rook.ra, rook.fi, rook_ra2, rook_fi2, rook.has_moved, rook.en_passant_able]])
			
	def move(self, my_board, ra, fi):
		result = self.move_rule(my_board, ra, fi)
		
		if not result: return False

		if result == "lcastle":	
			rook = my_board.get_piece(ra, 1)
			
			self.append_move_hist_castle(my_board, ra, fi, rook, ra, fi+1)
			
			rook.set_pos(my_board, ra, fi+1)
			
			my_board.set_space(ra, 1, 0)
			my_board.set_space(ra, fi + 1, rook)
			my_board.set_space(ra, fi, self)
			my_board.set_space(self.ra, self.fi, 0)
			
			self.set_pos(my_board, ra, fi)
			
			rook.has_moved = True
			self.has_moved = True
			
			my_board.last_move = "O-O-O"
			return True
			
		elif result == "rcastle":	
			rook = my_board.get_piece(ra, 8)
			
			self.append_move_hist_castle(my_board, ra, fi, rook, ra, fi-1)
			
			rook.set_pos(my_board, ra, fi-1)
			
			my_board.set_space(ra, 8, 0)
			my_board.set_space(ra, fi - 1, rook)
			my_board.set_space(ra, fi, self)
			my_board.set_space(self.ra, self.fi, 0)
			
			self.set_pos(my_board, ra, fi)
			
			rook.has_moved = True
			self.has_moved = True
			
			my_board.last_move = "O-O"
			return True
			
		elif result == True:
			Piece.append_move_hist(self, my_board, ra, fi)
		
			self.take_piece(my_board, ra, fi)
			
			my_board.set_space(ra, fi, self)
			my_board.set_space(self.ra, self.fi, 0)
			
			self.has_moved = True
			
			self.set_pos(my_board, ra, fi)
			return True
			

	def move_rule(self, my_board, ra, fi):
		if ((ra, fi) in self.moves):
			if ra == self.ra and fi - self.fi == -2:
				return "lcastle"
						
			elif ra == self.ra and fi - self.fi == 2:
				return "rcastle"
			
			else:
				return True
				
		else: 
			print("Invalid Move Attempted")
			print("My moves:")
			self.print_moves()
			print("Move attempted: " + board.move_to_str((self.ra, self.fi, ra ,fi)))
			print(self.has_moved)
			return False
			
		

class Queen(Piece):
	def __init__(self, ra, fi, color):
		Piece.__init__(self, ra, fi, color)
		self.shorthand = "Q"
		self.index = Piece.QUEN

	def set_image(self, height):
		self.image = Piece.load_image(board.colorKey(self.color, 5), height)
		
	def gen_moves(self, my_board):
		self.moves = []
		
		if not self.valid: return
		
		rinc = 1
		finc = 1
		
		for i in range(1, 9):
			if in_bounds(self.ra + i * rinc, self.fi + i * finc):
				if self.can_take(my_board, self.ra + i * rinc, self.fi + i * finc):
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
					break
				elif my_board.has_piece(self.ra + i * rinc, self.fi + i * finc):
					break
				else:
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
		
		rinc = -1
		
		for i in range(1, 9):
			if in_bounds(self.ra + i * rinc, self.fi + i * finc):
				if self.can_take(my_board, self.ra + i * rinc, self.fi + i * finc):
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
					break
				elif my_board.has_piece(self.ra + i * rinc, self.fi + i * finc):
					break
				else:
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
		
		finc = -1
		
		for i in range(1, 9):
			if in_bounds(self.ra + i * rinc, self.fi + i * finc):
				if self.can_take(my_board, self.ra + i * rinc, self.fi + i * finc):
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
					break
				elif my_board.has_piece(self.ra + i * rinc, self.fi + i * finc):
					break
				else:
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
		
		rinc = 1
		
		for i in range(1, 9):
			if in_bounds(self.ra + i * rinc, self.fi + i * finc):
				if self.can_take(my_board, self.ra + i * rinc, self.fi + i * finc):
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
					break
				elif my_board.has_piece(self.ra + i * rinc, self.fi + i * finc):
					break
				else:
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
					

					
		for ra in range(self.ra - 1, 0, -1):
			if self.can_take(my_board, ra, self.fi):
				self.moves.append((ra, self.fi))
				break
			elif my_board.has_piece(ra, self.fi):
				break
			else: self.moves.append((ra, self.fi))
			
		for ra in range(self.ra + 1, 9):
			if self.can_take(my_board, ra, self.fi):
				self.moves.append((ra, self.fi))
				break
			elif my_board.has_piece(ra, self.fi):
				break
			else: self.moves.append((ra, self.fi))
			
			
			
		for fi in range(self.fi - 1, 0, -1):
			if self.can_take(my_board, self.ra, fi):
				self.moves.append((self.ra, fi))
				break
			elif my_board.has_piece(self.ra, fi):
				break
			else: self.moves.append((self.ra, fi))
		for fi in range(self.fi + 1, 9):
			if self.can_take(my_board, self.ra, fi):
				self.moves.append((self.ra, fi))
				break
			elif my_board.has_piece(self.ra, fi):
				break
			else: self.moves.append((self.ra, fi))