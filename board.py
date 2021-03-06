import pygame, math, inspect, aicob, game, pieces, time
from pygame.locals import *

class Board():
	TOP = 1
	BOT = 2
	
	file_ = ['', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
	rank_ = ['', '8', '7', '6', '5', '4', '3', '2', '1']

	# --------------------------------------------------------------------------------
	def __init__(self, scrn_info, plyr1_color, screen):
		self.screen = screen
		self.scrn_info = scrn_info
		self.clock = pygame.time.Clock()
		
		scrn_h = scrn_info.current_h
		scrn_w = scrn_info.current_w
		margin = (scrn_w - scrn_h)/2 
		
		self.height = scrn_h
		self.width = scrn_w
		
		self.space_height = scrn_h/8
		self.edge_dist = margin/10 # this is the distance from the edge of the board to the edge of the screen
		
		self.rect = pygame.Rect(margin, 0, scrn_h, scrn_h)
		
		self.board = [[0 for x in range(9)] for y in range(9)]
		self.last_move = None
		self.turn = 0
		
		self.wh_check = False
		self.bl_check = False
		
		self.checkmate = False
		self.game_draw = False
		self.pawn_promotion = False
		
		self.make_hist()
		
	def gen_board_str(self, position):
		board_str = ""
		
		# string must be adjusted depending on which side of the board the player is on
		if position == Board.TOP:
			for ra in range(8, 0, -1):
				for fi in range(8, 0, -1):
					piece = self.get_piece(ra, fi)
					if isinstance(piece, pieces.Pawn): board_str += "P"
					elif piece != 0: board_str += piece.shorthand
					else: board_str += "x" 
		else:
			for ra in range(1, 9):
				for fi in range(1, 9):
					piece = self.get_piece(ra, fi)
					if isinstance(piece, pieces.Pawn): board_str += "P"
					elif piece != 0: board_str += piece.shorthand
					else: board_str += "x" 
		
		return board_str
		
	def set_game(self, my_game):
		self.game = my_game
		
	def set_players(self, plyr1, plyr2):
		self.plyr1 = plyr1
		self.plyr2 = plyr2
		
	# PRINT STATE OF BOARD for DEBUGGING
	def print_board(self, indent):
		for ra in range(1, 9):
			print(indent, end='')
			for fi in range(1, 9):
				piece = self.get_piece(ra, fi)
				if isinstance(piece, pieces.Pawn): print("P", end='')
				elif piece != 0: print(piece.shorthand, end='')
				else: print("x", end = '')
			print("")
			
	def print_moves(self):
		for ra in range(9):
			for fi in range(9):
				piece = self.get_piece(ra, fi)
				if piece != 0:
					print(piece.color + " " + str(piece) + " at " + space_to_str(ra, fi) + ":")
					print("moves: " + str(piece.moves) + "\n")
		
	# --------------------------------------------------------------------------------
	# DRAW BOARD BACKGROUND
	def draw_bg(self, screen):
		colors = [(249, 190, 102), (56,23,19)]
		current = 0
		space_height = self.space_height
		for i in range(9):
			for j in range(9):
				if current > 1:
					current = 0
				x_distance = space_height * i
				y_distance = space_height * j
				screen.fill(colors[current], pygame.Rect(x_distance,y_distance,space_height,space_height))
				current += 1
	
	# INIT BACKGROUND SURFACE
	def bg_init(self, wood):
		background = pygame.Surface((self.height, self.height))
		wood.set_alpha(150)
		bgwood = pygame.transform.scale(wood, (self.height, self.height))
		self.draw_bg(background)
		
		background.blit(bgwood, (0,0))
		self.screen.blit(background, (self.edge_dist, 0))
		
		background = self.screen.copy()
		self.set_background(background)
	
	# SET GROUPS for DRAWING
	def set_groups(self, highlight, highlight_current, all, ui):
		self.groups = (highlight, highlight_current, all, ui)
		self.layers = all
		
	def print_groups(self):
		for group in self.groups:
			print(group.sprites())
	
	# CLEAR AND DRAW to SCREEN
	def update(self):
		for group in self.groups:
			group.clear(self.screen, self.background)
		for group in self.groups:
			group.draw(self.screen)
			
		pygame.display.update()
	# --------------------------------------------------------------------------------
	def set_background(self, background):
		self.background = background

	# SET UI
	def set_interface(self, interface, group):
		self.interface = interface
		self.interface_group = group
	# --------------------------------------------------------------------------------
	# RETURN if MOUSE WITHIN BOARD
	def within(self, mouse):
		return (mouse.pos[0] > self.edge_dist and mouse.pos[0] < self.edge_dist + self.height)

	# --------------------------------------------------------------------------------
	# CONVERT (ra, fi) coordinates to (x, y) pixel coordinates
	def space_to_rect(self, ra, fi):
		y = (ra - 1) * self.space_height
		x = (fi-1) * self.space_height + self.edge_dist
		
		return pygame.Rect(x, y, self.space_height, self.space_height)
	
	# --------------------------------------------------------------------------------
	# CONVERT (x, y) pixel coordinates) to (ra, fi) coordinates
	def coord_to_space(self, x, y):
		ra = math.ceil(y/self.space_height)
		fi = math.ceil((x - self.edge_dist)/self.space_height)
		return (ra, fi)
	
	# --------------------------------------------------------------------------------
	# CONVERSIONS
	def rank_to_y(self, ra):
		y = (ra - 1) * self.space_height
		return y
	
	def file_to_x(self, fi):
		x = (fi-1) * self.space_height + self.edge_dist
		return x

	def y_to_rank(self, y):
		rank = math.ceil(y/self.space_height)
		return rank
	
	def x_to_file(self, x):
		fi = math.ceil((x - self.edge_dist)/self.space_height)
		return fi
	
	# --------------------------------------------------------------------------------
	# INITIAL STATE of BOARD
	def init_pieces(self, color1):
		for ra in range(9):
			for fi in range(9):
				piece = self.get_piece(ra, fi)
				if piece != 0:
					piece.kill()
					
		self.board = [[0 for x in range(9)] for y in range(9)]
		
		if color1 == "wh":
			color2 = "bl"
		else:
			color2 = "wh"
			
		init_layout = [
		["R", "N", "B", "K", "Q", "B", "N", "R"],
		["",  "",  "",  "",  "",  "",  "",  ""],
		[0,   0,   0,   0,   0,   0,   0,   0],
		[0,   0,   0,   0,   0,   0,   0,   0],
		[0,   0,   0,   0,   0,   0,   0,   0],
		[0,   0,   0,   0,   0,   0,   0,   0],
		["",  "",  "",  "",  "",  "",  "",  ""],
		["R", "N", "B", "K", "Q", "B", "N", "R"]
		]
		
		for col in range(1, 9):
			for row in range(1, 3):
				self.make_piece(init_layout[row-1][col-1], row, col, color2)
			for row in range(7, 9):
				self.make_piece(init_layout[row-1][col-1], row, col, color1)
				
	# --------------------------------------------------------------------------------
	# INITIALIZE any PIECE
	def make_piece(self, piece, ra, fi, color):
		x = self.file_to_x(fi)
		y = self.rank_to_y(ra)
		
		if piece == "":
			piece = pieces.Pawn(ra, fi, color)
			
		elif piece == "R":
			piece = pieces.Rook(ra, fi, color)
			
		elif piece == "N":
			piece = pieces.Knight(ra, fi, color)
			
		elif piece == "B":
			piece = pieces.Bishop(ra, fi, color)
			
		elif piece == "K":
			piece = pieces.King(ra, fi, color)
			
		elif piece == "Q":
			piece = pieces.Queen(ra, fi, color)
			
		elif piece == 0:
			return
			
		piece.set_rect(x, y, self.space_height)
		piece.set_image(self.space_height)
		self.board[ra][fi] = piece
		
	# --------------------------------------------------------------------------------
	# RETURN piece if there is a piece, false if not
	def get_piece(self, ra, fi):
		piece = self.board[ra][fi]
		if piece != 0:
			return piece
		else:
			return False
	# --------------------------------------------------------------------------------
	# SET a BOARD SPACE to a PIECE
	def set_space(self, ra, fi, piece):
		self.board[ra][fi] = piece
		return True
	
	# --------------------------------------------------------------------------------
	# RETURN whether a SPACE HAS a PIECE
	def has_piece(self, ra, fi):
		if self.board[ra][fi] == 0:
			return False
		else:
			return True
			
	def is_empty(self, ra, fi):
		return not self.has_piece(ra, fi)
		
	# --------------------------------------------------------------------------------
	# RETURN COLOR of a PIECE given it's SPACE
	def get_piece_color(self, ra, fi):
		piece = self.get_piece(ra, fi)
		if piece:
			return piece.color
		else:
			return False

	# --------------------------------------------------------------------------------
	# UPDATES CHECKMATE variable, DRAW if drawn, returns TRUE if checkmate or draw, FALSE if neither
	def update_checkmate(self, plyr):
		plyr.gen_moves(self)
		plyr.check_avoidance(self)
		
		if len(plyr.moves) == 0 and self.is_check(plyr.color):
			self.checkmate = plyr.color
			return True
			
		elif len(plyr.moves) == 0:
			self.checkmate = "dr"
			self.game_draw = True
			return True
		else:
			return False
	
	# RETURNS the check flag of a certain player color
	def is_check(self, color):
		if color == "wh":
			return self.wh_check
		else: 
			return self.bl_check
		
	# SETS the CHECK FLAG for a color if the position of that PLAYER'S KING is in the TAKES OF THEIR OPPONENT
	def update_check(self, plyr, opp):
		for ra in range(1, 9):
			for fi in range(1, 9):
				if isinstance(self.board[ra][fi], pieces.King):
					king = self.board[ra][fi]
					color = king.color
					
					if self.plyr1.color == "wh":
						white = plyr
						black = opp
					else: 
						black = plyr
						white = opp
					
					if color == "wh":
						for move in black.moves:	
							if (ra, fi) == move[2:4]:
								self.wh_check = True
								return True
						
						self.wh_check = False
								
					else:
						for move in white.moves:	
							if (ra, fi) == move[2:4]:
								self.bl_check = True
								return True
						self.bl_check = False

	# --------------------------------------------------------------------------------					
	# checks if piece is same color as plyr1_color
	def check_player(self, plyr, piece):
		if plyr.color == piece.color:
			return True
		else: return False
	
		
	# --------------------------------------------------------------------------------
	# compares color of two pieces
	def check_color(self, piece1, piece2):
			if piece1 != 0 and piece2 != 0 and piece1.color != piece2.color:
					return True
			else:
					return False
					
	# --------------------------------------------------------------------------------
	def make_hist(self):
		self.hist = []
		# each piece move will append to history in the form of:
		# [piece taken, [ra1.1, fi1.1, ra1.2, fi1.2], ([ra2.1, fi2.1, ra2.2, fi2.2], ... )]
		# for all pieces moved as a result of that move
		
	def pop_hist(self):
		end = len(self.hist) - 1
		result = self.hist[end]
		del self.hist[-1]
		
		return result
		
	def undo_move(self):
		last_move = self.pop_hist()
		
		length = len(last_move) - 1
		for i in range(length, 0, -1):
			move = last_move[i]
			has_moved, en_passant_able = move[4], move[5]
			ra1, fi1, ra2, fi2 = move[0], move[1], move[2], move[3]
			piece = self.get_piece(ra2, fi2)
			
			if piece == False:	
				print(space_to_str(ra2, fi2))
			
			piece.has_moved = has_moved
			piece.en_passant_able = en_passant_able
			
			piece.ra = ra1
			piece.fi = fi1
			
			self.set_space(ra1, fi1, piece)
			self.set_space(ra2, fi2, 0)
			
		taken_piece = last_move[0]
		if taken_piece != 0:
			self.set_space(taken_piece.ra, taken_piece.fi, taken_piece)
		else: self.set_space(ra2, fi2, taken_piece)
			
		
	# --------------------------------------------------------------------------------				
	# checks if move is a valid move
	def valid_move(self, ra1, fi1, ra2, fi2):
		piece = self.board[ra1][fi1]
		
		if ((ra1, fi1, ra2, fi2) in self.moves):
			return piece.valid_move(self, ra2, fi2)

	def in_moves(self, ra1, fi1, ra2, fi2):
		return ((ra1, fi1, ra2, fi2) in self.moves)
	# --------------------------------------------------------------------------------	
	def gen_plyr1_moves(self):
		self.plyr1.gen_moves(self)
		self.plyr1.check_avoidance(self)
	
	def gen_plyr2_moves(self):
		self.plyr2.gen_moves(self)
		self.plyr2.check_avoidance(self)
		
	# --------------------------------------------------------------------------------	
	# UPDATES the VISUAL POSITION of the PIECE if the piece is HELD
	def piece_held(self, my_game, ra, fi, group):
		piece = self.get_piece(ra, fi)
			
		if not piece or not valid_space(ra, fi) or piece.color != my_game.current_move or not self.check_player(self.plyr1, piece): 
			return False

		# update piece location to follow mouse
		group.move_to_front(piece)
		piece.rect = pygame.Rect( pygame.mouse.get_pos()[0] - (self.space_height / 2), 
		pygame.mouse.get_pos()[1] - (self.space_height / 2), self.space_height, self.space_height)
		
		# draw highlighted spaces
		self.next_highlight = self.highlight(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], piece)
		self.current_highlight = self.highlight_current(ra, fi)

	def piece_released(self, my_game, plyr, opp, ra1, fi1, ra2, fi2):
		piece = self.get_piece(ra1, fi1)
		#self.print_moves()
		
		# checking valid move
		if piece == 0 or piece.color != plyr.color or piece.color != my_game.current_move:
			return False
			
		# move piece
		if plyr.move_piece(self, ra1, fi1, ra2, fi2):
			if ra2 == 1 and isinstance(self.get_piece(ra2, fi2), pieces.Pawn):
				self.promote_pawn(ra2, fi2)
		
			self.update_check(plyr, opp)
			
			if self.update_checkmate(self.plyr2):
				self.last_move = self.last_move + "#"
				my_game.next_move()
				return True
			
			if self.is_check(opp.color):
				self.last_move = self.last_move + "+"
				
			self.gen_plyr1_moves()
			self.gen_plyr2_moves()
			
			my_game.next_move()
				
		else:
			self.piece_reset(ra1, fi1)
		if not self.next_highlight == False:
			self.next_highlight.kill()
		self.current_highlight.kill()

	def piece_reset(self, ra, fi):
		if ra < 1 or ra > 8 or fi < 1 or fi > 8:
			return False
		piece = self.board[ra][fi]
		if piece == 0:
			return False
		piece.rect = pygame.Rect(self.file_to_x(fi), self.rank_to_y(ra), self.space_height, self.space_height)
		return False
		

	# --------------------------------------------------------------------------------
	def highlight(self, x, y, piece):
		space = self.coord_to_space(x, y)
		ra = space[0]
		fi = space[1]
		
		if not valid_space(ra, fi):
			return False
		
		if ((ra, fi) in piece.moves and (piece.ra, piece.fi, ra, fi) in self.plyr1.moves) or (ra, fi) == (piece.ra, piece.fi) :
			highlight = Highlight(ra, fi, self, True)
			return highlight

		highlight = Highlight(ra, fi, self, False)
		return highlight
	
	def highlight_current(self, ra, fi):
		highlight = Highlight_Current(ra, fi, self)
		return highlight
					
	# --------------------------------------------------------------------------------
	# PROMOTE PAWN at a given SPACE
	def promote_pawn(self, ra, fi):
		old_piece = self.get_piece(ra, fi)
		old_piece.kill()
		self.open_pawn_promotion(ra, fi)
	
	# OPEN PAWN PROMOTION INTERFACE
	def open_pawn_promotion(self, ra, fi):
		self.interface.open_pawn_promotion(self.plyr1.color, self)
		self.interface_group.draw(self.screen)
		pygame.display.update()
		
		pawn_promoted = False
		newRelease = False
		lastRelease = False
		print("Before While")
		pygame.event.clear(MOUSEBUTTONUP)
		
		while not pawn_promoted:
			self.clock.tick(40)
			print("While")
		
			if pygame.event.peek(MOUSEBUTTONUP):
				for mouse_release in pygame.event.get(MOUSEBUTTONUP):
					lastRelease = mouse_release
				newRelease = True
				print(lastRelease.pos[0], lastRelease.pos[1])
				
			print("Promotion selected? " + str(self.interface.pawn_prom.clicked(lastRelease)))
			
			if newRelease and self.interface.pawn_prom.clicked(lastRelease):
				piece = self.interface.select_promotion(lastRelease)
				print(str(piece))
				print("Here")
				
				if piece != False:
					self.make_piece(piece, ra, fi, self.plyr1.color)
					pawn_promoted = True
					
			newRelease = False

	def open_end_game(self, color):
		self.interface.open_end_game()
		self.interface.game_end = True
		self.interface.end_game.animate(self, self.screen, color)
				
