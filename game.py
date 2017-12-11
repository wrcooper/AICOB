import pygame

class Game():
	def __init__(self, player_color):
		self.sequence = [] 
		self.turn_number = 1
		self.player = player_color
		self.current_move = "wh"

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

	def next_turn(self):
		self.turn_number += 1 
	
