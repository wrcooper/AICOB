import pygame, board

class Piece(pygame.sprite.Sprite):
	images = []
	def __init__(self, ra, fi, x, y, height, color):
		pygame.sprite.Sprite.__init__(self, self.containers)
		self.rect = pygame.Rect(x, y, height, height)
		self.hasMoved = False
		self.color = color
		self.ra = ra
		self.fi = fi
		self.en_passant_able = False
	
	def loadImage(n, height):
		return (pygame.transform.scale(Piece.images[n], (int(height), int(height))))

	def take_tostr(self, ra, fi):
		return self.shorthand + "x" + board.space_tostr(ra, fi)

	def pos_to_str(ra, fi):
		pos = str(Board.file_[fi]) + str(ra)
		return pos

	def direction(self):
		if self.color == board.player_color:
			return -1
		else:
			return 1
	
	def possibleMove(self, ra, fi):
		if ra > 0 and ra < 9 and (ra, fi) != (self.ra, self.fi) and fi > 0 and fi < 9:
			return True
		else:
			return False

	def validTake(self, my_board, ra, fi):
		if self.possibleMove(ra, fi) and self.takeRule(my_board, ra, fi) and self.color != my_board.board[ra][fi].color:
			return True

	def validMove(self, my_board, ra, fi):
		if self.possibleMove(ra, fi) and self.moveRule(my_board, ra, fi):
			return True

def in_bounds(ra, fi):
	return (ra > 0 and ra < 9 and fi > 0 and fi < 9)

class Pawn(Piece):
	def __init__(self, ra, fi, x, y, height, color):
		Piece.__init__(self, ra, fi, x, y, height, color)
		self.en_passant_able = False
		self.shorthand = ""
		self.image = Piece.loadImage(board.colorKey(color, 0), height)

	# returns a list of possible moves in the form of (ra, fi)
	def gen_moves(self, my_board):
		self.moves = []
		self.takes = []
		
		# two spaces forward if not moved
		if not self.hasMoved:
			if in_bounds((self.ra + self.direction() * 2), self.fi): 
				self.moves.append(((self.ra + self.direction() * 2), self.fi))
			
		# one space forward
		if in_bounds((self.ra + self.direction() * 1), self.fi):
			self.moves.append(
				((self.ra + self.direction() * 1), self.fi)
			)
		
		# en passant
		if in_bounds((self.ra + self.direction() * 1), (self.fi - 1)):
			if isinstance(my_board.board[self.ra][self.fi - 1], Piece) and my_board.board[self.ra][self.fi - 1].en_passant_able:
				self.moves.append(((self.ra + self.direction() * 1), (self.fi - 1)))
		if in_bounds((self.ra + self.direction() * 1), (self.fi + 1)):
			if isinstance(my_board.board[self.ra][self.fi + 1], Piece) and my_board.board[self.ra][self.fi + 1].en_passant_able:
				self.moves.append(((self.ra + self.direction() * 1), (self.fi + 1)))
				
		# regular takes
		if in_bounds((self.ra + self.direction() * 1), (self.fi - 1)):
			self.takes.append(((self.ra + self.direction() * 1), (self.fi - 1 )))
		if in_bounds((self.ra + self.direction() * 1), (self.fi + 1)):
			self.takes.append(((self.ra + self.direction() * 1), (self.fi + 1 )))
			
		print(str(self.moves))
		
		
	def moveRule(self, my_board, ra, fi):
	
		self.gen_moves(my_board)
		if ((ra, fi) in self.moves):
		
			# en passant special case
			if ra == (self.ra + (self.direction() * 1)) and abs(fi - self.fi) == 1:
				other_piece = my_board.board[self.ra][fi]
				if isinstance(other_piece,Pawn) and other_piece.en_passant_able:
					other_piece.kill()
					my_board.board[self.ra][fi] = 0
					my_board.last_move = board.Board.file_[self.fi] + self.take_tostr(ra, fi) +"e.p."
					return True
		
			else:
				my_board.last_move = board.space_tostr(ra,fi)
				if (ra, fi) == ((self.ra + self.direction() * 2), self.fi):
					self.en_passant_able = True
				else:
					self.en_passant_able = False
				return True
	
		"""
		if ra == (self.ra + (self.direction() * 1)) and fi == self.fi:
			board.last_move = space_tostr(ra, fi)
			return True
		elif not self.hasMoved:
			if ra == (self.ra + (self.direction() * 2)) and fi == self.fi:
				if not board.hasPiece(self.ra + (self.direction()), self.fi):
					self.en_passant_able = True
					#TODO reset en_passant_able after a turn passes
					board.last_move = space_tostr(ra, fi)
					return True
		elif ra == (self.ra + (self.direction() * 1)) and abs(fi - self.fi) == 1:
				other_piece = board.board[self.ra][fi]
				if isinstance(other_piece,Pawn) and other_piece.en_passant_able:
					other_piece.kill()
					board.board[self.ra][fi] = 0
					board.last_move = Board.file_[self.fi] + self.take_tostr(ra, fi) +"e.p."
					return True
		else:
			return False
		"""
	
	def takeRule(self, my_board, ra, fi):
		self.gen_moves(my_board)
		if ((ra,fi) in self.takes):
			my_board.last_move = board.Board.file_[self.fi] + self.take_tostr(ra, fi)
			return True
		else:
			return False
	
	
		"""
		if abs(fi - self.fi) == 1 and ra - self.ra == self.direction():
			my_board.last_move = board.Board.file_[self.fi] + self.take_tostr(ra, fi)
			return True
		else:
			return False
		"""

