import pygame, board, copy

class Player():
	def __init__(self, my_board, color, posit):
		self.my_board = my_board
		self.color = color
		
		self.posit = posit # side of the board that this character is on, 1 = bottom, 2 = top
		
	# --------------------------------------------------------------------------------
	# Merge gen_moves and check_avoidance
	def gen_moves(self, my_board):	
		self.moves = []
		
		# Gen moves for all pieces, append to self.moves and self.takes
		for ra in range(1, 9):
			for fi in range(1, 9):
				piece = my_board.get_piece(ra, fi)
				if piece and self.my_piece(piece):
					piece.gen_moves(my_board)
					
					for move in piece.moves:
						self.moves.append((ra, fi, move[0], move[1]))
						
	def my_piece(self, piece):
		return self.color == piece.color
					
	def print_moves(self):
		for move in self.moves:
			print(board.move_to_str(move))
						
	# Generates checked moves by analysis of whether move will lead to an unchecked king
	# If no move is found, then player is checkmated
	def check_avoidance(self, my_board):
		checked_moves = []
		
		virt_board = board.Virtual_Board()
		virt_board.copy_board(my_board)
		virt_board.set_players(my_board.plyr1, self)
		
		for move in self.moves:
			#print("\nPossible Move: " + board.Board.file_[move[1]] + board.Board.rank_[move[0]] + " to " + board.Board.file_[move[3]] + board.Board.rank_[move[2]])
			# create new board with same pieces as my_board
			ra1 = move[0]
			fi1 = move[1]
			ra2 = move[2]
			fi2 = move[3]
			
			moved_piece = virt_board.get_piece(ra1, fi1)
			
			result = moved_piece.move(virt_board, ra2, fi2)
			
			my_board.plyr2.gen_moves(virt_board)
			virt_board.update_check(my_board.plyr1, my_board.plyr2)
			
			#print("Will take uncheck? " + str(not virt_board.is_check(self.color)))
			
			if not virt_board.is_check(self.color):
				checked_moves.append((move[0], move[1], move[2], move[3]))
				
			virt_board.undo_move()
		
		self.moves = checked_moves
		
		my_board.plyr2.gen_moves(virt_board)
	# --------------------------------------------------------------------------------
	def valid_move(self, my_board, ra1, fi1, ra2, fi2):
		piece = my_board.get_piece(ra1, fi1)
		
		# Not only must piece be in self.moves, but may have to satisfy certain special rules
		if self.in_moves(ra1, fi1, ra2, fi2) and piece:
			return True
		else: return False
						
	def in_moves(self, ra1, fi1, ra2, fi2):
		return ((ra1, fi1, ra2, fi2) in self.moves)
		
	# --------------------------------------------------------------------------------
	def move_piece(self, my_board, ra1, fi1, ra2, fi2):
		if my_board.update_checkmate(self):	return True
		
		piece = my_board.get_piece(ra1, fi1)
		
		if not piece:
			return False
			
		if self.valid_move(my_board, ra1, fi1, ra2, fi2):
			piece.move(my_board, ra2, fi2)
			return True
		else:
			return False
			