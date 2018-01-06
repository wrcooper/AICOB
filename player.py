import pygame, board, copy

class Player():
	def __init__(self, my_board, color, posit):
		self.my_board = my_board
		self.color = color
		
		if color == "wh":	
			self.opp_color = "bl"
		else:
			self.opp_color = "wh"
		
		self.posit = posit # side of the board that this character is on, 1 = bottom, 2 = top
		
	# --------------------------------------------------------------------------------
	# Merge gen_moves and check_avoidance
	def gen_moves(self, my_board):	
		self.moves = []
		self.takes = []
		
		# Gen moves for all pieces, append to self.moves and self.takes
		for ra in range(1, 9):
			for fi in range(1, 9):
				piece = my_board.get_piece(ra, fi)
				if piece and my_board.check_player(piece):
					piece.gen_moves(my_board)
					
					for move in piece.moves:
						self.moves.append((ra, fi, move[0], move[1]))
						
					for take in piece.takes:
						self.takes.append((ra, fi, take[0], take[1]))
						
	# Generates checked moves by analysis of whether move will lead to an unchecked king
	# If no move is found, then player is checkmated
	def check_avoidance(self, my_board):
		checked_moves = []
		checked_takes = []
		
		virt_board = board.Virtual_Board(my_board.plyr1_color)
		virt_board.copy_board(my_board)
		
		for move in self.moves:
			#print("\nPossible Move: " + board.Board.file_[move[1]] + board.Board.rank_[move[0]] + " to " + board.Board.file_[move[3]] + board.Board.rank_[move[2]])
			# create new board with same pieces as my_board
			ra1 = move[0]
			fi1 = move[1]
			ra2 = move[2]
			fi2 = move[3]
			
			temp_piece = virt_board.get_piece(ra2, fi2)
			moved_piece = virt_board.get_piece(ra1, fi1)
			
			moved_piece.ra, moved_piece.fi = ra2, fi2
			if temp_piece: temp_piece.valid = False
			
			virt_board.set_space(ra2, fi2, moved_piece)
			virt_board.set_space(ra1, fi1, 0)
			
			my_board.plyr2.gen_moves(virt_board)
			virt_board.update_check(my_board.plyr1, my_board.plyr2)
			
			virt_board.set_space(ra1, fi1, moved_piece)
			virt_board.set_space(ra2, fi2, temp_piece)
			
			moved_piece.ra, moved_piece.fi = ra1, fi1
			if temp_piece: temp_piece.valid = True
			
			#print("Will take uncheck? " + str(not virt_board.is_check(self.color)))
			
			if not virt_board.is_check(self.color):
				checked_moves.append((move[0], move[1], move[2], move[3]))
				
		
		#print("\n\nFinding possible takes...")
		for take in self.takes:
			#print("\nPossible Move: " + board.Board.file_[move[1]] + board.Board.rank_[move[0]] + " to " + board.Board.file_[move[3]] + board.Board.rank_[move[2]])
			# create new board with same pieces as my_board
			ra1 = take[0]
			fi1 = take[1]
			ra2 = take[2]
			fi2 = take[3]
			
			temp_piece = virt_board.get_piece(ra2, fi2)
			moved_piece = virt_board.get_piece(ra1, fi1)
			
			moved_piece.ra, moved_piece.fi = ra2, fi2
			if temp_piece: temp_piece.valid = False
			
			virt_board.set_space(ra2, fi2, moved_piece)
			virt_board.set_space(ra1, fi1, 0)
			
			my_board.plyr2.gen_moves(virt_board)
			virt_board.update_check(my_board.plyr1, my_board.plyr2)
			
			virt_board.set_space(ra1, fi1, moved_piece)
			virt_board.set_space(ra2, fi2, temp_piece)
			
			moved_piece.ra, moved_piece.fi = ra1, fi1
			if temp_piece: temp_piece.valid = True
			
			#print("Will take uncheck? " + str(not virt_board.is_check(self.color)))
			
			if not virt_board.is_check(self.color):
				checked_takes.append((take[0], take[1], take[2], take[3]))

		my_board.plyr2.gen_moves(my_board)
		
		
		print("moves after check_avoidance: ")
		print(self.moves)
		print("takes after check_avoidance: ")
		print(self.takes)
		
		self.moves = checked_moves
		self.takes = checked_takes
	
	# --------------------------------------------------------------------------------
	def valid_move(self, my_board, ra1, fi1, ra2, fi2):
		piece = my_board.board[ra1][fi1]
		
		# Not only must piece be in self.moves, but may have to satisfy certain special rules
		if self.in_moves(ra1, fi1, ra2, fi2):
			return piece.valid_move(my_board, ra2, fi2)
		else: return False
						
	def in_takes(self, ra1, fi1, ra2, fi2):
		return ((ra1, fi1, ra2, fi2) in self.takes)
		
	def in_moves(self, ra1, fi1, ra2, fi2):
		return ((ra1, fi1, ra2, fi2) in self.moves)
		
	# --------------------------------------------------------------------------------
	def move_piece(self, my_board, ra1, fi1, ra, fi):
		if my_board.update_checkmate(self):	return True
			
		piece = my_board.get_piece(ra1, fi1)
		
		if not piece:
			return False
			
		if self.in_takes(ra1, fi1, ra, fi):
			return self.takePiece(my_board, ra1, fi1, ra, fi)
			
		elif self.valid_move(my_board, ra1, fi1, ra, fi):
			my_board.last_move = piece.move_str(ra, fi)
			
			piece.rect = pygame.Rect(my_board.file_to_x(fi), my_board.rank_to_y(ra), my_board.space_height, my_board.space_height)
			my_board.set_space(piece.ra, piece.fi, 0)
			piece.ra = ra
			piece.fi = fi
			
			piece.hasMoved = True
			
			my_board.set_space(ra, fi, piece)
			self.gen_moves(my_board)
			return True
		else:
			return False
			
	def takePiece(self, my_board, ra1, fi1, ra, fi):
		piece = my_board.get_piece(ra1, fi1)
		piece2 = my_board.get_piece(ra, fi)
		
		if not piece or not piece2:
			return False

		if piece.valid_take(my_board, ra, fi):
			my_board.last_move = piece.take_to_str(ra, fi)
			piece2.kill()
			
			piece.rect = pygame.Rect(my_board.file_to_x(fi), my_board.rank_to_y(ra), my_board.space_height, my_board.space_height)
			piece.ra = ra
			piece.fi = fi
			
			my_board.set_space(ra, fi, piece)
			my_board.set_space(ra1, fi1, 0)
			self.gen_moves(my_board)
			return True
		else:
			return False 