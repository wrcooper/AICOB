# ------------------------------------------------------
# chess.py
# A chess game with built in opponent AI and chatbot companion
# Winston Cooper
# 11/5/2017
# ------------------------------------------------------

import pygame, time, os.path, math
from board import *
from game import *
from pygame.locals import *
from UI import *

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
	Piece.images = loaded_images

	# initialize game groups
	pieces = pygame.sprite.Group()
	highlight = pygame.sprite.GroupSingle()
	highlight_current = pygame.sprite.GroupSingle()
	ui = pygame.sprite.Group()
	all = pygame.sprite.LayeredUpdates()

	# assigning groups to sprite classes
	Piece.containers = pieces, all
	Highlight.containers = highlight
	Highlight_Current.containers = highlight_current
	UI.containers = ui
	Button.containers = ui
	
	# decorate the game window
	pygame.display.set_caption('Artificially Intelligent Chess Oriented Bot')

	# draw the background
	board = Board(screen_height, screen_offset/10, player_color, SCREEN)
	background = pygame.Surface((screen_height,screen_height))
	bgwood = load_image("wood.jpg").convert()
	bgwood.set_alpha(150)
	board.draw(background)
	background.blit(bgwood, (0,0))
	SCREEN.blit(background, (board.edge_dist, 0))
	background = SCREEN.copy()
	board.set_background(background)
	pygame.display.flip()

	# initialize UI
	interface = UI(screen_info, load_image("wood2.jpg"))
	interface.init_buttons()

	#initialize piece sprites
	board.init_pieces(board.player)

	newClick = False
	newRelease = False
	game = Game(player_color)

	while(True):
		for mouseClicked in pygame.event.get(MOUSEBUTTONDOWN):
			lastClick = mouseClicked
			newClick = True
		for mouseReleased in pygame.event.get(MOUSEBUTTONUP):
			lastRelease = mouseReleased
			newRelease = True
	
		if newClick:
			ra1 = board.y_to_rank(lastClick.pos[1])
			fi1 = board.x_to_file(lastClick.pos[0])
			board.pieceHeld(game, ra1, fi1, all)
			
			if newRelease:
				newClick = False
				ra2 = board.y_to_rank(lastRelease.pos[1])
				fi2 = board.x_to_file(lastRelease.pos[0])
				newRelease = False
				board.pieceReleased(game, ra1, fi1, ra2, fi2)

		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
					print_sequence(game.sequence)
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
