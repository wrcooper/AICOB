import pygame, board, pieces

class Game():
	def __init__(self, player_color):
		self.sequence = [] 
		self.turn_number = 1
		self.player_color = player_color
		self.current_move = "wh"
		self.pgn = ""

	def next_move(self, my_board):
		self.sequence.append(my_board.last_move)
		if self.current_move == "wh":
			self.current_move = "bl"
			
			for ra in range(9):
				for fi in range(9):
					piece = my_board.board[ra][fi]
					if isinstance(piece, pieces.Pawn):	
						if piece.color == "bl":
							piece.en_passant_able = False
		else:	
			self.next_turn()
			self.current_move = "wh"
	
			for ra in range(9):
				for fi in range(9):
					piece = my_board.board[ra][fi]
					if isinstance(piece, pieces.Pawn):	
						if piece.color == "wh":
							piece.en_passant_able = False
		
			
		self.generate_pgn()

	def next_turn(self):
		self.turn_number += 1 
		
	def generate_pgn(self):
		self.pgn = ""
		for i in range(len(self.sequence)):
			if i % 2 == 0:
				self.pgn += str(int(i/2 + 1)) + ". "
			self.pgn += self.sequence[i] + " " 
		
