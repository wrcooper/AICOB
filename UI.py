import pygame, pieces, sys
from pygame.locals import *

class UI(pygame.sprite.Sprite):
	def __init__(self, screen_info, game, image):
		pygame.sprite.Sprite.__init__(self, self.containers)
		
		self.main_menu = True
		self.game_end = False
		
		self.elements = []
		
		self.screen_w = screen_info.current_w
		self.screen_h = screen_info.current_h
		
		# dimensions for ui
		self.screen_offset = (self.screen_w - self.screen_h) / 2
		self.edge_dist = self.screen_offset / 10 
		
		self.start_x = (2 * self.edge_dist) + self.screen_h
		self.end_x = self.screen_w - self.edge_dist
		self.rect_w = self.end_x - self.start_x
		#print("rect_w = " + str(self.rect_w) + " start_x = " + str(self.start_x))
		
		self.top_button_border = (self.screen_h * 3) / 100
		self.left_button_border = (self.rect_w * 3) / 100
		
		self.rect = pygame.Rect(self.start_x, 0, self.rect_w, self.screen_h)

		s = pygame.Surface((self.rect_w, self.screen_h))
		s.blit(image, (0,0), (0, 0, self.rect_w, self.screen_h))

		self.image = s
		
		self.game = game
		self.update_game_info(self.game)
		
	def clicked(self, click):
		#print("click!")
		if (click.pos[0] > self.start_x and click.pos[0] < self.end_x and click.pos[1] > 0):	
			for element in self.elements:
				result = element.clicked(click)
				if result != None:
					return result

	def get_font(size):
		font = pygame.font.Font(None, size)
		return font

	def update_game_info(self, game):
		self.current_move = game.current_move
		self.turn_number = game.turn_number
		self.player_color = game.player_color
		self.pgn = game.pgn
		
	def open_settings_page(self):
		self.main_menu = False
		self.settings = True
		self.remove_elements()
		self.init_settings()
		
	def remove_elements(self):
		for element in self.elements:
			element.kill()
		self.elements = []
			
	def change_depth(self, inc):
		self.game.depth += inc
		if self.game.depth < 1:
			self.game.depth = 1
			
	def change_wait(self, inc):
		self.game.ai_wait += inc
		if self.game.ai_wait < 0:
			self.game.ai_wait = 0
		
	def init_game_interface(self):
		self.turn_number = Turn_Number(self)
		self.to_move = To_Move(self)
		self.player_name_elt = Player_Name(self)
		self.player_color = Player_Color(self)
		self.new_game_button = New_Game_Button(self)
		self.settings = Settings(self)
		self.pgn = PGN(self)
		self.score = Score(self)
		
		self.elements = [self.turn_number, self.to_move, self.player_name_elt, self.player_color, 
			self.new_game_button, self.settings, self.pgn, self.score]
	
	def init_settings(self):
		self.settings_page = Settings_Page(self)
		self.elements.append(self.settings_page)
			
	def update_interface(self):
		self.remove_elements()
		
		self.update_game_info(self.game)
		if self.main_menu: 
			self.init_game_interface()
		elif self.settings: self.init_settings()
		
		if self.game_end: 
			#print("game_end is: " + str(self.game_end))
			self.open_end_game()
		
	def draw(self, scrn):
		bgd = scrn.copy()
		self.containers.clear(scrn, bgd)
		self.containers.draw(scrn)
		pygame.display.update()
		
	def open_pawn_promotion(self, color, my_board):
		self.pawn_prom = Pawn_Promotion(self, color, my_board)
		self.elements.append(self.pawn_prom)
		
	def open_end_game(self):
		self.end_game = End_Game(self)
		self.elements.append(self.end_game)
		
	def select_promotion(self, mouse):
		if self.pawn_prom is not None:
			return self.pawn_prom.select_promotion(mouse)
		
	def color_to_str(color):
		if color == "wh":
			return "White"
		else:
			return "Black"


