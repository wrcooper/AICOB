import pygame, pieces, random

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
	if isinstance(piece, pieces.King):
		return 15000
	

class Intelligence():
	TOP = 1
	BOT = 2

	def __init__(self, my_board, color, player):
		self.board = my_board
		self.color = color
		self.player = player # side of the board that this character is on, 1 = bottom, 2 = top
		
	def gen_moves(self, my_board, color):
		# will predict moves for both self and opponent using color argument
		self.moves = []
		self.takes = []
		
		for ra in range(1, 9):
			for fi in range(1, 9):
				piece = my_board.getPiece(ra, fi)
				if piece and piece.color == color:
					piece.gen_moves(my_board)
					
					for move in piece.moves:
						self.moves.append((piece.ra, piece.fi, move[0], move[1]))
						
					for take in piece.takes:
						self.takes.append((piece.ra, piece.fi, take[0], take[1]))
					
					
	def imagine(self, my_board, color, my_game):
		self.gen_moves(my_board, color)
		random.seed()
	
		best = 0
		best_move = 0
		
		print("\n\n" + color)
		
		possible = self.moves + self.takes
		i = int(random.uniform(0, len(possible) - 1))
		
		#for move in possible:
			# another = self.imagine(this_move, depth + 1)
			# (value, another)
			# if value > best, best_move = another
		my_board.ai_move(my_game, possible[i][0], possible[i][1], possible[i][2], possible[i][3])
		
		
		for move in self.moves:
			print("piece at: " + str(move[0]) + " " + str(move[1]) + " to " + str(move[2]) + " " + str(move[3]))
				
		for take in self.takes:
			print("piece at: " + str(take[0]) + " " + str(take[1]) + " takes " + str(take[2]) + " " + str(take[3]))
				#make move in new imagined board
					#move_value = value(this_move) + imagine(new_board with this move)
					#if value of move > best, best = move_value, best_move = move
					#imagine next moves in new board
	