import pygame, board, pieces, player, intelligence as intel

class Game():
	def __init__(self, player_color):
		self.sequence = [] 
		self.turn_number = 1
		self.player_color = player_color
		self.current_move = "wh"
		self.pgn = ""
		self.depth = 3
		
		self.player2 = "Computer"
		self.player1 = "Human"

	# BEGIN the NEXT MOVE of the game
	def next_move(self):
	
		self.sequence.append(self.my_board.last_move)
		
		if self.check_end():
			return
	
		if self.current_move == "wh":
			self.current_move = "bl"
			
			self.reset_en_passant()
			
		elif self.current_move == "bl":	
			self.next_turn()
			self.current_move = "wh"
	
			self.reset_en_passant()
		
		self.generate_pgn()
	
	# RESET the EN PASSANT FLAG of each PAWN
	def reset_en_passant(self):
		for ra in range(9):
			for fi in range(9):
				piece = self.my_board.board[ra][fi]
				if isinstance(piece, pieces.Pawn):	
					if piece.color == self.current_move:
						piece.en_passant_able = False
	
	def toggle_player(self):
		if self.player1 == "Computer":
			plyr = player.Player(self.my_board, "wh", board.Board.BOT)
			self.my_board.plyr1 = plyr
			self.my_board.plyr2.set_opp(plyr)
			plyr.gen_moves(self.my_board)
			self.player1 = "Player"
		else:
			plyr = intel.Intelligence(self.my_board, "wh", board.Board.BOT)
			self.my_board.plyr1 = plyr
			self.my_board.plyr2.set_opp(plyr)
			plyr.gen_moves(self.my_board)
			self.player1 = "Computer"
						
	def check_end(self):
		if self.my_board.checkmate != False:
			self.end_game()
			return True
			
	def end_game(self):
		self.current_move = None
		if self.my_board.checkmate == "wh":
			self.winner = "Black"
			self.my_board.open_end_game((0,0,0))
		elif self.my_board.checkmate == "bl":
			self.winner = "White"
			self.my_board.open_end_game((255,255,255))
		elif self.my_board.checkmate == "dr":
			self.winner = "Draw"
			self.my_board.open_end_game((125,125,125))
						
	def set_board(self, my_board):
		self.my_board = my_board
		
	def new_game(self):
		self.my_board.interface.game_end = False
		self.checkmate = False
		self.pgn = ""
		self.sequence = [] 
		self.turn_number = 1
		self.my_board.init_pieces("wh")
		self.current_move = "wh"

	# INCREMENT TURN NUMBER
	def next_turn(self):
		self.turn_number += 1 
		
	# APPEND EACH MOVE to PGN
	def generate_pgn(self):
		self.pgn = ""
		for i in range(len(self.sequence)):
			if i % 2 == 0:
				self.pgn += str(int(i/2 + 1)) + ". "
			self.pgn += self.sequence[i] + " " 
		
