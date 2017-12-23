import pygame, pieces, random, copy, board

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
	def __init__(self, my_board, color, posit):
		self.board = my_board
		self.color = color
		
		if color == "wh":	
			self.opp_color = "bl"
		else:
			self.opp_color = "wh"
		
		self.posit = posit # side of the board that this character is on, 1 = bottom, 2 = top
		
		self.takes = []
		self.moves = [] 
		
		
	# --------------------------------------------------------------------------------
	def ai_move(self, my_board, ra1, fi1, ra2, fi2):
		print("AI Moving Piece " + str(my_board.board[ra1][fi1]))
		
		piece = my_board.board[ra1][fi1]
		my_board.last_move = piece.move_str(ra2, fi2)
		piece.rect = pygame.Rect(my_board.file_to_x(fi2), my_board.rank_to_y(ra2), my_board.space_height, my_board.space_height)
		my_board.board[piece.ra][piece.fi] = 0
			
		piece.ra = ra2
		piece.fi = fi2
			
		piece.hasMoved = True
		my_board.board[ra2][fi2] = piece
		my_board.plyr1.gen_moves(my_board)
		
		my_board.update_check(my_board.plyr1, self)
		
		print("white checked? " + str(my_board.wh_check))
		print("black checked? " + str(my_board.bl_check))
		if my_board.is_check(my_board.plyr1_color):
			my_board.last_move = my_board.last_move + "+"
		
	def ai_take(self, my_board, ra1, fi1, ra2, fi2):
		piece = my_board.board[ra1][fi1]
		piece2 = my_board.board[ra2][fi2]
		
		my_board.last_move = piece.take_to_str(ra2, fi2)
		piece2 = my_board.board[ra2][fi2]
		piece2.kill()
		piece.rect = pygame.Rect(my_board.file_to_x(fi2), my_board.rank_to_y(ra2), my_board.space_height, my_board.space_height)
		piece.ra = ra2
		piece.fi = fi2
		my_board.board[ra2][fi2] = piece
		my_board.board[ra1][fi1] = 0
		my_board.plyr1.gen_moves(my_board)
		
		my_board.update_check(my_board.plyr1, self)
		print("white checked? " + str(my_board.wh_check))
		print("black checked? " + str(my_board.bl_check))
		if my_board.is_check(my_board.plyr1_color):
			my_board.last_move = my_board.last_move + "+"
	
		
	def gen_moves(self, my_board):
		# will predict moves for both self and opponent using color argument
		self.moves = []
		self.takes = []
		
		for ra in range(1, 9):
			for fi in range(1, 9):
				piece = my_board.get_piece(ra, fi)
				if piece and piece.color == self.color:
					piece.gen_moves(my_board)
					
					for move in piece.moves:
						self.moves.append((piece.ra, piece.fi, move[0], move[1]))
						
					for take in piece.takes:
						self.takes.append((piece.ra, piece.fi, take[0], take[1]))
						
						
	def gen_opp_moves(self, my_board):
		# will predict moves for both self and opponent using color argument
		self.opp_moves = []
		self.opp_takes = []
		
		for ra in range(1, 9):
			for fi in range(1, 9):
				piece = my_board.get_piece(ra, fi)
				if piece and piece.color == self.opp_color:
					piece.gen_moves(my_board)
					
					for move in piece.moves:
						self.moves.append((piece.ra, piece.fi, move[0], move[1]))
						
					for take in piece.takes:
						self.takes.append((piece.ra, piece.fi, take[0], take[1]))
						
	def gen_checked_moves(self, my_board):
		self.gen_moves(my_board)
		checked_moves = []
		checked_takes = []
		
		virt_board = board.Virtual_Board(my_board.plyr1_color)
		virt_board.board = copy.copy(my_board.board)
		
		for move in self.moves:
			# create new board with same pieces as my_board
			temp_piece = virt_board.get_piece(move[2], move[3])
			moved_piece = virt_board.get_piece(move[0], move[1])
			
			virt_board.set_space(move[2], move[3], moved_piece)
			virt_board.set_space(move[0], move[1], 0)
			my_board.plyr1.gen_moves(my_board)
			virt_board.update_check(my_board.plyr1, self)
			
			virt_board.set_space(move[0], move[1], moved_piece)
			virt_board.set_space(move[2], move[3], temp_piece)
			
			
			if not virt_board.is_check(self.color):
				checked_moves.append((move[0], move[1], move[2], move[3]))
				
		
		print("\n\nFinding possible takes...")
		for take in self.takes:
			print("\nPossible Take: " + board.Board.file_[take[1]] + board.Board.rank_[take[0]] + " to " + board.Board.file_[take[3]] + board.Board.rank_[take[2]])
			temp_piece = virt_board.get_piece(take[2], take[3])
			taking_piece = virt_board.get_piece(take[0], take[1])
			
			virt_board.set_space(take[2], take[3], taking_piece)
			virt_board.set_space(take[0], take[1], 0)
			my_board.plyr1.gen_moves(my_board)
			virt_board.update_check(my_board.plyr1, self)
			
			#print(str(virt_board.takes))
			
			for player_take in virt_board.takes:
				print("Player threatens: " + board.Board.file_[player_take[1]] + board.Board.rank_[player_take[0]] + " to " + board.Board.file_[player_take[3]] + board.Board.rank_[player_take[2]])
			
			virt_board.set_space(take[0], take[1], taking_piece)
			virt_board.set_space(take[2], take[3], temp_piece)
			
			print("Will take uncheck? " + str(not virt_board.is_check(self.color)))
			
			if not virt_board.is_check(self.color):
				checked_takes.append((take[0], take[1], take[2], take[3]))
				
		for move in checked_moves:
			print("ai uncheck move is " + str(move))
			
		for take in checked_takes:
			print("ai uncheck take is " + str(take))
			
		self.moves = checked_moves
		self.takes = checked_takes
					
					
	def imagine(self, my_board, color, my_game):
		if my_board.is_check(self.color):
			print("\nAI is checked: self.color = " + self.color + " color = " + color)
			self.gen_checked_moves(my_board)
		else:
			self.gen_moves(my_board)
		
		random.seed()
	
		best = 0
		best_move = 0
		
		#print("\n\n" + color)
		
		possible = self.moves + self.takes
		i = int(random.uniform(0, len(possible) - 1))
		
		
		#print("ai chosen move = " + str(possible[i][0]) + str(possible[i][1]) + str(possible[i][2]) + str(possible[i][3]))
		
		#for move in possible:
			# another = self.imagine(this_move, depth + 1)
			# (value, another)
			# if value > best, best_move = another
		if ((possible[i][0], possible[i][1], possible[i][2], possible[i][3]) in self.takes):
			self.ai_take(my_board, possible[i][0], possible[i][1], possible[i][2], possible[i][3])	
			my_game.next_move(my_board)
		else: 
			self.ai_move(my_board, possible[i][0], possible[i][1], possible[i][2], possible[i][3])
			my_game.next_move(my_board)
		
		
		
		"""for move in self.moves:
			print("piece at: " + str(move[0]) + " " + str(move[1]) + " to " + str(move[2]) + " " + str(move[3]))
				
		for take in self.takes:
			print("piece at: " + str(take[0]) + " " + str(take[1]) + " takes " + str(take[2]) + " " + str(take[3]))"""
				#make move in new imagined board
					#move_value = value(this_move) + imagine(new_board with this move)
					#if value of move > best, best = move_value, best_move = move
					#imagine next moves in new board
	