class Element(pygame.sprite.Sprite):
	def __init__(self, parent):
		pygame.sprite.Sprite.__init__(self, self.containers)
		
		centered = False
		self.dimensions()
		self.centered()
		self.set_border()
		
		self.parent = parent
		
		self.width = int((self.w_percent * parent.rect_w) / 100)
		self.height = int((self.h_percent * parent.screen_h) / 100)
		
		self.stroke = 10
		
		if (self.centered):	
			x = parent.start_x + int((parent.rect_w - self.width)/2)
		else:
			x = (self.x_percent * parent.rect_w)/100 + parent.start_x + parent.left_button_border
			
		y = parent.top_button_border + (self.y_percent * parent.screen_h)/100
		
		self.rect = pygame.Rect(x, y, self.width, self.height)
		
		if self.border:
			s = pygame.Surface((self.width, self.height))
			b = pygame.Surface((self.width - self.stroke, self.height - self.stroke))
			
			s.fill((0,0,0))
			b.fill((255,255,255))
			
			s.blit(b, (self.stroke/2, self.stroke/2))
			
		else:
			s = pygame.Surface((self.width, self.height))
			s.fill((255,255,255))
		
		self.image = s
		
	def get_middle(self):
		return int(self.rect.w * .5)
		
	def set_border(self, setting = True):
		self.border = setting
	
	def dimensions(self):
		self.w_percent = 0
		self.h_percent = 0
		self.x_percent = 0
		self.y_percent = 0
		
	def centered(self):
		self.centered = False
	
	def clicked(self, click):
		if (click.pos[0] > self.rect.x and click.pos[0] < self.rect.x + self.rect.w and click.pos[1] < self.rect.y + self.rect.h and click.pos[1] > self.rect.y):	
			return self.click_function()
	
	def click_function(self):
		return
		#print(str(self))
		
class Enter_Name(pygame.sprite.Sprite):
	def __init__(self, scrn_info):
		pygame.sprite.Sprite.__init__(self, self.containers)
		w_percent = 20
		h_percent = 15
		
		scrn_w = scrn_info.current_w
		scrn_h = scrn_info.current_h
		
		width = int((scrn_w * w_percent)/100)
		height = int((scrn_h * h_percent)/100)
		
		x = (scrn_w - width)/2
		y = (scrn_h - height)/2
		
		surf = pygame.Surface((width, height))
		surf.fill((255,255,255))
		
		text = "Player Name: "
		subtext = "(type and press enter to submit)"
		subtext2 = "press ESC at any time to quit the game"
		
		font = UI.get_font(60)
		smallfont = UI.get_font(25)
		
		text_surf = font.render(text, True, (0,0,0))
		subtext_surf = smallfont.render(subtext, True, (0,0,0))
		subtext2_surf = smallfont.render(subtext2, True, (0,0,0))
		
		self.subtext_size = smallfont.size(subtext)
		subtext_x = (width - self.subtext_size[0])/2
		
		self.subtext2_size = smallfont.size(subtext2)
		subtext2_x = (width - self.subtext2_size[0])/2
		
		self.text_size = font.size(text)
		text_x = (width - self.text_size[0])/2
		
		subtext_y = 10
		self.subtext_y = subtext_y
		
		self.text_x = text_x
		self.text_y = (self.subtext_y + self.subtext_size[1]) + 10
		
		
		self.font = font
		
		surf.blit(text_surf, (text_x, self.text_y))
		surf.blit(subtext_surf, (subtext_x, subtext_y))
		surf.blit(subtext2_surf, (subtext2_x, height - self.subtext2_size[1] - 15))
		
		self.blank = surf.copy()
		self.image = surf
		
		self.rect = pygame.rect.Rect(x, y, width, height)
		
	def get_name(self, screen):
		self.name = ""
		bgd = screen
		enter_pressed = False
		while not enter_pressed:
			self.containers.clear(screen, bgd)
			self.containers.draw(screen)
			pygame.display.flip()
			
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == K_RETURN and len(self.name) > 0:
						return self.name
					elif event.key == K_BACKSPACE:
						self.name = self.name[:-1]
						self.update_name()
					elif event.key > 31 and event.key < 127 and len(self.name) < 10: 
						self.name += (event.unicode)
						self.update_name()
					elif event.key == K_ESCAPE:
						sys.exit()
				elif event.type == pygame.QUIT: sys.exit()
						
	def update_name(self):
		name_surf = self.font.render(self.name, True, (0,0,0))
		name_size = self.font.size(self.name)
		
		name_y = self.text_y + self.text_size[1] + 10
		
		name_x = (self.rect.w - name_size[0])/2
		surf = self.blank.copy()
		surf.blit(name_surf, (name_x, name_y)) 
		self.image = surf
		
	