class Rook(Piece):
	def __init__(self, ra, fi, x, y, height, color):
		Piece.__init__(self, ra, fi, x, y, height, color)
		self.shorthand = "R"
		self.image = Piece.loadImage(board.colorKey(color, 1), height)
		
	def gen_moves(self, my_board):
		self.moves = []
		self.takes = []
	
		for ra in range(self.ra - 1, 0, -1):
			if my_board.hasPiece(ra, self.fi):
				self.takes.append((ra, self.fi))
				break
			else: self.moves.append((ra, self.fi))
		for ra in range(self.ra + 1, 9):
			if my_board.hasPiece(ra, self.fi):
				self.takes.append((ra, self.fi))
				break
			else: self.moves.append((ra, self.fi))
			
		for fi in range(self.fi - 1, 0, -1):
			if my_board.hasPiece(self.ra, fi):
				self.takes.append((self.ra, fi))
				break
			else: self.moves.append((self.ra, fi))
		for fi in range(self.fi + 1, 9):
			if my_board.hasPiece(self.ra, fi):
				self.takes.append((self.ra, fi))
				break
			else: self.moves.append((self.ra, fi))

	def moveRule(self, my_board, ra, fi):
		self.gen_moves(my_board)
		
		if ((ra, fi) in self.moves):
			my_board.last_move = self.shorthand + board.space_tostr(ra,fi)
			return True
		else: return False
	
		"""
		if ra == self.ra:
			if fi < self.fi:
				increment = -1
			else:
				increment = 1
			for i in range(self.fi + increment, fi, increment):
				if my_board.hasPiece(ra, i):
					return False
			my_board.last_move = self.shorthand + board.space_tostr(ra, fi)
			return True

		elif fi == self.fi:
			if ra < self.ra:
				increment = -1
			else:
				increment = 1
			for i in range(self.ra + increment, ra, increment):
				if my_board.hasPiece(i, fi):
					return False
			my_board.last_move = self.shorthand + board.space_tostr(ra, fi)
			return True
		else:
			return False
		"""

	def takeRule(self, my_board, ra, fi):
		self.gen_moves(my_board)
		
		if ((ra, fi) in self.takes):
			my_board.last_move = self.take_tostr(ra, fi)
			return True

