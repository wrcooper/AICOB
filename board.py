import pygame, math, inspect
from chess import *
from game import *

player_color = "wh"

class Board():
	file_ = ['', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
	rank_ = ['', '8', '7', '6', '5', '4', '3', '2', '1']

	def __init__(self, height, edge_dist, player, screen):
		self.screen = screen
		self.player = player
		self.rect = pygame.Rect(edge_dist, 0, height, height)
		global player_color
		player_color = player
		self.board = [[0 for x in range(9)] for y in range(9)]
		self.height = height
		self.edge_dist = edge_dist
		self.space_height = height/8
		self.last_move = None
		self.turn = 0


	def set_background(self, background):
		self.background = background


	def space_to_rect(self, ra, fi):
		y = (ra - 1) * self.space_height
		x = (fi-1) * self.space_height + self.edge_dist
		return Rect(x, y, self.space_height, self.space_height)
	
	def coord_to_space(self, x, y):
		ra = math.ceil(y/self.space_height)
		fi = math.ceil((x - self.edge_dist)/self.space_height)
		return (ra, fi)


	def rank_to_y(self, ra):
		y = (ra - 1) * self.space_height
		return y
	
	def file_to_x(self, fi):
		x = (fi-1) * self.space_height + self.edge_dist
		return x

	def y_to_rank(self, y):
		rank = math.ceil(y/self.space_height)
		return rank
	
	def x_to_file(self, x):
		fi = math.ceil((x - self.edge_dist)/self.space_height)
		return fi
	
	
	def init_pieces(self, color1):
		if color1 == "wh":
			color2 = "bl"
		else:
			color2 = "wh"
		
		order = [color1, color2]
		row2 = [7, 2]
		row1 = [8, 1]

		for i in range(1, -1, -1):
			for fi in range(1, 9):
				self.makePiece("", row2[i], fi, order[i])
			self.makePiece("R", row1[i], 1, order[i])
			self.makePiece("R", row1[i], 8, order[i])
			self.makePiece("N", row1[i], 2, order[i])
			self.makePiece("N", row1[i], 7, order[i])
			self.makePiece("B", row1[i], 3, order[i])
			self.makePiece("B", row1[i], 6, order[i])
			self.makePiece("K", row1[i], 4, order[i])
			self.makePiece("Q", row1[i], 5, order[i])


	def draw(self, screen):
		colors = [(56,23,19), (249, 190, 102)]
		current = 0
		space_height = self.space_height
		for i in range(9):
			for j in range(9):
				if current == 2:
					current = 0
				x_distance = space_height * i
				y_distance = space_height * j
				screen.fill(colors[current], pygame.Rect(x_distance,y_distance,space_height,space_height))
				current += 1

	def draw_pieces(self, screen):
		for ra in range(1, 9):
			for fi in range(1, 9):
				piece = getPiece(ra, fi)
				screen.blit(piece.image, position_to_pixels(ra, fi))
	
	def getPiece(self, ra, fi):
		return self.board[ra][fi]


	def makePiece(self, piece, ra, fi, color):
		x = self.file_to_x(fi)
		y = self.rank_to_y(ra)
		if piece == "":
			piece = Pawn(ra, fi, x, y, self.space_height, color)
		elif piece == "R":
			piece = Rook(ra, fi, x, y, self.space_height, color)
		elif piece == "N":
			piece = Knight(ra, fi, x, y, self.space_height, color)
		elif piece == "B":
			piece = Bishop(ra, fi, x, y, self.space_height, color)
		elif piece == "K":
			piece = King(ra, fi, x, y, self.space_height, color)
		elif piece == "Q":
			piece = Queen(ra, fi, x, y, self.space_height, color)
		self.board[ra][fi] = piece

	def checkPlayer(self, game, piece):
		if game.player == piece.color:
			return True
		else: return False
	
	def checkColor(self, piece1, piece2):
			if piece1.color != piece2.color:
					return True
			else:
					return False

	def validMove(self, ra, fi, piece):
		return piece.validMove(self, ra, fi)

	def pieceHeld(self, game, ra, fi, group):
		if ra < 1 or ra > 8 or fi < 1 or fi > 8:
			return False
		
		piece = self.board[ra][fi]
		if piece == 0 or piece.color != game.player or piece.color != game.current_move: 
			return False

		# update piece location to follow mouse
		group.move_to_front(piece)
		piece.rect = pygame.Rect( pygame.mouse.get_pos()[0] - (self.space_height / 2), 
		pygame.mouse.get_pos()[1] - (self.space_height / 2), self.space_height, self.space_height)
		
		# draw highlighted spaces
		self.next_highlight = self.highlight(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
		self.current_highlight = self.highlight_current(ra, fi)

	def pieceReleased(self, game, ra1, fi1, ra2, fi2):
		piece = self.board[ra1][fi1]
		if piece == 0:
			return False
		if piece.color != game.player or piece.color != game.current_move:
			return False
		if self.move_piece(ra1, fi1, ra2, fi2):
			game.next_move(self)
		else:
			self.pieceReset(ra1, fi1)
		self.next_highlight.kill()
		self.current_highlight.kill()


	def highlight(self, x, y):
		space = self.coord_to_space(x, y)
		ra = space[0]
		fi = space[1]
		highlight = Highlight(ra, fi, self)
		return highlight
	
	def highlight_current(self, ra, fi):
		highlight = Highlight_Current(ra, fi, self)
		return highlight

	def pieceReset(self, ra, fi):
		if ra < 1 or ra > 8 or fi < 1 or fi > 8:
			return False
		piece = self.board[ra][fi]
		if piece == 0:
			return False
		piece.rect = pygame.Rect(self.file_to_x(fi), self.rank_to_y(ra), self.space_height, self.space_height)
		return False
	
	def move_piece(self, ra1, fi1, ra, fi):
		if ra < 1 or ra > 8 or fi < 1 or fi > 8:
			return False
		piece = self.board[ra1][fi1]
		if piece == 0:
			return False
		if self.hasPiece(ra, fi):
			return self.takePiece(ra1, fi1, ra, fi)
		elif self.validMove(ra, fi, piece):
			print("Moving Piece " + str(self.board[ra1][fi1]))
			piece.rect = pygame.Rect(self.file_to_x(fi), self.rank_to_y(ra), self.space_height, self.space_height)
			self.board[piece.ra][piece.fi] = 0
			piece.ra = ra
			piece.fi = fi
			piece.hasMoved = True
			self.board[ra][fi] = piece
			return True
		else:
			return False
	
	def takePiece(self, ra1, fi1, ra, fi):
		piece = self.board[ra1][fi1]
		piece2 = self.board[ra][fi]
		if self.checkColor(piece, piece2) and piece.validTake(self, ra, fi):
			piece2 = self.board[ra][fi]
			piece2.kill()
			piece.rect = pygame.Rect(self.file_to_x(fi), self.rank_to_y(ra), self.space_height, self.space_height)
			piece.ra = ra
			piece.fi = fi
			self.board[ra][fi] = piece
			self.board[ra1][fi1] = 0
			return True
		else:
			return False 


	def hasPiece(self, ra, fi):
		if self.board[ra][fi] == 0:
			return False
		else:
			return True
	
def colorKey(color, n):
	if (color == "bl"):
		return n + 6
	else:
		return n
	
def space_tostr(ra, fi):
	return (str(Board.file_[fi]) + str(Board.rank_[ra]))


class Highlight(pygame.sprite.Sprite):
	def __init__(self, ra, fi, board):
		pygame.sprite.Sprite.__init__(self, self.containers)
		rect = board.space_to_rect(ra, fi)
		self.rect = rect
		s = pygame.Surface((rect.width, rect.height))
		s.set_alpha(100)
		s.fill((255, 180, 60))
		self.image = s

class Highlight_Current(pygame.sprite.Sprite):
	def __init__(self, ra, fi, board):
		pygame.sprite.Sprite.__init__(self, self.containers)
		rect = board.space_to_rect(ra, fi)
		self.rect = rect
		s = pygame.Surface((self.rect.width, self.rect.height))
		s.set_alpha(100)
		s.fill((255, 160, 40))
		self.image = s

class Piece(pygame.sprite.Sprite):
	images = []
	def __init__(self, ra, fi, x, y, height, color):
		pygame.sprite.Sprite.__init__(self, self.containers)
		self.rect = pygame.Rect(x, y, height, height)
		self.hasMoved = False
		self.color = color
		self.ra = ra
		self.fi = fi
	
	def loadImage(n, height):
		return (pygame.transform.scale(Piece.images[n], (int(height), int(height))))

	def take_tostr(self, ra, fi):
		return self.shorthand + "x" + space_tostr(ra, fi)

	def pos_to_str(ra, fi):
		pos = str(Board.file_[fi]) + str(ra)
		return pos

	def direction(self):
		if self.color == player_color:
			return -1
		else:
			return 1
	
	def possibleMove(self, ra, fi):
		if ra > 0 and ra < 9 and (ra, fi) != (self.ra, self.fi) and fi > 0 and fi < 9:
			return True
		else:
			return False

	def validTake(self, board, ra, fi):
		if self.possibleMove(ra, fi) and self.takeRule(board, ra, fi) and self.color != board.board[ra][fi].color:
			return True

	def validMove(self, board, ra, fi):
		if self.possibleMove(ra, fi) and self.moveRule(board, ra, fi):
			return True

	
	


class Pawn(Piece):
	def __init__(self, ra, fi, x, y, height, color):
		Piece.__init__(self, ra, fi, x, y, height, color)
		self.en_passant_able = False
		self.shorthand = ""
		self.image = Piece.loadImage(colorKey(color, 0), height)

	# returns a list of possible moves in the form of (ra, fi)
	def validMoves():
		moves = []
		# if piece hasn't moved, then (ra + direction * 2, fi)
		# (ra + direction, fi)
		# (ra + direction, fi + 1)
		# (ra + direction, fi - 1)
		# en passant
		
	def moveRule(self, board, ra, fi):
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
	
	def takeRule(self, board, ra, fi):
		if abs(fi - self.fi) == 1 and ra - self.ra == self.direction():
			board.last_move = Board.file_[self.fi] + self.take_tostr(ra, fi)
			return True
		else:
			return False
		

class Rook(Piece):
	def __init__(self, ra, fi, x, y, height, color):
		Piece.__init__(self, ra, fi, x, y, height, color)
		self.shorthand = "R"
		self.image = Piece.loadImage(colorKey(color, 1), height)


	def moveRule(self, board, ra, fi):
		if ra == self.ra:
			if fi < self.fi:
				increment = -1
			else:
				increment = 1
			for i in range(self.fi + increment, fi, increment):
				if board.hasPiece(ra, i):
					return False
			board.last_move = self.shorthand + space_tostr(ra, fi)
			return True

		elif fi == self.fi:
			if ra < self.ra:
				increment = -1
			else:
				increment = 1
			for i in range(self.ra + increment, ra, increment):
				if board.hasPiece(i, fi):
					return False
			board.last_move = self.shorthand + space_tostr(ra, fi)
			return True
		else:
			return False

	def takeRule(self, board, ra, fi):
		if self.moveRule(board, ra, fi):
			board.last_move = self.take_tostr(ra, fi)
			return True

class Knight(Piece):
	def __init__(self, ra, fi, x, y, height, color):
		Piece.__init__(self, ra, fi, x, y, height, color)
		self.shorthand = "N"
		self.image = Piece.loadImage(colorKey(color, 2), height)


	def moveRule(self, board, ra, fi):
		if abs(fi - self.fi) == 2:
			if abs(ra - self.ra) == 1:
				board.last_move = self.shorthand + space_tostr(ra, fi)
				return True
		elif abs(ra - self.ra) == 2:
			if abs(fi - self.fi) == 1:
				board.last_move = self.shorthand + space_tostr(ra, fi)
				return True
		else:
			return False
	
	def takeRule(self, board, ra, fi):
		if self.moveRule(board, ra, fi):
			board.last_move = self.take_tostr(ra, fi)
			return True


class Bishop(Piece):
	def __init__(self, ra, fi, x, y, height, color):
		Piece.__init__(self, ra, fi, x, y, height, color)
		self.shorthand = "B"
		self.image = Piece.loadImage(colorKey(color, 3), height)


	def moveRule(self, board, ra, fi):
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
				if board.hasPiece(self.ra + (inc2 * i), self.fi + (inc1 * i)):
					return False
			board.last_move = self.shorthand + space_tostr(ra, fi)
			return True
		else:
			return False
	
	def takeRule(self, board, ra, fi):
		if self.moveRule(board, ra, fi):
			board.last_move = self.take_tostr(ra, fi)
			return True

class King(Piece):
	def __init__(self, ra, fi, x, y, height, color):
		Piece.__init__(self, ra, fi, x, y, height, color)
		self.shorthand = "K"
		self.image = Piece.loadImage(colorKey(color, 4), height)


	def moveRule(self, board, ra, fi):
		if abs(ra - self.ra) < 2 and abs(fi - self.fi) < 2:
			board.last_move = self.shorthand + space_tostr(ra, fi)
			return True

		elif not self.hasMoved: # checking for a castling move

			if abs(fi - self.fi) == 2:
					if fi < self.fi and board.board[ra][1] != 0 and not board.board[ra][1].hasMoved:
						for i in range(fi + 1, self.fi):
								if board.board[ra][fi] != 0:
										return False
						castle = board.move_piece(ra, 1, ra, fi+1)
						board.last_move = "O-O"
						return castle

					elif fi > self.fi and board.board[ra][8] != 0 and not board.board[ra][8].hasMoved:
						for i in range(self.fi + 1, fi):
								if board.board[ra][fi] != 0:
										return False
						castle = board.move_piece(ra, 8, ra, fi-1)
						board.last_move = "O-O-O"
						return castle
							
		else:
			return False


	def takeRule(self, board, ra, fi):
		if self.moveRule(board, ra, fi):
			board.last_move = self.take_tostr(ra, fi)
			return True
			

class Queen(Piece):
	def __init__(self, ra, fi, x, y, height, color):
		Piece.__init__(self, ra, fi, x, y, height, color)
		self.shorthand = "Q"
		self.image = Piece.loadImage(colorKey(color, 5), height)


	def moveRule(self, board, ra, fi):
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
				if board.hasPiece(self.ra + (inc2 * i), self.fi + (inc1 * i)):
					return False
			board.last_move = self.shorthand + space_tostr(ra, fi)
			return True
		elif ra == self.ra:
			if fi < self.fi:
				increment = -1
			else:
				increment = 1
			for i in range(self.fi + increment, fi, increment):
				print("Checking board["+str(ra)+"]["+str(i)+"]")
				if board.hasPiece(ra, i):
					return False
			board.last_move = self.shorthand + space_tostr(ra, fi)
			return True

		elif fi == self.fi:
			if ra < self.ra:
				increment = -1
			else:
				increment = 1
			for i in range(self.ra + increment, ra, increment):
				if board.hasPiece(i, fi):
					return False
			board.last_move = self.shorthand + space_tostr(ra, fi)
			return True
		else:
			return False
	
	def takeRule(self, board, ra, fi):
		if self.moveRule(board, ra, fi):
			board.last_move = self.take_tostr(ra, fi)
			return True




'''

	def checkMove(ra1, fi1, ra2, fi2): #check if a valid move is being attempted

	def move_piece(ra1, fi1, ra2, fi2):

	def killPiece(ra, fi):
'''

