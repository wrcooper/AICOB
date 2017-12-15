# ------------------------------------------------------
# chess.py
# A chess game with built-in opponent AI and chatbot companion
# Winston Cooper
# 11/5/2017
# ------------------------------------------------------

import pygame, time, os.path, math, board, game, UI, pieces
from pygame.locals import *

# game constants
main_dir = os.path.split(os.path.abspath(__file__))[0]
player_color = "wh"

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

def print_sequence(sequence):
	for i in range(len(sequence)):
		if i % 2 == 0:
			print(str(int(i/2 + 1)) + ".", end=" ")
		print(sequence[i], end=" ") 

# initialize display

def main():
	# initialize display
	pygame.display.init() 
	pygame.init()
	SCREEN = pygame.display.set_mode([0,0], pygame.FULLSCREEN, 0)
	screen_info = pygame.display.Info()

	screen_offset = (screen_info.current_w - screen_info.current_h)/2 # this is the distance from the edge of the board to the edge of the screen

	screen_height = screen_info.current_h
	screen_width = screen_info.current_w

	# initialize images
	images = ["wh_pawn.png", "wh_rook.png", "wh_knight.png", "wh_bishop.png", "wh_king.png", "wh_queen.png"
	,"bl_pawn.png", "bl_rook.png", "bl_knight.png", "bl_bishop.png", "bl_king.png", "bl_queen.png"]

	loaded_images = []
	for image in images:
		loaded_images.append(load_image(image))
	pieces.Piece.images = loaded_images

	# initialize game groups
	piece_group = pygame.sprite.Group()
	highlight = pygame.sprite.GroupSingle()
	highlight_current = pygame.sprite.GroupSingle()
	ui = pygame.sprite.Group()
	all = pygame.sprite.LayeredUpdates()

	# assigning groups to sprite classes
	pieces.Piece.containers = piece_group, all
	board.Highlight.containers = highlight
	board.Highlight_Current.containers = highlight_current
	UI.UI.containers = ui
	UI.Button.containers = ui
	
	# decorate the game window
	pygame.display.set_caption('Artificially Intelligent Chess Oriented Bot')

	# draw the background
	my_board = board.Board(screen_height, screen_offset/10, player_color, SCREEN)
	background = pygame.Surface((screen_height,screen_height))
	bgwood = load_image("wood.jpg").convert()
	bgwood.set_alpha(150)
	my_board.draw(background)
	background.blit(bgwood, (0,0))
	SCREEN.blit(background, (my_board.edge_dist, 0))
	background = SCREEN.copy()
	my_board.set_background(background)
	pygame.display.flip()
	
	# init game and clock
	my_clock = pygame.time.Clock()
	my_game = game.Game(player_color)

	# initialize UI
	interface = UI.UI(screen_info, my_game, load_image("wood2.jpg"))
	interface.init_game_interface()

	#initialize piece sprites
	my_board.init_pieces(my_board.player)

	newClick = False
	newRelease = False
	piece_held = False
	
	

	while(True):
		#print("newClick = " + str(newClick) + " newRelease = " + str(newRelease))
		
		my_clock.tick(60)
	
		for mouseClicked in pygame.event.get(MOUSEBUTTONDOWN):
			lastClick = mouseClicked
			newClick = True
			
		for mouseReleased in pygame.event.get(MOUSEBUTTONUP):
			lastRelease = mouseReleased
			newRelease = True
	
		if newClick:
			if my_board.within(lastClick):
				ra1 = my_board.y_to_rank(lastClick.pos[1])
				fi1 = my_board.x_to_file(lastClick.pos[0])
				my_board.pieceHeld(my_game, ra1, fi1, all)
				piece_held = True
			
			if newRelease:
				newClick = False
				newRelease = False
				
				if piece_held and my_board.within(lastRelease):
					ra2 = my_board.y_to_rank(lastRelease.pos[1])
					fi2 = my_board.x_to_file(lastRelease.pos[0])
					
					my_board.pieceReleased(my_game, ra1, fi1, ra2, fi2)
					piece_held = False
				elif piece_held:
					my_board.pieceReset(ra1, fi1)
					
				interface.update_interface()

		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
					print_sequence(my_game.sequence)
					return
		keystate = pygame.key.get_pressed()
		
		highlight.clear(SCREEN, background)
		highlight_current.clear(SCREEN, background)
		ui.clear(SCREEN, background)
		all.clear(SCREEN, background)
		
		
		highlight_current.draw(SCREEN)
		highlight.draw(SCREEN)
		all.draw(SCREEN)
		ui.draw(SCREEN)
		pygame.display.update()

if __name__ == '__main__': main()