class Knight(Piece):
	def __init__(self, ra, fi, x, y, height, color):
		Piece.__init__(self, ra, fi, x, y, height, color)
		self.shorthand = "N"
		self.image = Piece.loadImage(board.colorKey(color, 2), height)

	def gen_moves(self, my_board):
		self.moves = []
		self.takes = []
		
		ra = self.ra + 1
		fi = self.fi + 2
		if in_bounds(ra, fi):
			if my_board.hasPiece(ra, fi):
				self.takes.append((ra,fi))
			else: self.moves.append((ra, fi))
			
		ra = self.ra - 1
		if in_bounds(ra, fi):
			if my_board.hasPiece(ra, fi):
				self.takes.append((ra,fi))
			else: self.moves.append((ra, fi))
		
		fi = self.fi - 2
		if in_bounds(ra, fi):
			if my_board.hasPiece(ra, fi):
				self.takes.append((ra,fi))
			else: self.moves.append((ra, fi))
			
		ra = self.ra + 1
		if in_bounds(ra, fi):
			if my_board.hasPiece(ra, fi):
				self.takes.append((ra,fi))
			else: self.moves.append((ra, fi))
		
		ra = self.ra + 2
		fi = self.fi + 1
		if in_bounds(ra, fi):
			if my_board.hasPiece(ra, fi):
				self.takes.append((ra,fi))
			else: self.moves.append((ra, fi))
			
		ra = self.ra - 2
		if in_bounds(ra, fi):
			if my_board.hasPiece(ra, fi):
				self.takes.append((ra,fi))
			else: self.moves.append((ra, fi))
		
		fi = self.fi - 1
		if in_bounds(ra, fi):
			if my_board.hasPiece(ra, fi):
				self.takes.append((ra,fi))
			else: self.moves.append((ra, fi))
			
		ra = self.ra + 2
		if in_bounds(ra, fi):
			if my_board.hasPiece(ra, fi):
				self.takes.append((ra,fi))
			else: self.moves.append((ra, fi))
		

	def moveRule(self, my_board, ra, fi):
		self.gen_moves(my_board)
		
		if ((ra, fi) in self.moves):
			my_board.last_move = self.shorthand + board.space_tostr(ra,fi)
			return True
		else:
			return False
			
	
		
		"""
		if abs(fi - self.fi) == 2:
			if abs(ra - self.ra) == 1:
				my_board.last_move = self.shorthand + board.space_tostr(ra, fi)
				return True
		elif abs(ra - self.ra) == 2:
			if abs(fi - self.fi) == 1:
				my_board.last_move = self.shorthand + board.space_tostr(ra, fi)
				return True
		else:
			return False
		"""
	
	def takeRule(self, my_board, ra, fi):
		self.gen_moves(my_board)
		
		if ((ra, fi) in self.takes):
			my_board.last_move = self.take_tostr(ra, fi)
			return True
		else:
			return False
		
		
		"""
		if self.moveRule(my_board, ra, fi):
			my_board.last_move = self.take_tostr(ra, fi)
			return True
		"""


class Bishop(Piece):
	def __init__(self, ra, fi, x, y, height, color):
		Piece.__init__(self, ra, fi, x, y, height, color)
		self.shorthand = "B"
		self.image = Piece.loadImage(board.colorKey(color, 3), height)

	def gen_moves(self, my_board):
		self.moves = []
		self.takes = []
		
		rinc = 1
		finc = 1
		
		for i in range(1, 9):
			if in_bounds(self.ra + i * rinc, self.fi + i * finc):
				if my_board.hasPiece(self.ra + i * rinc, self.fi + i * finc):
					self.takes.append((self.ra + i * rinc, self.fi + i * finc))
					break
				else:
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
		
		rinc = -1
		
		for i in range(1, 9):
			if in_bounds(self.ra + i * rinc, self.fi + i * finc):
				if my_board.hasPiece(self.ra + i * rinc, self.fi + i * finc):
					self.takes.append((self.ra + i * rinc, self.fi + i * finc))
					break
				else:
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
		
		finc = -1
		
		for i in range(1, 9):
			if in_bounds(self.ra + i * rinc, self.fi + i * finc):
				if my_board.hasPiece(self.ra + i * rinc, self.fi + i * finc):
					self.takes.append((self.ra + i * rinc, self.fi + i * finc))
					break
				else:
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
		
		rinc = 1
		
		for i in range(1, 9):
			if in_bounds(self.ra + i * rinc, self.fi + i * finc):
				if my_board.hasPiece(self.ra + i * rinc, self.fi + i * finc):
					self.takes.append((self.ra + i * rinc, self.fi + i * finc))
					break
				else:
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
					

	def moveRule(self, my_board, ra, fi):
		self.gen_moves(my_board)
		
		if ((ra, fi) in self.moves):
			my_board.last_move = self.shorthand + board.space_tostr(ra, fi)
			return True
		else:
			return False
	
		"""
		if abs(ra - self.ra) == abs(fi- self.fi):
			if fi < self.fi:
				inc1 = -1
			else:
				inc1 = 1
			if ra < self.ra:
				inc2 = -1
			else:
				inc2 = 1
			
			dist = abs(fi - self.fi)

			for i in range(1, dist):
				if my_board.hasPiece(self.ra + (inc2 * i), self.fi + (inc1 * i)):
					return False
			my_board.last_move = self.shorthand + board.space_tostr(ra, fi)
			return True
		else:
			return False
		"""
	
	def takeRule(self, my_board, ra, fi):
		self.gen_moves(my_board)
		if ((ra, fi) in self.takes):
			my_board.last_move = self.take_tostr(ra, fi)
			return True
		else:
			return False