# COLOR KEY FOR LOADING PIECE IMAGES		
def colorKey(color, n):
	if (color == "bl"):
		return n + 6
	else:
		return n
	
def space_to_str(ra, fi):
	return (str(Board.file_[fi]) + str(Board.rank_[ra]))
	
def move_to_str(move):
	return space_to_str(move[0], move[1]) + " to: " + space_to_str(move[2], move[3])
					
def valid_space(ra, fi):
	return ra > 0 and ra < 9 and fi > 0 and fi < 9
		
class Virtual_Board(Board):
	def __init__(self):
		self.board = [[0 for x in range(9)] for y in range(9)]
		self.space_height = 0
		self.edge_dist = 0
		
		self.make_hist()
		
	def make_piece(self, piece, ra, fi):
		shorthand = piece.shorthand
		color = piece.color
		if shorthand == "":
			new_piece = pieces.Pawn(ra, fi, color)
		elif shorthand == "R":
			new_piece = pieces.Rook(ra, fi, color)
		elif shorthand == "N":
			new_piece = pieces.Knight(ra, fi, color)
		elif shorthand == "B":
			new_piece = pieces.Bishop(ra, fi, color)
		elif shorthand == "K":
			new_piece = pieces.King(ra, fi, color)
		elif shorthand == "Q":
			new_piece = pieces.Queen(ra, fi, color)
			
		new_piece.kill()
		new_piece.moves = list(piece.moves)
		new_piece.has_moved = piece.has_moved
		new_piece.en_passant_able = piece.en_passant_able
		self.board[ra][fi] = new_piece
		
	def copy_board(self, my_board):
		self.wh_check = my_board.wh_check
		self.bl_check = my_board.bl_check
	
		for ra in range(1, 9):
			for fi in range(1, 9):
				piece = my_board.get_piece(ra, fi)
				if piece:
					self.make_piece(piece, ra, fi)
				else:
					self.set_space(ra, fi, 0)
					
	def kill(self):
		for ra in range(1, 9):
			for fi in range(1, 9):
				piece = self.get_piece(ra, fi)
				if piece:
					piece.kill()
		
# SPRITE CLASSES FOR HIGHLIGHTING SPACES
class Highlight(pygame.sprite.Sprite):
	def __init__(self, ra, fi, board, valid):
		pygame.sprite.Sprite.__init__(self, self.containers)
		rect = board.space_to_rect(ra, fi)
		self.rect = rect
		s = pygame.Surface((rect.width, rect.height))
		s.set_alpha(100)
		if valid: s.fill((255, 180, 60))
		else: s.fill((255, 60, 10))
		self.image = s
	
class Highlight_Current(pygame.sprite.Sprite):
	def __init__(self, ra, fi, board):
		pygame.sprite.Sprite.__init__(self, self.containers)
		rect = board.space_to_rect(ra, fi)
		self.rect = rect
		s = pygame.Surface((self.rect.width, self.rect.height))
		s.set_alpha(100)
		s.fill((255, 160, 40))
		self.image = s

