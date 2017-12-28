import pygame, pieces, random, copy, board

def value(piece):
	if isinstance(piece, pieces.Pawn):
		return 50
	elif isinstance(piece, pieces.Rook):
		return 500
	elif isinstance(piece, pieces.Knight):
		return 300
	elif isinstance(piece, pieces.Bishop):
		return 300
	elif isinstance(piece, pieces.Queen):
		return 1000
	elif isinstance(piece, pieces.King):
		return 15000
	else: return 1
	

class Intelligence():
	def __init__(self, my_board, color, posit):
		self.board = my_board
		self.color = color
		
		if color == "wh":	
			self.opp_color = "bl"
		else:
			self.opp_color = "wh"
		
		self.posit = posit # side of the board that this character is on, 1 = top, 2 = Bottom
		
		self.max_depth = 2
		
		self.takes = []
		self.moves = [] 
		
		
	# --------------------------------------------------------------------------------
	def ai_move(self, my_board, ra1, fi1, ra2, fi2):
		print("AI Moving Piece " + str(my_board.board[ra1][fi1]))
		
		piece = my_board.board[ra1][fi1]
		my_board.last_move = piece.move_str(ra2, fi2)
		self.animate(my_board, ra1, fi1, ra2, fi2)
		piece.rect = pygame.Rect(my_board.file_to_x(fi2), my_board.rank_to_y(ra2), my_board.space_height, my_board.space_height)
		my_board.board[piece.ra][piece.fi] = 0
			
		piece.ra = ra2
		piece.fi = fi2
			
		piece.hasMoved = True
		my_board.board[ra2][fi2] = piece
		
		my_board.plyr1.gen_moves(my_board)
		self.gen_moves(my_board)
		
		my_board.update_check(my_board.plyr1, self)
		
		print("white checked? " + str(my_board.wh_check))
		print("black checked? " + str(my_board.bl_check))
		
		if my_board.is_checkmate(my_board.plyr1):
			my_board.last_move = my_board.last_move + "#"
			return True
		
		if my_board.is_check(my_board.plyr1_color):
			my_board.last_move = my_board.last_move + "+"
		
	def ai_take(self, my_board, ra1, fi1, ra2, fi2):
		piece = my_board.board[ra1][fi1]
		piece2 = my_board.board[ra2][fi2]
		
		my_board.last_move = piece.take_to_str(ra2, fi2)
		piece2 = my_board.board[ra2][fi2]
		self.animate(my_board, ra1, fi1, ra2, fi2)
		piece2.kill()
		piece.rect = pygame.Rect(my_board.file_to_x(fi2), my_board.rank_to_y(ra2), my_board.space_height, my_board.space_height)
		piece.ra = ra2
		piece.fi = fi2
		my_board.board[ra2][fi2] = piece
		my_board.board[ra1][fi1] = 0
		my_board.plyr1.gen_moves(my_board)
		self.gen_moves(my_board)
		
		my_board.update_check(my_board.plyr1, self)
		print("white checked? " + str(my_board.wh_check))
		print("black checked? " + str(my_board.bl_check))
		
		if my_board.is_checkmate(my_board.plyr1):
			my_board.last_move = my_board.last_move + "#"
			return True
			
		if my_board.is_check(my_board.plyr1_color):
			my_board.last_move = my_board.last_move + "+"
	
		
	# --------------------------------------------------------------------------------
	def animate(self, my_board, ra1, fi1, ra2, fi2):
		time = 12
		
		piece1 = my_board.get_piece(ra1, fi1)
		
		x1 = my_board.file_to_x(fi1)
		y1 = my_board.rank_to_y(ra1)
		
		x2 = my_board.file_to_x(fi2)
		y2 = my_board.rank_to_y(ra2)
	
		delta_x = int((x2 - x1)/time) 
		delta_y = int((y2 - y1)/time)
		
		for i in range(0, time):
			x1 = x1 + delta_x
			y1 = y1 + delta_y
			piece1.rect = pygame.Rect(x1, y1, my_board.space_height, my_board.space_height)
			my_board.layers.move_to_front(piece1)
			my_board.update()
	
	
	# --------------------------------------------------------------------------------
	def check_promote(self, my_board, ra, fi):
		if self.posit == board.Board.BOT:
			end = 1
		else:
			end = 8
		if isinstance(my_board.get_piece(ra, fi), pieces.Pawn) and ra == end:
			self.promote_pawn(my_board, ra, fi)
			return True
			
	def promote_pawn(self, my_board, ra, fi):
		old_piece = my_board.get_piece(ra, fi)
		old_piece.kill()
		
		rook = "R"
		knight = "N"
		bishop = "B"
		queen = "Q"
		
		possible_pieces = [rook, knight, bishop, queen]
		
		random.seed()
		i = int(random.uniform(0, 3))
		
		my_board.make_piece(possible_pieces[i], ra, fi, self.color)
		
	# --------------------------------------------------------------------------------
	def gen_moves(self, my_board):
		# will predict moves for self
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
		# will predict moves opponent
		self.opp_moves = []
		self.opp_takes = []
		
		for ra in range(1, 9):
			for fi in range(1, 9):
				piece = my_board.get_piece(ra, fi)
				if piece and piece.color == self.opp_color:
					piece.gen_moves(my_board)
					
					for move in piece.moves:
						self.opp_moves.append((piece.ra, piece.fi, move[0], move[1]))
						
					for take in piece.takes:
						self.opp_takes.append((piece.ra, piece.fi, take[0], take[1]))
		
	# Filters player move list for moves that do not immediately check the player's king as a result
	def check_avoidance(self, my_board):
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
				
		
		#print("\n\nFinding possible takes...")
		for take in self.takes:
			#print("\nPossible Take: " + board.Board.file_[take[1]] + board.Board.rank_[take[0]] + " to " + board.Board.file_[take[3]] + board.Board.rank_[take[2]])
			temp_piece = virt_board.get_piece(take[2], take[3])
			taking_piece = virt_board.get_piece(take[0], take[1])
			
			virt_board.set_space(take[2], take[3], taking_piece)
			virt_board.set_space(take[0], take[1], 0)
			
			my_board.plyr1.gen_moves(my_board)
			virt_board.update_check(my_board.plyr1, self)
			
			#print(str(virt_board.takes))
			
			virt_board.set_space(take[0], take[1], taking_piece)
			virt_board.set_space(take[2], take[3], temp_piece)
			
			#print("Will take uncheck? " + str(not virt_board.is_check(self.color)))
			
			if not virt_board.is_check(self.color):
				checked_takes.append((take[0], take[1], take[2], take[3]))
			
		self.moves = checked_moves
		self.takes = checked_takes
		
	# filters through opp move list for valid moves that do not check
	def check_opp_avoidance(self, my_board):
		checked_moves = []
		checked_takes = []
		
		virt_board = board.Virtual_Board(my_board.plyr1_color)
		virt_board.board = copy.copy(my_board.board)
		
		for move in self.opp_moves:
			# create new board with same pieces as my_board
			temp_piece = virt_board.get_piece(move[2], move[3])
			moved_piece = virt_board.get_piece(move[0], move[1])
			
			virt_board.set_space(move[2], move[3], moved_piece)
			virt_board.set_space(move[0], move[1], 0)
			
			self.gen_moves(my_board)
			virt_board.update_check(my_board.plyr1, self)
			
			virt_board.set_space(move[0], move[1], moved_piece)
			virt_board.set_space(move[2], move[3], temp_piece)
			
			
			if not virt_board.is_check(my_board.plyr1_color):
				checked_moves.append((move[0], move[1], move[2], move[3]))
				
		
		#print("\n\nFinding possible takes...")
		for take in self.opp_takes:
			#print("\nPossible Take: " + board.Board.file_[take[1]] + board.Board.rank_[take[0]] + " to " + board.Board.file_[take[3]] + board.Board.rank_[take[2]])
			temp_piece = virt_board.get_piece(take[2], take[3])
			taking_piece = virt_board.get_piece(take[0], take[1])
			
			virt_board.set_space(take[2], take[3], taking_piece)
			virt_board.set_space(take[0], take[1], 0)
			
			self.gen_moves(my_board)
			virt_board.update_check(my_board.plyr1, self)
			
			#print(str(virt_board.takes))
			
			virt_board.set_space(take[0], take[1], taking_piece)
			virt_board.set_space(take[2], take[3], temp_piece)
			
			#print("Will take uncheck? " + str(not virt_board.is_check(self.color)))
			
			if not virt_board.is_check(my_board.plyr1_color):
				checked_takes.append((take[0], take[1], take[2], take[3]))
			
		self.opp_moves = checked_moves
		self.opp_takes = checked_takes	
		
	def decide(self, my_board):
		return True
		
	def calc_score(self, my_board):	
		return True
		# How the AI will score the state of the board at a given configuration
		# 500(K - K`) + 
		# 10(Q - Q`) +
		# 5(R - R`) +
		# 3(N - N` + B - B`) +
		# 1(P - P`) +
		# 0.5(M - M`) = score
					
	def move(self, my_board, color, my_game):
		self.gen_moves(my_board)
		self.check_avoidance(my_board)
		
		possible = self.moves + self.takes
		
		if len(possible) == 0 and my_board.is_check(self.color):
			print("Is AI checked? " + str(my_board.is_check(self.color)))
			my_board.checkmate = self.color
			return True
		elif len(possible) == 0:
			my_board.game_draw = True
			return True
		
		random.seed()
		i = int(random.uniform(0, len(possible) - 1))
		
		"""
		move = self.decide(my_board)
		
		if ((move[0], move[1], move[2], move[3]) in self.takes):
			self.ai_take(my_board, move[0], move[1], move[2], move[3])	
			self.check_promote(my_board, move[2], move[3])
			my_game.next_move(my_board)
		else: 
			self.ai_move(my_board, move[0], move[1], move[2], move[3])				
			self.check_promote(my_board, move[2], move[3])
			my_game.next_move(my_board)
	
		"""
		if ((possible[i][0], possible[i][1], possible[i][2], possible[i][3]) in self.takes):
			self.ai_take(my_board, possible[i][0], possible[i][1], possible[i][2], possible[i][3])	
			self.check_promote(my_board, possible[i][2], possible[i][3])
			my_game.next_move(my_board)
		else: 
			self.ai_move(my_board, possible[i][0], possible[i][1], possible[i][2], possible[i][3])				
			self.check_promote(my_board, possible[i][2], possible[i][3])
			my_game.next_move(my_board)
			
			
		#for move in possible:
			# another = self.imagine(this_move, depth + 1)
			# (value, another)
			# if value > best, best_move = another
		
		
		"""for move in self.moves:
			print("piece at: " + str(move[0]) + " " + str(move[1]) + " to " + str(move[2]) + " " + str(move[3]))
				
		for take in self.takes:
			print("piece at: " + str(take[0]) + " " + str(take[1]) + " takes " + str(take[2]) + " " + str(take[3]))"""
				#make move in new imagined board
					#move_value = value(this_move) + imagine(new_board with this move)
					#if value of move > best, best = move_value, best_move = move
					#imagine next moves in new board
	