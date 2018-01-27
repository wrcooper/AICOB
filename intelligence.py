import pygame, pieces, random, copy, board, sys, aicob, json, os, time, game
from pygame.locals import *



class Intelligence():
	def __init__(self, my_board, color, posit):
		self.my_board = my_board
		self.color = color
		
		if posit == board.Board.BOT:
			self.opp = my_board.plyr2
		else:
			self.opp = my_board.plyr1
		
		self.posit = posit # side of the board that this character is on, 1 = top, 2 = Bottom
		
		self.moves = []
		
		self.load_dict(game.DEFAULT_DEPTH)
		
	def print_moves(self):
		for move in self.moves:
			print(board.move_to_str(move))
			
	def indent_depth(self, depth):
		indents = self.depth - depth
		indent = ""
		for i in range(indents):
			indent += "|   "
		return indent
			
	def set_opp(self, opp):
		self.opp = opp
		
	def get_key_pressed(self, my_board):
		for event in pygame.event.get():
			if event.type == QUIT:
					sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					sys.exit()
				elif event.key == K_SPACE:
					self.my_board.game.paused = not self.my_board.game.paused
					my_board.interface.update_interface()
					my_board.update()
					pygame.event.clear()
					
	# --------------------------------------------------------------------------------
	# move a piece from a starting position and an ending position 
	def ai_move(self, my_board, ra1, fi1, ra2, fi2):
		#print("AI Moving Piece " + str(my_board.board[ra1][fi1]))
		
		# GET PIECE from starting position and APPEND PGN
		piece1 = my_board.get_piece(ra1, fi1)
		piece2 = my_board.get_piece(ra2, fi2)
		
		self.animate(my_board, ra1, fi1, ra2, fi2)
		if not piece1.move(my_board, ra2, fi2): return False
		
		my_board.layers.move_to_front(piece1)
		my_board.update()
		
		if piece2: piece2.kill()

		# GENERATE MOVES for both players based on new board condition
		self.opp.gen_moves(my_board)
		self.gen_moves(my_board)
		
		# UPDATE whether player is CHECKED
		my_board.update_check(self.opp, self)
		
		# if CHECKMATE, APPEND corresponding PGN
		if my_board.update_checkmate(self.opp):
			my_board.last_move = my_board.last_move + "#"
			return True
		
		# if CHECKED, APPEND corresponding PGN
		if my_board.is_check(self.opp.color):
			my_board.last_move = my_board.last_move + "+"
	# --------------------------------------------------------------------------------
	def load_dict(self, depth):
		file_str = "move_dicts/move_dict" + str(depth) + ".json"
	
		if not os.path.exists(file_str):
			dict_file = open(file_str, "w+")
		else: dict_file = open(file_str, "r")
		
		if os.stat(file_str).st_size != 0:
			move_dict = json.load(dict_file)
		else: move_dict = dict()
		dict_file.close()
		
		self.move_dict = move_dict
		
	def flip_move(self, move):
		transformed_move = list(map(lambda x: (-1 * x) + 9, move))
		return transformed_move
		
	def load_calculated_move(self):
		# must be adjusted for the side of the board this player is on
		board_str = self.my_board.gen_board_str(self.posit)
		if board_str not in self.move_dict:
			return False
		else:
			if self.wait != 0:
				wait = int(self.wait/0.1)
				for i in range(wait):
					self.get_click(self.my_board.interface, self.my_board.screen)
					time.sleep(0.1)
			best_move = self.move_dict[board_str]
		
		if self.posit == board.Board.TOP:
			return self.flip_move(best_move)
		
		return best_move
		
	def save_move(self, move):
		board_str = self.my_board.gen_board_str(self.posit)
		
		if self.posit == board.Board.TOP:
			saved_move = self.flip_move(move)
		else: saved_move = list(move)
		
		file_str = "move_dicts/move_dict" + str(self.depth) + ".json"
		
		if not os.path.exists(file_str):
			dict_file = open(file_str, "w+")
			dict_file.close()
			
		if os.stat(file_str).st_size == 0:
			with open(file_str, "rb+") as dict_file:
				string = "{\"" + board_str + "\": " + str(saved_move) + "}"
				binary = bytearray(string, "utf-8")
				dict_file.write(binary)
		else:
			with open(file_str, "rb+") as dict_file:
				string = ", \"" + board_str + "\": " + str(saved_move) + "}"
				binary = bytearray(string, "utf-8")
				dict_file.seek(-1, 2)
				dict_file.write(binary)
		
		self.move_dict[board_str] = saved_move
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
		
		virt_board = board.Virtual_Board()
		virt_board.copy_board(my_board)
		virt_board.set_players(my_board.plyr1, my_board.plyr2)
		
		for move in self.moves:
			#print("\nPossible Move: " + board.Board.file_[move[1]] + board.Board.rank_[move[0]] + " to " + board.Board.file_[move[3]] + board.Board.rank_[move[2]])
			# create new board with same pieces as my_board
			ra1 = move[0]
			fi1 = move[1]
			ra2 = move[2]
			fi2 = move[3]
			
			moved_piece = virt_board.get_piece(ra1, fi1)
			
			result = moved_piece.move(virt_board, ra2, fi2)
			
			self.opp.gen_moves(virt_board)
			virt_board.update_check(my_board.plyr1, my_board.plyr2)
			
			#print("Will take uncheck? " + str(not virt_board.is_check(self.color)))
			
			if not virt_board.is_check(self.color):
				checked_moves.append((move[0], move[1], move[2], move[3]))
				
			virt_board.undo_move()
		
		self.moves = checked_moves
	
		self.opp.gen_moves(virt_board)
		
	def get_click(self, interface, scrn):
		newRelease = False
		lastRelease = False
	
		# GET MOUSE RELEASES
		for mouseReleased in pygame.event.get(MOUSEBUTTONUP):
			lastRelease = mouseReleased
			newRelease = True
			
		if newRelease:
			result = interface.clicked(lastRelease)
			interface.update_interface()
			interface.draw(scrn)
			
			if result == "new_game":
				return "new_game"
		
		self.get_key_pressed(self.my_board)
		
	def update_depth(self, my_game):
		self.depth = my_game.depth
		self.load_dict(self.depth)
		
	def update_wait(self, my_game):
		self.wait = my_game.ai_wait
		
	# --------------------------------------------------------------------------------
	def decide(self, my_board):
		virt_board = board.Virtual_Board()
		virt_board.copy_board(my_board)
		virt_board.set_players(my_board.plyr1, my_board.plyr2)
		
		interface = my_board.interface
		scrn = my_board.screen
		
		self.best_move = [] 
		
		#print(self.color + " MOVING ! ------------------------------------------------------------------\n")
		decision = self.minimax(virt_board, self.depth, float('-inf'), float('inf'), True, interface, scrn)
		if decision == "new_game":
			return decision
		#print("Decision value is " + str(decision))
		
		virt_board.kill()
		return self.best_move
		
	# RETURNS OPTIMAL MOVE via classic naive minimax algorithm
	def minimax(self, my_board, depth, alpha, beta, my_turn, interface, scrn):
	
		if depth == 0:
			# GENERATE MOVES, RETURN SCORE of the current state of the BOARD
			#self.gen_moves(my_board)
			#self.check_avoidance(my_board)
			#print(self.indent_depth(depth) + "END REACHED ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
			result = self.score_board(my_board)
			#print(self.indent_depth(depth) + "value: " + str(result))
			return result
			
			
		if my_turn:
			# GENERATE MOVES based on current state of the BOARD
			self.gen_moves(my_board)
			self.check_avoidance(my_board)
			
			result = self.get_click(interface, scrn)
			if result == "new_game":
				return "new_game"
			
			best_value = float('-inf')
					
			# TRY EACH MOVE in a NEW BOARD
			for move in self.moves:
				#print(self.indent_depth(depth) + "MY MOVE: depth = " + str(depth) + "----------------------------------------------------------------------------------")
				
				ra1 = move[0]
				fi1 = move[1]
				ra2 = move[2]
				fi2 = move[3]
				
				moved_piece = my_board.get_piece(ra1, fi1)
				moved_piece.gen_moves(my_board)
				
				moved_piece.move(my_board, ra2, fi2)
				
				#print(self.indent_depth(depth) + str(moved_piece))
				#print(self.indent_depth(depth) + board.move_to_str(move))
				
				#my_board.print_board(self.indent_depth(depth))
				
				# make move for opponent
				result = self.minimax(my_board, depth-1, alpha, beta, False, interface, scrn)
				
				if result == "new_game":
					return "new_game"
				
				value = max(best_value, result)
				alpha = max(value, alpha)
				
				if value >= best_value: 
					if depth == self.depth: 
						if value > best_value:
							self.best_move = [move]
						#elif value == best_value: self.best_move.append(move)
					best_value = value
					
				my_board.undo_move()
				
				if beta <= alpha:
					break
					
			#print(self.indent_depth(depth) + "Best value for depth" + str(depth) + " = " + str(best_value))
			return best_value
			
		else: # opponent's turn
			self.opp.gen_moves(my_board)
			self.opp.check_avoidance(my_board)
			
			result = self.get_click(interface, scrn)
			if result == "new_game":
				return "new_game"
			
			# my_board.print_board()
			
			best_value = float('inf')
			
			for move in self.opp.moves:
				#print(self.indent_depth(depth) + "OPPONENT MOVE: depth = " + str(depth) + "|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
				
				
				ra1 = move[0]
				fi1 = move[1]
				ra2 = move[2]
				fi2 = move[3]
				
				moved_piece = my_board.get_piece(ra1, fi1)
				
				moved_piece.gen_moves(my_board)
				moved_piece.move(my_board, ra2, fi2)
				
				#print(self.indent_depth(depth) + str(moved_piece))
				#print(self.indent_depth(depth) + board.move_to_str(move))
				
				#my_board.print_board(self.indent_depth(depth))
				
				result = self.minimax(my_board, depth-1, alpha, beta, True, interface, scrn)
				
				if result == "new_game":
					return "new_game"
				
				value = min(best_value, result)
				beta = min(value, beta)
				
				if value < best_value: best_value = value
				
				my_board.undo_move()
				
				if beta <= alpha:
					break
				
			#print("Best value for depth" + str(depth) + " = " + str(best_value))
			return best_value
			
			
			
			
	# RETURNS a SCORE of the BOARD CONFIGURATION in favor of this player
	def score_board(self, my_board):
		# [Pawn, Rook, Knight, Bishop, King, Queen]
		opp_pieces = [0 for i in range(0, 6)]
		my_pieces = [0 for i in range(0, 6)]
	
		for ra in range(1, 9):
			for fi in range(1, 9):
				piece = my_board.get_piece(ra, fi)
				if piece == 0: continue
				if my_board.check_player(self.opp, piece):	
					opp_pieces[piece.index] += 1
				else: my_pieces[piece.index] += 1
		
		score = 5000 * (my_pieces[pieces.Piece.KING] - opp_pieces[pieces.Piece.KING])
		score += 200 * (my_pieces[pieces.Piece.QUEN] - opp_pieces[pieces.Piece.QUEN])
		score += 50 * (my_pieces[pieces.Piece.ROOK] - opp_pieces[pieces.Piece.ROOK])
		score += 30 * (my_pieces[pieces.Piece.KNGH] - opp_pieces[pieces.Piece.KNGH])
		score += 30 * (my_pieces[pieces.Piece.BSHP] - opp_pieces[pieces.Piece.BSHP])
		score += 10 * (my_pieces[pieces.Piece.PAWN] - opp_pieces[pieces.Piece.PAWN])
		score += 1 * (len(self.moves) - len(self.opp.moves))
		
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
		#print("Is AI checked? " + str(my_board.is_check(self.color)))
		self.update_depth(my_game)
		self.update_wait(my_game)
			
		result = self.get_click(my_board.interface, my_board.screen)
		if result == "new_game":
			return "new_game"
	
		# UPDATE CHECKMATE and DRAW
		my_board.update_check(my_board.plyr1, my_board.plyr2)
		if my_board.update_checkmate(self):
			return False
		
		# PICK an OPTIMAL MOVE
		precalc = self.load_calculated_move()
		
		if precalc == False:
			moves = self.decide(my_board)
		else: moves = [precalc]
		#print(self.color + "'s best moves: " + str(moves))
		
		if moves == "new_game":
			return False
		
		# PICK a RANDOM MOVE, if choosing randomly
		random.seed()
		i = int(random.uniform(0, len(moves) - 1))
		
		move = moves[i]
		
		self.save_move(move)
		
		self.gen_moves(my_board)
		self.check_avoidance(my_board)
		
		self.ai_move(my_board, move[0], move[1], move[2], move[3])				
		self.check_promote(my_board, move[2], move[3])
		my_game.next_move()