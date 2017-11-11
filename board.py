import pygame, math
from chess import *

player_color = "wh"

class Board():
	file_ = ['', 'a', 'b', 'c', 'd', 'e', 'f', 'g']
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
				self.makePiece("p", row2[i], fi, order[i])
			self.makePiece("r", row1[i], 1, order[i])
			self.makePiece("r", row1[i], 8, order[i])
			self.makePiece("k", row1[i], 2, order[i])
			self.makePiece("k", row1[i], 7, order[i])
			self.makePiece("b", row1[i], 3, order[i])
			self.makePiece("b", row1[i], 6, order[i])
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

		#screen.fill((40, 10, 1),pygame.Rect(x,y,height,height))
		#board_rect = pygame.draw.rect(screen, (142, 80, 0), pygame.Rect(x, y, height, height))
		#screen.blit(board_rect)

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
		if piece == "p":
			piece = Piece.makePawn(ra, fi, x, y, self.space_height, color)
		elif piece == "r":
			piece = Piece.makeRook(ra, fi, x, y, self.space_height, color)
		elif piece == "k":
			piece = Piece.makeKnight(ra, fi, x, y, self.space_height, color)
		elif piece == "b":
			piece = Piece.makeBishop(ra, fi, x, y, self.space_height, color)
		elif piece == "K":
			piece = Piece.makeKing(ra, fi, x, y, self.space_height, color)
		elif piece == "Q":
			piece = Piece.makeQueen(ra, fi, x, y, self.space_height, color)
		self.board[ra][fi] = piece

	def checkPlayer(self, piece):
		if self.player == piece.color:
			return True
		else: return False

	def validMove(self, ra, fi, piece):
		return piece.validMove(self, ra, fi)

	def pieceHeld(self, ra, fi):
		piece = self.board[ra][fi]
		if piece == 0:
			return False
		piece.rect = pygame.Rect( pygame.mouse.get_pos()[0] - (self.space_height / 2), 
		pygame.mouse.get_pos()[1] - (self.space_height / 2), self.space_height, self.space_height)
		self.cur_highlight = self.highlight(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

	def pieceReleased(self, ra1, fi1, ra2, fi2):
		if not self.movePiece(ra1, fi1, ra2 ,fi2):
			self.pieceReset(ra1, fi1)
		self.cur_highlight.kill()


	def highlight(self, x, y):
		print(x, y)
		space = self.coord_to_space(x, y)
		ra = space[0]
		fi = space[1]
		print(ra, fi)
		highlight = Highlight(ra, fi, self)
		return highlight

	def pieceReset(self, ra, fi):
		piece = self.board[ra][fi]
		if piece == 0:
			return False
		piece.rect = pygame.Rect(self.file_to_x(fi), self.rank_to_y(ra), self.space_height, self.space_height)
	
	def movePiece(self, ra1, fi1, ra, fi):
		piece = self.board[ra1][fi1]
		if piece == 0:
			return False
		print("right player? " + str(self.checkPlayer(piece)) + " valid move? " + str(self.validMove(ra, fi, piece)))
		if self.hasPiece(ra, fi):
			self.takePiece(ra1, fi1, ra, fi)
		elif self.checkPlayer(piece) and self.validMove(ra, fi, piece):
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
		if self.checkPlayer(piece) and piece.validTake(self, ra, fi):
			deadPiece = self.board[ra][fi]
			deadPiece.kill()
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

class Highlight(pygame.sprite.Sprite):
	def __init__(self, ra, fi, board):
		pygame.sprite.Sprite.__init__(self, self.containers)
		rect = board.space_to_rect(ra, fi)
		self.rect = rect
		s = pygame.Surface((rect.width, rect.height))
		s.set_alpha(100)
		s.fill((255, 180, 60))
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

	def makePawn(ra, fi, x, y, height, color):
		pawn = Pawn(ra, fi, x, y, height, color)
		pawn.image = Piece.loadImage(colorKey(color, 0), height)
		return pawn
	
	def makeRook(ra, fi, x, y, height, color):
		rook = Rook(ra, fi, x, y, height, color)
		rook.image = Piece.loadImage(colorKey(color, 1), height)
		return rook

	def makeKnight(ra, fi, x, y, height, color):
		knight = Knight(ra, fi, x, y, height, color)
		knight.image = Piece.loadImage(colorKey(color, 2), height)
		return knight

	def makeBishop(ra, fi, x, y, height, color):
		bishop = Bishop(ra, fi, x, y, height, color)
		bishop.image = Piece.loadImage(colorKey(color, 3), height)
		return bishop
	
	def makeKing(ra, fi, x, y, height, color):
		king = King(ra, fi, x, y, height, color)
		king.image = Piece.loadImage(colorKey(color, 4), height)
		return king
	
	def makeQueen(ra, fi, x, y, height, color):
		queen = Queen(ra, fi, x, y, height, color)
		queen.image = Piece.loadImage(colorKey(color, 5), height)
		return queen
	
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
	def moveRule(self, board, ra, fi):
		if ra == (self.ra + (self.direction() * 1)) and fi == self.fi:
			return True
		elif not self.hasMoved:
			if ra == (self.ra + (self.direction() * 2)) and fi == self.fi:
				if not board.hasPiece(self.ra + (self.direction()), self.fi):
					return True
		else:
			return False
	
	def takeRule(self, board, ra, fi):
		if abs(fi - self.fi) == 1 and ra - self.ra == self.direction():
			return True
		else:
			return False
		

class Rook(Piece):
	def moveRule(self, board, ra, fi):
		if ra == self.ra:
			if fi < self.fi:
				increment = -1
			else:
				increment = 1
			for i in range(self.fi + increment, fi, increment):
				if board.hasPiece(ra, i):
					return False
			return True

		elif fi == self.fi:
			if ra < self.ra:
				increment = -1
			else:
				increment = 1
			for i in range(self.ra + increment, ra, increment):
				if board.hasPiece(i, fi):
					return False
			return True
		else:
			return False

	def takeRule(self, board, ra, fi):
		return self.moveRule(board, ra, fi)

class Knight(Piece):
	def moveRule(self, board, ra, fi):
		if abs(fi - self.fi) == 2:
			if abs(ra - self.ra) == 1:
				return True
		elif abs(ra - self.ra) == 2:
			if abs(fi - self.fi) == 1:
				return True
		else:
			return False
	
	def takeRule(self, board, ra, fi):
		return self.moveRule(board, ra, fi)


class Bishop(Piece):
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
			return True
		else:
			return False
	
	def takeRule(self, board, ra, fi):
		return self.moveRule(board, ra, fi)

class King(Piece):
	def moveRule(self, board, ra, fi):
		if abs(ra - self.ra) < 2 and abs(fi - self.fi) < 2:
			return True
		else:
			return False

	def takeRule(self, board, ra, fi):
		return self.moveRule(board, ra, fi)

class Queen(Piece):
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
			return True

		elif fi == self.fi:
			if ra < self.ra:
				increment = -1
			else:
				increment = 1
			for i in range(self.ra + increment, ra, increment):
				if board.hasPiece(i, fi):
					return False
			return True
		else:
			return False
	
	def takeRule(self, board, ra, fi):
		return self.moveRule(board, ra, fi)




'''

	def checkMove(ra1, fi1, ra2, fi2): #check if a valid move is being attempted

	def movePiece(ra1, fi1, ra2, fi2):

	def killPiece(ra, fi):
'''

