import pygame

class Game():
	def __init__(self, player_color):
		self.sequence = [] 
		self.turn_number = 1
		self.player_color = player_color
		self.current_move = "wh"
		self.pgn = ""

	def next_move(self, board):
        	#TODO: store move in array: i.e. rXd4 
	    	# sequence of moves in 2 array as such:
    		# [white move]
    		# [black move]
		self.sequence.append(board.last_move)
		if self.current_move == "wh":
			self.current_move = "bl"
		else:	
			self.next_turn()
			self.current_move = "wh"
			
		self.generate_pgn()

	def next_turn(self):
		self.turn_number += 1 
		
	def generate_pgn(self):
		self.pgn = ""
		for i in range(len(self.sequence)):
			if i % 2 == 0:
				self.pgn += str(int(i/2 + 1)) + ". "
			self.pgn += self.sequence[i] + " " 
		
