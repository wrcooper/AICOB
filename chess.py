# ------------------------------------------------------
# chess.py
# A chess game with built in opponent AI and chatbot companion
# Winston Cooper
# 11/5/2017
# ------------------------------------------------------

import pygame, time, os.path, math
from board import *
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

# initialize display

def main():
	# initialize display
	pygame.display.init() 
	SCREEN = pygame.display.set_mode([0,0], pygame.FULLSCREEN, 0)
	screen_info = pygame.display.Info()
	print(str(screen_info.current_w) + " " + str(screen_info.current_h))
	screen_offset = (screen_info.current_w - screen_info.current_h)/2
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
	all = pygame.sprite.RenderUpdates()

	# assing groups to sprite classes
	Piece.containers = pieces, all
	Highlight.containers = highlight
	
	# decorate the game window
	pygame.display.set_caption('Chess Bot')

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

	#initialize sprites
	board.init_pieces(board.player)

	newClick = False
	newRelease = False

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
			board.pieceHeld(ra1, fi1)
			print(all.sprites())
			
			if newRelease:
				print("Clicked: ")
				print(ra1, fi1)
				newClick = False
				print("Released: ")
				ra2 = board.y_to_rank(lastRelease.pos[1])
				fi2 = board.x_to_file(lastRelease.pos[0])
				print(ra2, fi2)
				newRelease = False
				board.pieceReleased(ra1, fi1, ra2, fi2)

		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
					return
		keystate = pygame.key.get_pressed()

		if keystate[K_q]:
			print("q pressed!")
		
		highlight.clear(SCREEN, background)
		all.clear(SCREEN, background)
		
		highlight.draw(SCREEN)
		all.draw(SCREEN)
		pygame.display.update(board.rect)

if __name__ == '__main__': main()