class Turn_Number(Element):
	def __init__(self, parent):
		Element.__init__(self, parent)
		font = UI.get_font(45)
		text = "Turn Number: " + str(parent.turn_number)
		s = font.render(text, True, (0, 0, 0))
		
		size = font.size(text)
		left_border = (self.width - size[0])/2
		top_border = (self.height - size[1])/2		
		
		self.image.blit(s, (left_border, top_border))
	
	def dimensions(self):
		self.w_percent = 45
		self.h_percent = 6.5
		self.x_percent = 0
		self.y_percent = 0
		
class To_Move(Element):
	def __init__(self, parent):
		Element.__init__(self, parent)
		font = UI.get_font(50)
		move = UI.color_to_str(parent.current_move)
		text = "To Move: " + move
		s = font.render(text, True, (0, 0, 0))
		
		size = font.size(text)
		left_border = (self.width - size[0])/2
		top_border = (self.height - size[1])/2		
		
		self.image.blit(s, (left_border, top_border))
	
	def dimensions(self):
		self.w_percent = 45
		self.h_percent = 6.5
		self.x_percent = 49
		self.y_percent = 0
		
class Player_Name(Element):
	def __init__(self, parent):
		Element.__init__(self, parent)
		font = UI.get_font(40)
		text = "Player: " + parent.player_name
		s = font.render(text, True, (0, 0, 0))
		
		size = font.size(text)
		left_border = (self.width - size[0])/2
		top_border = (self.height - size[1])/2		
		
		self.image.blit(s, (left_border, top_border))
	
	def dimensions(self):
		self.w_percent = 45
		self.h_percent = 6.5
		self.x_percent = 0
		self.y_percent = 8
		
class Player_Color(Element):
	def __init__(self, parent):
		Element.__init__(self, parent)
		font = UI.get_font(38)
		text = "Player Color: " + UI.color_to_str(parent.player_color)
		s = font.render(text, True, (0, 0, 0))
		
		size = font.size(text)
		left_border = (self.width - size[0])/2
		top_border = (self.height - size[1])/2		
		
		
		self.image.blit(s, (left_border, top_border))
	
	def dimensions(self):
		self.w_percent = 45
		self.h_percent = 6.5
		self.x_percent = 49
		self.y_percent = 8
				
class New_Game_Button(Element):
	def __init__(self, parent):
		Element.__init__(self, parent)
		font = UI.get_font(60)
		text = "New Game"
		s = font.render(text, True, (0, 0, 0))
		
		size = font.size(text)
		left_border = (self.width - size[0])/2
		top_border = (self.height - size[1])/2		
		
		self.image.blit(s, (left_border, top_border))
		
	def click_function(self):
		self.parent.game.new_game()
		return "new_game"
	
	def dimensions(self):
		self.w_percent = 94
		self.h_percent = 6.5
		self.x_percent = 0
		self.y_percent = 16.5
		
	def centered(self):
		self.centered = True
				
class Settings(Element):
	def __init__(self, parent):
		Element.__init__(self, parent)
		font = UI.get_font(60)
		text = "Settings"
		s = font.render(text, True, (0, 0, 0))
		
		size = font.size(text)
		left_border = (self.width - size[0])/2
		top_border = (self.height - size[1])/2		
		
		self.image.blit(s, (left_border, top_border))
		
	def click_function(self):
		self.parent.open_settings_page()
	
	def dimensions(self):
		self.w_percent = 94
		self.h_percent = 6.5
		self.x_percent = 0
		self.y_percent = 24.5
		
	def centered(self):
		self.centered = True
		
# Settings --------------------------------------------------------------------------------
		