class King(Piece):
	def __init__(self, ra, fi, x, y, height, color):
		Piece.__init__(self, ra, fi, x, y, height, color)
		self.shorthand = "K"
		self.image = Piece.loadImage(board.colorKey(color, 4), height)
		
	def gen_moves(self, my_board):
		self.moves = []
		self.takes = []
	
		for i in range(-1, 2):
			for j in range(-1, 2):
				if (i, j) == (0, 0):
					continue
				ra = self.ra + i
				fi = self.fi + j
				if in_bounds(ra, fi):
					if my_board.hasPiece(ra, fi):
						self.takes.append((ra, fi))
					else:
						self.moves.append((ra, fi))
		
		if not self.hasMoved and my_board.board[self.ra][1] != 0 and not my_board.board[self.ra][1].hasMoved:
			for i in range(2, self.fi):
				if my_board.board[self.ra][i] != 0: break
			self.moves.append((self.ra, self.fi - 2))
		
		if not self.hasMoved and my_board.board[self.ra][8] != 0 and not my_board.board[self.ra][8].hasMoved:
			for i in range(self.fi, 8):
				if my_board.board[self.ra][i] != 0: break
			self.moves.append((self.ra, self.fi + 2))
			


	def moveRule(self, my_board, ra, fi):
		self.gen_moves(my_board)
		
		if ra == self.ra and fi - self.fi == -2:
			if ((ra, fi) in self.moves):
				castle = my_board.move_piece(ra, 1, ra, fi + 1)
				my_board.last_move = "O-O"
				return castle
				
		if ra == self.ra and fi - self.fi == 2:
			if ((ra, fi) in self.moves):
				castle = my_board.move_piece(ra, 8, ra, fi - 1)
				my_board.last_move = "O-O-O"
				return castle
				
		if ((ra, fi) in self.moves):
			my_board.last_move = self.shorthand + board.space_tostr(ra,fi)
			return True
		else: return False
			
		
	
		"""
		if abs(ra - self.ra) < 2 and abs(fi - self.fi) < 2:
			my_board.last_move = self.shorthand + board.space_tostr(ra, fi)
			return True

		elif not self.hasMoved: # checking for a castling move

			if abs(fi - self.fi) == 2:
					if fi < self.fi and my_board.board[ra][1] != 0 and not my_board.board[ra][1].hasMoved:
						for i in range(fi + 1, self.fi):
								if my_board.board[ra][fi] != 0:
										return False
						castle = my_board.move_piece(ra, 1, ra, fi+1)
						my_board.last_move = "O-O"
						return castle

					elif fi > self.fi and my_board.board[ra][8] != 0 and not my_board.board[ra][8].hasMoved:
						for i in range(self.fi + 1, fi):
								if my_board.board[ra][fi] != 0:
										return False
						castle = my_board.move_piece(ra, 8, ra, fi-1)
						my_board.last_move = "O-O-O"
						return castle
							
		else:
			return False
		"""

	def takeRule(self, my_board, ra, fi):
		if ((ra, fi) in self.takes):
			my_board.last_move = self.take_tostr(ra,fi)
			return True
		else:
			return False
	
		"""
		if self.moveRule(my_board, ra, fi):
			my_board.last_move = self.take_tostr(ra, fi)
			return True
		"""

