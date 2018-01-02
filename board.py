import pygame, math, inspect, chess, game, pieces, time
from pygame.locals import *



class Board():
	TOP = 1
	BOT = 2
	
	file_ = ['', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
	rank_ = ['', '8', '7', '6', '5', '4', '3', '2', '1']

	# --------------------------------------------------------------------------------
	def __init__(self, height, edge_dist, plyr1_color, screen):
		self.screen = screen
		self.clock = pygame.time.Clock()
		
		if plyr1_color == "wh":
			plyr2_color = "bl"
		else: plyr2_color = "wh"
		
		self.plyr1_color = plyr1_color
		self.plyr2_color = plyr2_color
		
		self.height = height
		self.space_height = height/8
		self.edge_dist = edge_dist
		
		self.rect = pygame.Rect(edge_dist, 0, height, height)
		self.board = [[0 for x in range(9)] for y in range(9)]
		
		self.last_move = None
		self.turn = 0
		
		self.wh_check = False
		self.bl_check = False
		
		self.checkmate = False
		self.game_draw = False
		self.pawn_promotion = False
		
	def set_players(self, plyr1, plyr2):
		self.plyr1 = plyr1
		self.plyr2 = plyr2
		
	# PRINT STATE OF BOARD for DEBUGGING
	def print_board(self):
		for ra in range(1, 9):
			for fi in range(1, 9):
				piece = self.get_piece(ra, fi)
				if isinstance(piece, pieces.Pawn): print("P", end='')
				elif piece != 0: print(piece.shorthand, end='')
				else: print("x", end = '')
			print("")
		
	# --------------------------------------------------------------------------------
	def draw(self, screen):
		colors = [(56,23,19), (249, 190, 102)]
		current = 0
		space_height = self.space_height
		for i in range(9):
			for j in range(9):
				if current == 2:
					current = 0
				x_distance = space_height * i
				y_distance = space_height * j
				screen.fill(colors[current], pygame.Rect(x_distance,y_distance,space_height,space_height))
				current += 1
	
	# SET GROUPS for DRAWING
	def set_groups(self, highlight, highlight_current, ui, all):
		self.groups = (highlight, highlight_current, ui, all)
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
		if color1 == "wh":
			color2 = "bl"
		else:
			color2 = "wh"
		
		order = [color1, color2]
		row2 = [7, 2]
		row1 = [8, 1]

		for i in range(1, -1, -1):
			for fi in range(1, 9):
				self.make_piece("", row2[i], fi, order[i])
			self.make_piece("R", row1[i], 1, order[i])
			self.make_piece("R", row1[i], 8, order[i])
			self.make_piece("N", row1[i], 2, order[i])
			self.make_piece("N", row1[i], 7, order[i])
			self.make_piece("B", row1[i], 3, order[i])
			self.make_piece("B", row1[i], 6, order[i])
			self.make_piece("K", row1[i], 4, order[i])
			self.make_piece("Q", row1[i], 5, order[i])
			
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
		
		if len(plyr.moves + plyr.takes) == 0 and self.is_check(plyr.color):
			self.checkmate = plyr.color
			return True
		elif len(plyr.moves + plyr.takes) == 0:
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
					piece = self.board[ra][fi]
					color = piece.color
					
					
					if self.plyr1_color == "wh":
						white = plyr
						black = opp
					else: 
						black = plyr
						white = opp
					
					if color == "wh":
						for take in black.takes:	
							if (ra, fi) == take[2:4]:
								self.wh_check = True
								return True
						
						self.wh_check = False
								
					else:
						for take in white.takes:	
							if (ra, fi) == take[2:4]:
								self.bl_check = True
								return True
						self.bl_check = False

	# --------------------------------------------------------------------------------					
	# checks if piece is same color as plyr1_color
	def check_player(self, piece):
		if self.plyr1_color == piece.color:
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
	# checks if move is a valid move
	def valid_move(self, ra1, fi1, ra2, fi2):
		piece = self.board[ra1][fi1]
		
		if ((ra1, fi1, ra2, fi2) in self.moves):
			return piece.valid_move(self, ra2, fi2)

	def in_takes(self, ra1, fi1, ra2, fi2):
		return ((ra1, fi1, ra2, fi2) in self.takes)
		
	def in_moves(self, ra1, fi1, ra2, fi2):
		return ((ra1, fi1, ra2, fi2) in self.moves)
	# --------------------------------------------------------------------------------	
	def gen_moves(self):
		self.plyr1.gen_moves(self)
		self.plyr1.check_avoidance(self)
	
	def gen_opp_moves(self):
		self.plyr2.gen_moves(self)
		self.plyr2.check_avoidance(self)
		
	# --------------------------------------------------------------------------------	
	# UPDATES the VISUAL POSITION of the PIECE if the piece is HELD
	def piece_held(self, my_game, ra, fi, group):
		piece = self.get_piece(ra, fi)
			
		if not piece or not valid_space(ra, fi) or piece.color != my_game.current_move or not self.check_player(piece): 
			return False

		# update piece location to follow mouse
		group.move_to_front(piece)
		piece.rect = pygame.Rect( pygame.mouse.get_pos()[0] - (self.space_height / 2), 
		pygame.mouse.get_pos()[1] - (self.space_height / 2), self.space_height, self.space_height)
		
		# draw highlighted spaces
		self.next_highlight = self.highlight(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
		self.current_highlight = self.highlight_current(ra, fi)

	def piece_released(self, my_game, plyr, opp, ra1, fi1, ra2, fi2):
		piece = self.get_piece(ra1, fi1)
		
		# checking valid move
		if piece == 0 or piece.color != plyr.color or piece.color != my_game.current_move:
			return False
			
		# move piece
		self.gen_moves()
		if plyr.move_piece(self, ra1, fi1, ra2, fi2):
			if ra2 == 1 and isinstance(self.get_piece(ra2, fi2), pieces.Pawn):
				self.promote_pawn(ra2, fi2)
		
			self.update_check(plyr, opp)
			
			if self.update_checkmate(self.plyr2):
				self.last_move = self.last_move + "#"
				my_game.next_move(self)
				return True
			
			if self.is_check(opp.color):
				self.last_move = self.last_move + "+"
				
			self.gen_opp_moves()
			my_game.next_move(self)
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
	def highlight(self, x, y):
		space = self.coord_to_space(x, y)
		ra = space[0]
		fi = space[1]
		
		if not valid_space(ra, fi):
			return False
		
		highlight = Highlight(ra, fi, self)
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
		self.interface.open_pawn_promotion(self.plyr1_color, self)
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
					self.make_piece(piece, ra, fi, self.plyr1_color)
					pawn_promoted = True
					
			newRelease = False		
				
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
	def __init__(self, plyr1_color):
		self.board = [[0 for x in range(9)] for y in range(9)]
		self.plyr1_color = plyr1_color
		self.wh_check = False
		self.bl_check = False
		
	def make_piece(self, piece, ra, fi, color):
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
		piece.kill()
		self.board[ra][fi] = piece
		
	def copy_board(self, my_board):
		for ra in range(1, 9):
			for fi in range(1, 9):
				piece = my_board.get_piece(ra, fi)
				if piece:
					shorthand = piece.shorthand
					self.make_piece(shorthand, ra, fi, piece.color)
				else:
					self.set_space(ra, fi, 0)
					
	def kill(self):
		for ra in range(1, 9):
			for fi in range(1, 9):
				piece = self.get_piece(ra, fi)
				if piece:
					piece.kill()
		
	def virt_move(self, moved_piece, temp_piece, ra1, fi1, ra2, fi2):
		moved_piece.hasMoved = True
		self.set_space(ra2, fi2, moved_piece)
		moved_piece.ra = ra2
		moved_piece.fi = fi2
		if temp_piece != 0: 
			temp_piece.kill()
		self.set_space(ra1, fi1, 0)
		
	def virt_unmove(self, moved_piece, temp_piece, ra1, fi1, ra2, fi2):
		moved_piece.ra = ra1
		moved_piece.fi = fi1
		self.set_space(ra1, fi1, moved_piece)
		self.set_space(ra2, fi2, temp_piece)
		if temp_piece != 0: temp_piece.valid = True
		
# SPRITE CLASSES FOR HIGHLIGHTING SPACES
class Highlight(pygame.sprite.Sprite):
	def __init__(self, ra, fi, board):
		pygame.sprite.Sprite.__init__(self, self.containers)
		rect = board.space_to_rect(ra, fi)
		self.rect = rect
		s = pygame.Surface((rect.width, rect.height))
		s.set_alpha(100)
		s.fill((255, 180, 60))
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