class Settings_Page(Element):
	def __init__(self, parent):
		Element.__init__(self, parent)
		text = "press ESC at any time to quit the game"
		font = UI.get_font(25)
		text_surf = font.render(text, True, (0,0,0))
		text_size = font.size(text)
		self.image.blit(text_surf, (self.rect.w - text_size[0] - 30, 30))
		
		
		depth_selector = AI_Depth_Selector(parent)
		wait_selector = AI_Wait_Selector(parent)
		back_button = Back_Button(parent)
		player_select = Player_Select(parent)
		user_config = User_Config(parent)
		
		parent.elements.append(depth_selector)
		parent.elements.append(wait_selector)
		parent.elements.append(back_button)
		parent.elements.append(player_select)
		parent.elements.append(user_config)
	
	def dimensions(self):
		self.w_percent = 94
		self.h_percent = 95
		self.x_percent = 0
		self.y_percent = 0
	
class Back_Button(Element):
	def __init__(self, parent):
		Element.__init__(self, parent)
		font = UI.get_font(40)
		text = "Back"
		s = font.render(text, True, (0,0,0))
		self.image.blit(s, (self.stroke, self.stroke))
		
		size = font.size(text)
		self.rect.y = size[0] + 10
		
	def click_function(self):
		self.parent.main_menu = True
		
	def dimensions(self):
		self.w_percent = 15
		self.h_percent = 4
		self.x_percent = 5
		self.y_percent = 2.5
		
class AI_Depth_Selector(Element):
	def __init__(self, parent):
		Element.__init__(self, parent)
		font = UI.get_font(50)
		smallfont = UI.get_font(20)
		text = "AI Move Algorithm Depth: " 
		note = "(default: 3, any more than 3 may result in ridiculous processing time!)"
		title_s = font.render(text, True, (0,0,0))
		
		size = font.size(text)
		
		self.arrow_w = 60
		self.arrow_h = 60
		
		depth = str(parent.game.depth)
		depth_s = font.render(depth, True, (0,0,0))
		depth_size = font.size(depth)
		
		note_s = smallfont.render(note, True, (0,0,0))
		note_size = smallfont.size(note)
		
		left_arrow = pygame.transform.smoothscale(parent.images[0], (self.arrow_w, self.arrow_h))
		right_arrow = pygame.transform.smoothscale(parent.images[1], (self.arrow_w, self.arrow_h))
		
		middle_x = int(self.rect.w * .5)
		
		title_offset = middle_x-(size[0]/2)
		
		self.image.blit(title_s, (self.stroke + title_offset, self.stroke))
		self.image.blit(left_arrow, (30, size[1] + 10))
		self.image.blit(depth_s, (middle_x - depth_size[0], size[1] + 25))
		self.image.blit(right_arrow, (self.rect.w - (30 + self.arrow_w), size[1] + 10))
		self.image.blit(note_s, (middle_x - (note_size[0])/2, 3 * size[1] + 8))
		
		
		self.left_arrow_x = self.rect.x + 30
		self.left_arrow_y = self.rect.y + size[1] + 10
		
		self.right_arrow_x = self.rect.x + (self.rect.w - (30 + self.arrow_w))
		self.right_arrow_y = self.rect.y + size[1] + 10
	
	def clicked(self, click):
		if (click.pos[0] > self.rect.x and click.pos[0] < self.rect.x + self.rect.w and click.pos[1] < self.rect.y + self.rect.h and click.pos[1] > self.rect.y):	
			self.left_arrow_clicked(click)
			self.right_arrow_clicked(click)

	def left_arrow_clicked(self, click):
		x = click.pos[0]
		y = click.pos[1]
		if (x > self.left_arrow_x and x < self.left_arrow_x + self.arrow_w and y > self.left_arrow_y and y < self.left_arrow_y + self.arrow_w):
			self.parent.change_depth(-1)
	
	def right_arrow_clicked(self, click):
		x = click.pos[0]
		y = click.pos[1]
		if (x > self.right_arrow_x and x < self.right_arrow_x + self.arrow_w and y > self.right_arrow_y and y < self.right_arrow_y + self.arrow_w):
			self.parent.change_depth(1)	
		
	
	def dimensions(self):
		self.w_percent = 80
		self.h_percent = 12
		self.x_percent = 7.5
		self.y_percent = 9
		