class Queen(Piece):
	def __init__(self, ra, fi, x, y, height, color):
		Piece.__init__(self, ra, fi, x, y, height, color)
		self.shorthand = "Q"
		self.image = Piece.loadImage(board.colorKey(color, 5), height)

	def gen_moves(my_board):
		self.moves = []
		self.takes = []
		
		rinc = 1
		finc = 1
		
		for i in range(1, 9):
			if in_bounds(self.ra + i * rinc, self.fi + i * finc):
				if my_board.hasPiece(self.ra + i * rinc, self.fi + i * finc):
					self.takes.append((self.ra + i * rinc, self.fi + i * finc))
					break
				else:
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
		
		rinc = -1
		
		for i in range(1, 9):
			if in_bounds(self.ra + i * rinc, self.fi + i * finc):
				if my_board.hasPiece(self.ra + i * rinc, self.fi + i * finc):
					self.takes.append((self.ra + i * rinc, self.fi + i * finc))
					break
				else:
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
		
		finc = -1
		
		for i in range(1, 9):
			if in_bounds(self.ra + i * rinc, self.fi + i * finc):
				if my_board.hasPiece(self.ra + i * rinc, self.fi + i * finc):
					self.takes.append((self.ra + i * rinc, self.fi + i * finc))
					break
				else:
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
		
		rinc = 1
		
		for i in range(1, 9):
			if in_bounds(self.ra + i * rinc, self.fi + i * finc):
				if my_board.hasPiece(self.ra + i * rinc, self.fi + i * finc):
					self.takes.append((self.ra + i * rinc, self.fi + i * finc))
					break
				else:
					self.moves.append((self.ra + i * rinc, self.fi + i * finc))
					
					
		for ra in range(self.ra - 1, 0, -1):
			if my_board.hasPiece(ra, self.fi):
				self.takes.append((ra, self.fi))
				break
			else: self.moves.append((ra, self.fi))
		for ra in range(self.ra + 1, 9):
			if my_board.hasPiece(ra, self.fi):
				self.takes.append((ra, self.fi))
				break
			else: self.moves.append((ra, self.fi))
			
		for fi in range(self.fi - 1, 0, -1):
			if my_board.hasPiece(self.ra, fi):
				self.takes.append((self.ra, fi))
				break
			else: self.moves.append((self.ra, fi))
		for fi in range(self.fi + 1, 9):
			if my_board.hasPiece(self.ra, fi):
				self.takes.append((self.ra, fi))
				break
			else: self.moves.append((self.ra, fi))
		

	def moveRule(self, my_board, ra, fi):
		if abs(ra - self.ra) == abs(fi- self.fi):
			if fi < self.fi:
				inc1 = -1
			else:
				inc1 = 1
			if ra < self.ra:
				inc2 = -1
			else:
				inc2 = 1
			
			dist = abs(fi - self.fi)

			for i in range(1, dist):
				if my_board.hasPiece(self.ra + (inc2 * i), self.fi + (inc1 * i)):
					return False
			my_board.last_move = self.shorthand + board.space_tostr(ra, fi)
			return True
		elif ra == self.ra:
			if fi < self.fi:
				increment = -1
			else:
				increment = 1
			for i in range(self.fi + increment, fi, increment):
				print("Checking board["+str(ra)+"]["+str(i)+"]")
				if my_board.hasPiece(ra, i):
					return False
			my_board.last_move = self.shorthand + board.space_tostr(ra, fi)
			return True

		elif fi == self.fi:
			if ra < self.ra:
				increment = -1
			else:
				increment = 1
			for i in range(self.ra + increment, ra, increment):
				if my_board.hasPiece(i, fi):
					return False
			my_board.last_move = self.shorthand + board.space_tostr(ra, fi)
			return True
		else:
			return False
	
	def takeRule(self, my_board, ra, fi):
		if self.moveRule(my_board, ra, fi):
			my_board.last_move = self.take_tostr(ra, fi)
			return True