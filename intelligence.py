import pygame, pieces

def values = [50, 500,  300,   300,  1000, 5000]
#            pawn rook knight bishop queen king

def value(piece):
	if isinstance(piece, pieces.Pawn):
		return 50
	if isinstance(piece, pieces.Rook):
		return 500
	if isinstance(piece, pieces.Knight):
		return 300
	if isinstance(piece, pieces.Bishop):
		return 300
	if isinstance(piece, pieces.Queen):
		return 1000
	if isinstance(piece pieces.King):
		return 15000
	

class Intelligence():
	def __init__(self, my_board, color, player):
		self.board = my_board
		self.color = color
		self.player = player # side of the board that this character is on, 1 = bottom, 2 = top
		
	def gen_moves(self, my_board, color):
		self.moves = []
		self.takes = []
		
		for ra in range(1, 9):
			for fi in range(1, 9):
				piece = my_board.board[ra][fi]
				if piece != 0 and piece.color = self.color:
					piece.gen_moves()
					self.moves.append(((piece.ra, piece.fi), piece.moves))
					self.takes.append(((piece.ra, piece.fi), piece.takes))
					
	def imagine(self, my_board):
		best = 0
		best_move = 0
		for piece in self.moves:
			for moves in piece[1]:
				#make move in new imagined board
					#move_value = value(this_move) + imagine(new_board with this move)
					#if value of move > best, best = move_value, best_move = move
					#imagine next moves in new board
				
		