class AI_Wait_Selector(Element):
	def __init__(self, parent):
		Element.__init__(self, parent)
		font = UI.get_font(50)
		smallfont = UI.get_font(20)
		text = "AI Wait Time (sec): " 
		note = "(Wait time during precalculated AI moves; makes them easier to follow)"
		title_s = font.render(text, True, (0,0,0))
		
		size = font.size(text)
		
		self.arrow_w = 60
		self.arrow_h = 60
		
		wait = str(parent.game.ai_wait)
		wait_s = font.render(wait, True, (0,0,0))
		wait_size = font.size(wait)
		
		note_s = smallfont.render(note, True, (0,0,0))
		note_size = smallfont.size(note)
		
		left_arrow = pygame.transform.smoothscale(parent.images[0], (self.arrow_w, self.arrow_h))
		right_arrow = pygame.transform.smoothscale(parent.images[1], (self.arrow_w, self.arrow_h))
		
		middle_x = int(self.rect.w * .5)
		
		title_offset = middle_x-(size[0]/2)
		
		self.image.blit(title_s, (self.stroke + title_offset, self.stroke))
		self.image.blit(left_arrow, (30, size[1] + 10))
		self.image.blit(wait_s, (middle_x - wait_size[0], size[1] + 25))
		self.image.blit(right_arrow, (self.rect.w - (30 + self.arrow_w), size[1] + 10))
		self.image.blit(note_s, (middle_x - (note_size[0])/2, 3 * size[1] + 8))
		
		self.left_arrow_x = self.rect.x + 30
		self.left_arrow_y = self.rect.y + size[1] + 10
		
		self.right_arrow_x = self.rect.x + (self.rect.w - (30 + self.arrow_w))
		self.right_arrow_y = self.rect.y + size[1] + 10
	
	def clicked(self, click):
		if (click.pos[0] > self.rect.x and click.pos[0] < self.rect.x + self.rect.w and click.pos[1] < self.rect.y + self.rect.h and click.pos[1] > self.rect.y):	
			self.left_arrow_clicked(click)
			self.right_arrow_clicked(click)

	def left_arrow_clicked(self, click):
		x = click.pos[0]
		y = click.pos[1]
		if (x > self.left_arrow_x and x < self.left_arrow_x + self.arrow_w and y > self.left_arrow_y and y < self.left_arrow_y + self.arrow_w):
			self.parent.change_wait(-0.5)
	
	def right_arrow_clicked(self, click):
		x = click.pos[0]
		y = click.pos[1]
		if (x > self.right_arrow_x and x < self.right_arrow_x + self.arrow_w and y > self.right_arrow_y and y < self.right_arrow_y + self.arrow_w):
			self.parent.change_wait(0.5)	
		
	
	def dimensions(self):
		self.w_percent = 80
		self.h_percent = 12
		self.x_percent = 7.5
		self.y_percent = 35
		
