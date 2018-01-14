import pygame, pieces, random, copy, board, sys

class Intelligence():
	def __init__(self, my_board, color, posit):
		self.board = my_board
		self.color = color
		
		if color == "wh":	
			self.opp_color = "bl"
		else:
			self.opp_color = "wh"
		
		self.posit = posit # side of the board that this character is on, 1 = top, 2 = Bottom
		
		self.takes = []
		
	def print_takes(self):
		for take in self.takes:
			print(board.move_to_str(take))
		
		
	# --------------------------------------------------------------------------------
	# move a piece from a starting position and an ending position 
	def ai_move(self, my_board, ra1, fi1, ra2, fi2):
		#print("AI Moving Piece " + str(my_board.board[ra1][fi1]))
		
		# GET PIECE from starting position and APPEND PGN
		piece1 = my_board.get_piece(ra1, fi1)
		piece2 = my_board.get_piece(ra2, fi2)
		
		self.animate(my_board, ra1, fi1, ra2, fi2)
		if not piece1.move(my_board, ra2, fi2): return False
		
		if piece2: piece2.kill()

		# GENERATE MOVES for both players based on new board condition
		my_board.plyr1.gen_moves(my_board)
		self.gen_moves(my_board)
		
		# UPDATE whether player is CHECKED
		my_board.update_check(my_board.plyr1, self)
		
		#print("white checked? " + str(my_board.wh_check))
		#print("black checked? " + str(my_board.bl_check))
		
		# if CHECKMATE, APPEND corresponding PGN
		if my_board.update_checkmate(my_board.plyr1):
			my_board.last_move = my_board.last_move + "#"
			return True
		
		# if CHECKED, APPEND corresponding PGN
		if my_board.is_check(my_board.plyr1_color):
			my_board.last_move = my_board.last_move + "+"
		
	# --------------------------------------------------------------------------------
	# ANIMATE using simple distance/time velocity formula
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
	# PROMOTE pawn if at end of corresponding end of the board
	def check_promote(self, my_board, ra, fi):
		if self.posit == board.Board.BOT:
			end = 1
		else:
			end = 8
		if isinstance(my_board.get_piece(ra, fi), pieces.Pawn) and ra == end:
			self.promote_pawn(my_board, ra, fi)
			return True
			
	def promote_pawn(self, my_board, ra, fi):
		# KILL old piece SPRITE
		old_piece = my_board.get_piece(ra, fi)
		old_piece.kill()
		
		rook = "R"
		knight = "N"
		bishop = "B"
		queen = "Q"
		
		possible_pieces = [rook, knight, bishop, queen]
		
		# ai currently always picks queen
		# TODO: pick the optimal piece for the situation, will be queen for most
		i = 3
		
		my_board.make_piece(possible_pieces[i], ra, fi, self.color)
		
	# --------------------------------------------------------------------------------
	# GENERATE MOVES based on current board configuration
	# TODO: add a boolean flag for whether check should be avoided in generated moves
	def gen_moves(self, my_board):
		# will predict moves for self
		self.moves = []
		
		for ra in range(1, 9):
			for fi in range(1, 9):
				piece = my_board.get_piece(ra, fi)
				if piece and piece.color == self.color:
					piece.gen_moves(my_board)
					
					for move in piece.moves:
						self.moves.append((piece.ra, piece.fi, move[0], move[1]))
		
	# Filters player move list for moves that do not immediately check the player's king as a result
	
	def check_avoidance(self, my_board):
		checked_moves = []
		
		virt_board = board.Virtual_Board(my_board.plyr1_color)
		virt_board.copy_board(my_board)
		virt_board.set_players(my_board.plyr1, self)
		
		self.gen_moves(virt_board)
		
		for move in self.moves:
			#print("\nPossible Move: " + board.Board.file_[move[1]] + board.Board.rank_[move[0]] + " to " + board.Board.file_[move[3]] + board.Board.rank_[move[2]])
			# create new board with same pieces as my_board
			ra1 = move[0]
			fi1 = move[1]
			ra2 = move[2]
			fi2 = move[3]
			
			moved_piece = virt_board.get_piece(ra1, fi1)
			
			result = moved_piece.move(virt_board, ra2, fi2)
			
			my_board.plyr1.gen_moves(virt_board)
			virt_board.update_check(my_board.plyr1, my_board.plyr2)
			
			#print("Will take uncheck? " + str(not virt_board.is_check(self.color)))
			
			if not virt_board.is_check(self.color):
				checked_moves.append((move[0], move[1], move[2], move[3]))
				
			virt_board.undo_move()
		
		self.moves = checked_moves
	
		my_board.plyr1.gen_moves(virt_board)
	
	def update_depth(self, my_game):
		self.depth = my_game.depth
		
	# --------------------------------------------------------------------------------
	def decide(self, my_board):
		virt_board = board.Virtual_Board(my_board.plyr1_color)
		virt_board.copy_board(my_board)
		virt_board.set_players(my_board.plyr1, self)
		
		decision = self.minimax(virt_board, self.depth, float('-inf'), float('inf'), True)
		# print("Decision value is " + str(decision))
		virt_board.kill()
		return self.best_move
		
	# RETURNS OPTIMAL MOVE via classic naive minimax algorithm
	def minimax(self, my_board, depth, alpha, beta, my_turn):
	
		if depth == 0:
			# GENERATE MOVES, RETURN SCORE of the current state of the BOARD
			#self.gen_moves(my_board)
			#self.check_avoidance(my_board)
			# print("END REACHED ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
			return self.score_board(my_board)
			
			
		if my_turn:
			# GENERATE MOVES based on current state of the BOARD
			self.gen_moves(my_board)
			self.check_avoidance(my_board)
			
			best_value = float('-inf')
					
			# TRY EACH MOVE in a NEW BOARD
			for move in self.moves:
				# print("MY MOVE: depth = " + str(depth) + "----------------------------------------------------------------------------------")
				
				ra1 = move[0]
				fi1 = move[1]
				ra2 = move[2]
				fi2 = move[3]
				
				moved_piece = my_board.get_piece(ra1, fi1)
				
				moved_piece.gen_moves(my_board)
				
				result = moved_piece.move(my_board, ra2, fi2)
				
				# make move for opponent
				value = max(best_value, self.minimax(my_board, depth-1, alpha, beta, False))
				
				alpha = max(value, alpha)
				
				if value > best_value: 
					best_value = value
					if depth == self.depth: self.best_move = move
					
				my_board.undo_move()
				
				if beta <= alpha:
					break
					
			# print("Best value for depth" + str(depth) + " = " + str(best_value))
			return best_value
			
		else: # opponent's turn
			my_board.plyr1.gen_moves(my_board)
			my_board.plyr1.check_avoidance(my_board)
			
			# my_board.print_board()
			
			best_value = float('inf')
			
			for move in my_board.plyr1.moves:
				# print("PLAYER MOVE: depth = " + str(depth) + "|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
				
				ra1 = move[0]
				fi1 = move[1]
				ra2 = move[2]
				fi2 = move[3]
				
				moved_piece = my_board.get_piece(ra1, fi1)
				
				moved_piece.gen_moves(my_board)
				
				result = moved_piece.move(my_board, ra2, fi2)
				
				value = min(best_value, self.minimax(my_board, depth-1, alpha, beta, True))
				
				beta = min(value, beta)
				
				if value < best_value: best_value = value
				
				my_board.undo_move()
				
				if beta <= alpha:
					break
				
				
			# print("Best value for depth" + str(depth) + " = " + str(best_value))
			return best_value
			
			
			
			
	# RETURNS a SCORE of the BOARD CONFIGURATION in favor of this player
	def score_board(self, my_board):
		# [Pawn, Rook, Knight, Bishop, King, Queen]
		plyr_pieces = [0 for i in range(0, 6)]
		my_pieces = [0 for i in range(0, 6)]
	
		for ra in range(1, 9):
			for fi in range(1, 9):
				piece = my_board.get_piece(ra, fi)
				if piece == 0: continue
				if my_board.check_player(piece):	
					plyr_pieces[piece.index] += 1
				else: my_pieces[piece.index] += 1
		
		score = 5000 * (my_pieces[pieces.Piece.KING] - plyr_pieces[pieces.Piece.KING])
		score += 100 * (my_pieces[pieces.Piece.QUEN] - plyr_pieces[pieces.Piece.QUEN])
		score += 50 * (my_pieces[pieces.Piece.ROOK] - plyr_pieces[pieces.Piece.ROOK])
		score += 30 * (my_pieces[pieces.Piece.KNGH] - plyr_pieces[pieces.Piece.KNGH])
		score += 30 * (my_pieces[pieces.Piece.BSHP] - plyr_pieces[pieces.Piece.BSHP])
		score += 10 * (my_pieces[pieces.Piece.PAWN] - plyr_pieces[pieces.Piece.PAWN])
		score += 0.8 * (len(self.moves) - len(my_board.plyr1.moves))
		
		return score
					
		# How the AI will score the state of the board at a given configuration
		# 500(K - K`) + 
		# 10(Q - Q`) +
		# 5(R - R`) +
		# 3(N - N` + B - B`) +
		# 1(P - P`) +
		# 0.5(M - M`) = score
					
	# --------------------------------------------------------------------------------
	# CHOOSE an OPTIMAL MOVE and MAKE IT
	def move(self, my_board, my_game):
		print("Is AI checked? " + str(my_board.is_check(self.color)))
		self.update_depth(my_game)
	
		# UPDATE CHECKMATE and DRAW
		my_board.update_check(my_board.plyr1, self)
		my_board.update_checkmate(self)
		
		possible = self.moves
		
		if len(possible) == 0 and my_board.is_check(self.color):
			my_board.checkmate = self.color
			return True
		elif len(possible) == 0:
			my_board.game_draw = True
			return True
		
		# PICK a RANDOM MOVE, if choosing randomly
		random.seed()
		i = int(random.uniform(0, len(possible) - 1))
		
		# PICK an OPTIMAL MOVE
		move = self.decide(my_board)
		
		self.gen_moves(my_board)
		self.check_avoidance(my_board)
		
		print("Current board before moving: ")
		my_board.print_board()
		
		print("AI moving")
		print(board.move_to_str(move))
		self.ai_move(my_board, move[0], move[1], move[2], move[3])				
		self.check_promote(my_board, move[2], move[3])
		my_game.next_move()
	
		"""
		print(self.score_board(my_board))
		
		self.ai_move(my_board, possible[i][0], possible[i][1], possible[i][2], possible[i][3])				
		self.check_promote(my_board, possible[i][2], possible[i][3])
		my_game.next_move()	
		"""	
	
		
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
	