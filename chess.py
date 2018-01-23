# ------------------------------------------------------
# chess.py
# A chess game with built-in opponent AI and chatbot companion
# Winston Cooper
# 11/5/2017
# ------------------------------------------------------

import pygame, time, os.path, math, board, game, UI, pieces, intelligence as intel, player
from pygame.locals import *

# ---------------------------
# game constants
main_dir = os.path.split(os.path.abspath(__file__))[0]
plyr1_color = "wh"

# ---------------------------
# load images
def load_image(file):
	file = os.path.join(main_dir, 'data', file)
	try:
		surface = pygame.image.load(file)
	except pygame.error:
		raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
	return surface.convert_alpha()

def load_images(*files):
	imgs = []
	for file in files:
		imgs.append(load_image(file))
	return imgs
	
# ---------------------------
def print_sequence(sequence):
	for i in range(len(sequence)):
		if i % 2 == 0:
			print(str(int(i/2 + 1)) + ".", end=" ")
		print(sequence[i], end=" ") 
		
def main():
	# --------------------------------------------------------------------------------
	# initialize display
	pygame.display.init() 
	pygame.init()
	SCREEN = pygame.display.set_mode([0,0], pygame.FULLSCREEN, 0)
	scrn_info = pygame.display.Info()

	scrn_height = scrn_info.current_h
	scrn_width = scrn_info.current_w

	# --------------------------------------------------------------------------------
	# initialize images
	images = ["wh_pawn.png", "wh_rook.png", "wh_knight.png", "wh_bishop.png", "wh_king.png", "wh_queen.png"
	,"bl_pawn.png", "bl_rook.png", "bl_knight.png", "bl_bishop.png", "bl_king.png", "bl_queen.png"]

	loaded_images = []
	for image in images:
		loaded_images.append(load_image(image))
	pieces.Piece.images = loaded_images
	
	ui_images = ["left_arrow_button.png", "right_arrow_button.png", "toggle_button.png"]
	
	loaded_ui_images = []
	for image in ui_images:
		loaded_ui_images.append(load_image(image))
	UI.UI.images = loaded_ui_images

	# --------------------------------------------------------------------------------
	# initialize game groups
	piece_group = pygame.sprite.Group()
	highlight = pygame.sprite.GroupSingle()
	highlight_current = pygame.sprite.GroupSingle()
	ui = pygame.sprite.LayeredUpdates()
	all = pygame.sprite.LayeredUpdates()

	# --------------------------------------------------------------------------------
	# assigning groups to sprite classes
	pieces.Piece.containers = piece_group, all
	board.Highlight.containers = highlight
	board.Highlight_Current.containers = highlight_current
	UI.UI.containers = ui
	UI.Element.containers = ui
	
	# --------------------------------------------------------------------------------
	# decorate the game window
	pygame.display.set_caption('Artificially Intelligent Chess Oriented Bot')

	# --------------------------------------------------------------------------------
	# init board, draw the background
	my_board = board.Board(scrn_info, plyr1_color, SCREEN)
	wood = load_image("wood.jpg").convert()
	my_board.bg_init(wood)
	
	# --------------------------------------------------------------------------------
	# init game and clock
	my_clock = pygame.time.Clock()
	my_game = game.Game(plyr1_color)
	my_game.set_board(my_board)

	# --------------------------------------------------------------------------------
	# initialize UI
	interface = UI.UI(scrn_info, my_game, load_image("wood2.jpg"))
	interface.init_game_interface()

	# --------------------------------------------------------------------------------
	#initialize piece sprites
	my_board.init_pieces(plyr1_color)
	
	# --------------------------------------------------------------------------------
	#initialize player and opponent
	plyr = player.Player(my_board, "wh", board.Board.BOT)
	my_board.plyr1 = plyr
	
	opp = intel.Intelligence(my_board, "bl", board.Board.TOP)
	my_board.plyr2 = opp
	
	my_board.set_interface(interface, ui)
	
	# ORDER MATTERS
	my_board.set_groups(highlight, highlight_current, all, ui)


	newClick = False
	newRelease = False
	piece_held = False
	
	ra1 = 0
	fi1 = 0

	while(True):
		
		# IF BLACK'S MOVE, MAKE MOVE
		if my_game.current_move == "bl":
			my_board.plyr2.move(my_board, my_game)
			my_board.plyr1.gen_moves(my_board)
			interface.update_interface()
		
		if my_game.current_move == "wh" and my_game.player1 == "Computer":
			my_board.plyr1.move(my_board, my_game)
			my_board.plyr2.gen_moves(my_board)
			interface.update_interface()
		
		# LIMIT FRAMERATE to 60
		my_clock.tick(60)
	
		# GET CLICKS
		for mouseClicked in pygame.event.get(MOUSEBUTTONDOWN):
			lastClick = mouseClicked
			newClick = True
			
		# GET MOUSE RELEASES
		for mouseReleased in pygame.event.get(MOUSEBUTTONUP):
			lastRelease = mouseReleased
			newRelease = True
	
		# PICK UP PIECE IF CLICKED
		if newClick:
			if my_board.within(lastClick):
				ra1 = my_board.y_to_rank(lastClick.pos[1])
				fi1 = my_board.x_to_file(lastClick.pos[0])
				piece_held = True
				newClick = False
			
		if piece_held:
			my_board.piece_held(my_game, ra1, fi1, all)
			
		# RELEASE PIECE; IF RELEASED, ATTEMPT MOVE
		if newRelease:
			newRelease = False
			interface.clicked(lastRelease)
				
			if piece_held and my_board.within(lastRelease) and my_game.current_move == plyr.color and isinstance(my_board.plyr1, player.Player):
				ra2 = my_board.y_to_rank(lastRelease.pos[1])
				fi2 = my_board.x_to_file(lastRelease.pos[0])
					
				my_board.piece_released(my_game, plyr, opp, ra1, fi1, ra2, fi2)
				
				piece_held = False
				my_board.update()
				
			elif piece_held:
				my_board.piece_reset(ra1, fi1)
				piece_held = False
					
			interface.update_interface()
			
		# IF ESC PRESSED, QUIT PROGRAM
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
					print_sequence(my_game.sequence)
					return
		keystate = pygame.key.get_pressed()
		
		# UPDATE AND DRAW SCREEN
		my_board.update()

if __name__ == '__main__': main()