class Player_Select(Element):
	def __init__(self, parent):
		Element.__init__(self, parent)
		font = UI.get_font(50)
		player2_text = "Player 2: " + parent.game.player2
		player1_text = "Player 1: " + parent.game.player1
		
		player2_surf = font.render(player2_text, True, (0,0,0))
		player2_size = font.size(player2_text)
		
		player1_surf = font.render(player1_text, True, (0,0,0))
		player1_size = font.size(player1_text)
		
		mid_x = self.get_middle()
		
		self.image.blit(player2_surf, (20, 20))
		player1_y = (player2_size[1] + 40)
		self.image.blit(player1_surf, (20, player1_y))
		
		toggle_button = pygame.transform.smoothscale(parent.images[2], (100, 50))
		toggle_rect = toggle_button.get_rect()
		
		toggle_x = self.rect.w - toggle_rect.w - 20
		#toggle1_y = 14
		toggle2_y = player1_y - 7
		
		#self.image.blit(toggle_button, (toggle_x, toggle1_y))
		self.image.blit(toggle_button, (toggle_x, toggle2_y))
		
		#self.toggle1_rect = pygame.rect.Rect(toggle_x, toggle1_y, 100, 50)
		self.toggle_x = self.rect.x + toggle_x
		self.toggle2_y = self.rect.y + toggle2_y
		self.toggle_w  = 100
		self.toggle_h = 50
		
	def clicked(self, click):
		if (click.pos[0] > self.rect.x and click.pos[0] < self.rect.x + self.rect.w and click.pos[1] < self.rect.y + self.rect.h and click.pos[1] > self.rect.y):
			self.toggle2_clicked(click)
			
	def toggle2_clicked(self, click):
		#print(click.pos[0])
		#print(self.toggle_x)
		if (click.pos[0] > self.toggle_x and click.pos[0] < self.toggle_x + self.toggle_w and click.pos[1] < self.toggle2_y + self.toggle_h and click.pos[1] > self.toggle2_y):	
			self.parent.game.toggle_player()
		
	def dimensions(self):
		self.w_percent = 80
		self.h_percent = 12
		self.x_percent = 7.5
		self.y_percent = 22
		
		
class User_Config(Element):
	def __init__(self, parent):
		Element.__init__(self, parent)
		font = UI.get_font(40)
		change_player_text = "Change Player Name: "
		reset_move_dict_text = "Reset Move Dictionary: "
		
		change_player_surf = font.render(change_player_text, True, (0,0,0))
		change_player_size = font.size(change_player_text)
		
		reset_move_dict_surf = font.render(reset_move_dict_text, True, (0,0,0))
		reset_move_dict_size = font.size(reset_move_dict_text)
		
		mid_x = self.get_middle()
		
		self.image.blit(change_player_surf, (20, 25))
		reset_move_dict_y = (change_player_size[1] + 55)
		self.image.blit(reset_move_dict_surf, (20, reset_move_dict_y))
		
		reset_button = pygame.transform.smoothscale(parent.images[3], (100, 50))
		change_button = pygame.transform.smoothscale(parent.images[4], (100, 50))
		reset_rect = reset_button.get_rect()
		
		reset_x = self.rect.w - reset_rect.w - 20
		reset_y = reset_move_dict_y - 5
		
		change_x = reset_x
		change_y = 15
		
		self.image.blit(change_button, (change_x, change_y))
		self.image.blit(reset_button, (reset_x, reset_y))
		
		self.reset_x = self.rect.x + reset_x
		self.reset_y = self.rect.y + reset_y
		self.reset_w  = 100
		self.reset_h = 50
		
		self.change_x = self.rect.x + change_x
		self.change_y = self.rect.y + change_y
		self.change_w = 100
		self.change_h = 50
		
	def clicked(self, click):
		if (click.pos[0] > self.rect.x and click.pos[0] < self.rect.x + self.rect.w and click.pos[1] < self.rect.y + self.rect.h and click.pos[1] > self.rect.y):
			self.reset_clicked(click)
			self.change_clicked(click)
			
	def reset_clicked(self, click):
		if (click.pos[0] > self.reset_x and click.pos[0] < self.reset_x + self.reset_w and click.pos[1] < self.reset_y + self.reset_h and click.pos[1] > self.reset_y):	
			self.parent.game.reset_move_dict()
			
	def change_clicked(self, click):
		if (click.pos[0] > self.change_x and click.pos[0] < self.change_x + self.change_w and click.pos[1] < self.change_y + self.change_h and click.pos[1] > self.change_y):	
			self.parent.game.change_player_name()
		
	def dimensions(self):
		self.w_percent = 80
		self.h_percent = 12
		self.x_percent = 7.5
		self.y_percent = 48
		
		
# End Settings --------------------------------------------------------------------------------		

class PGN(Element):
	def __init__(self, parent):
		Element.__init__(self, parent)
		font = UI.get_font(30)
		text = "PGN: " + parent.pgn
		
		words = text.split(' ')
		line = ""
		i = 0
		left_border = 5
		top_border = 5
		
		for word in words:
			if font.size(line + word)[0] > self.width - 5:
				s = font.render(line, True, (0, 0, 0))
				self.image.blit(s, (left_border + 5, top_border + 5 + (i * 25) ))
				line = ""
				i += 1
			line += word + " "
		s = font.render(line, True, (0, 0, 0))
		self.image.blit(s, (left_border + 5, top_border + 5 + (i * 25) ))
	
	def dimensions(self):
		self.w_percent = 94
		self.h_percent = 30
		self.x_percent = 0
		self.y_percent = 33
		
	def centered(self):
		self.centered = True
		
class Score(Element):
	def __init__(self, parent):
		Element.__init__(self, parent)
		if parent.game.paused == False:
			text = "Playing..."
		else: text = "Paused"
		
		subtext = "(press SPACEBAR to pause game)"
		
		font = UI.get_font(40)
		smallfont = UI.get_font(25)
		
		text_surf = font.render(text, True, (0,0,0))
		subtext_surf = smallfont.render(subtext, True, (0,0,0))
		
		text_size = font.size(text)
		subtext_size = smallfont.size(subtext)
		
		self.text_x = (self.rect.w - text_size[0])/2
		self.text_y = 10
		
		self.subtext_x = (self.rect.w - subtext_size[0])/2
		self.subtext_y = self.text_y + text_size[1] + 5
		
		self.image.blit(text_surf, (self.text_x, self.text_y))
		self.image.blit(subtext_surf, (self.subtext_x, self.subtext_y))
		
		left_border = 0
		top_border = 0	
		
	
	def dimensions(self):
		self.w_percent = 94
		self.h_percent = 30
		self.x_percent = 0
		self.y_percent = 65
		
	def centered(self):
		self.centered = True
		
class End_Game(Element):
	def __init__(self, parent):
		pygame.sprite.Sprite.__init__(self, self.containers)
		
		self.parent = parent
		
		if parent.game.winner == "Draw":
			end_text = "Draw!!"
		else:
			end_text = parent.game.winner + " has won!!"
			
		font = UI.get_font(80)
		text_size = font.size(end_text)
		text_surf = font.render(end_text, True, (0,0,0))
		
		self.dimensions()
		self.inner_dimensions()
		
		outer_w = parent.screen_h * self.w_percent / 100
		outer_h = parent.screen_h * self.h_percent / 100
		outer_x = (parent.screen_h - outer_w) / 2 + parent.edge_dist
		outer_y = (parent.screen_h - outer_h) / 2
		
		self.start_x = outer_x
		self.start_y = outer_y
		
		self.rect = pygame.Rect(outer_x, outer_y, outer_w, outer_h)
		outer = pygame.Surface((outer_w, outer_h))
		outer.fill((0, 0, 0))
		
		self.inner_w = parent.screen_h * self.inner_w_percent / 100
		self.inner_h = parent.screen_h * self.inner_h_percent / 100
		
		inner = pygame.Surface((self.inner_w, self.inner_h))
		inner.fill((255, 255, 255))
		
		inner.blit(text_surf, ((self.inner_w - text_size[0])/2, (self.inner_h - text_size[1])/2))
		
		self.inner_x = (outer_w - self.inner_w) / 2
		self.inner_y = (outer_h - self.inner_h) / 2
		
		outer.blit(inner, (self.inner_x, self.inner_y))
		
		self.image = outer
		
	def animate(self, my_board, scrn, color):
		radius = 50
		scale = 1
		dscale = 0.8
		
		my_board.update()
		
		Circle.containers = self.parent.containers
		background = scrn.copy()
		width = 40
	
		for i in range(200):
			if 5 * radius > self.parent.screen_h:
				width -= 2
				if width < 1: width = 1
		
			circle = Circle(int(radius), color, self.parent, width)
			self.parent.containers.move_to_front(circle)
			self.parent.containers.move_to_front(self)
			my_board.interface_group.clear(scrn, background)
			my_board.interface_group.draw(scrn)
			pygame.display.update()
			
			circle.kill()
			radius += scale
			scale += dscale
			
			if 2*radius > self.parent.screen_h + 200: break
		
		my_board.update()
		my_board.interface_group.draw(scrn)
		pygame.display.flip()
		
	def dimensions(self):
		self.w_percent = 52.5
		self.h_percent = 15
		
	def inner_dimensions(self):
		self.inner_w_percent = 50
		self.inner_h_percent = 12.5
		
class Circle(pygame.sprite.Sprite):
	def __init__(self, radius, color, parent, width):
		pygame.sprite.Sprite.__init__(self, self.containers)
		s = pygame.surface.Surface((2*radius, 2*radius), pygame.SRCALPHA, 32)
		pygame.draw.circle(s, color, (int(radius), int(radius)), radius, width)
		s.set_alpha(0)
		self.image = s.convert_alpha()
		middle_x = int(parent.screen_h/2 + parent.edge_dist)
		middle_y = int(parent.screen_h/2)
		self.rect = pygame.rect.Rect(int(middle_x - radius), int(middle_y - radius), 2 * radius, 2 * radius)
	
				
class Pawn_Promotion(Element):
	def __init__(self, parent, color, my_board):
		pygame.sprite.Sprite.__init__(self, self.containers)
		
		self.space_height = my_board.space_height
		
		self.dimensions()
		self.inner_dimensions()
	
		outer_w = parent.screen_h * self.w_percent / 100
		outer_h = parent.screen_h * self.h_percent / 100
		outer_x = (parent.screen_h - outer_w) / 2 + parent.edge_dist
		outer_y = (parent.screen_h - outer_h) / 2
		
		self.start_x = outer_x
		self.start_y = outer_y
		
		self.rect = pygame.Rect(outer_x, outer_y, outer_w, outer_h)
		
		outer = pygame.Surface((outer_w, outer_h))
		outer.fill((0, 0, 0))
		
		self.inner_w = parent.screen_h * self.inner_w_percent / 100
		self.inner_h = parent.screen_h * self.inner_h_percent / 100
		
		inner = pygame.Surface((self.inner_w, self.inner_h))
		inner.fill((255, 255, 255))
		
		self.inner_x = (outer_w - self.inner_w) / 2
		self.inner_y = (outer_h - self.inner_h) / 2
		
		outer.blit(inner, (self.inner_x, self.inner_y))
		
		self.piece_selection = ["R", "N", "B", "Q"]
		
		self.image = outer
		self.load_images(color)
		
	def get_image(self, index):
		return pygame.transform.scale(self.images[index], (int(self.space_height), int(self.space_height)))
		
	def select_promotion(self, mouse):
		start_x = self.start_x + self.inner_x
		start_y = self.start_y + self.inner_y
		
		mouse_x = mouse.pos[0]
		mouse_y = mouse.pos[1]
		
		if self.clicked(mouse):
			space = self.inner_w / 4
			for i in range(1, 5):
				if mouse_x < (start_x + (space * i)):
					#print(str(self.piece_selection[i-1]))
					return self.piece_selection[i-1]
		else:	
			return False
	
	def clicked(self, mouse):
		if mouse == False:
			return mouse
		
		mouse_x = mouse.pos[0]
		mouse_y = mouse.pos[1]
		
		start_x = self.start_x + self.inner_x
		start_y = self.start_y + self.inner_y
		
		return (mouse_x > start_x and mouse_x < (start_x + self.inner_w) and mouse_y > start_y and mouse_y < (start_y + self.inner_h))
		
	def load_images(self, color):
		self.images = pieces.Piece.images
		
		if color == "bl":
			offset = 6
		else: offset = 0
		
		rook = self.get_image(1 + offset)
		knight = self.get_image(2 + offset)
		bishop = self.get_image(3 + offset)
		queen = self.get_image(5 + offset)
		
		piece_images = [rook, knight, bishop, queen]
		
		space = self.inner_w / 4
		for i in range(0, 4):
			self.image.blit(piece_images[i], (self.inner_x + (space * i), self.inner_y))
		
	def dimensions(self):
		self.w_percent = 52.5
		self.h_percent = 15
		
	def inner_dimensions(self):
		self.inner_w_percent = 50
		self.inner_h_percent = 12.5
		
