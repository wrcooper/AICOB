import pygame

class UI(pygame.sprite.Sprite):
	def __init__(self, screen_info, game, image):
		pygame.sprite.Sprite.__init__(self, self.containers)
		
		self.buttons = []
		
		self.screen_w = screen_info.current_w
		self.screen_h = screen_info.current_h
		
		# dimensions for ui
		screen_offset = (self.screen_w - self.screen_h) / 2
		edge_dist = screen_offset / 10 
		
		self.start_x = (2 * edge_dist) + self.screen_h
		self.end_x = self.screen_w - edge_dist
		self.rect_w = self.end_x - self.start_x
		print("rect_w = " + str(self.rect_w) + " start_x = " + str(self.start_x))
		
		self.top_button_border = (self.screen_h * 3) / 100
		self.left_button_border = (self.rect_w * 3) / 100
		
		self.rect = pygame.Rect(self.start_x, 0, self.rect_w, self.screen_h)

		s = pygame.Surface((self.rect_w, self.screen_h))
		s.blit(image, (0,0), (0, 0, self.rect_w, self.screen_h))

		self.image = s
		
		self.game = game
		self.update_game_info(self.game)

	def clicked(self, click):
		if (click.pos[0] > self.start_x and click.pos[0] < self.end_x and click.pos[1] > 0):	
			for button in self.buttons:
				button.clicked(click)
				
	def update_game_info(self, game):
		self.current_move = game.current_move
		self.turn_number = game.turn_number
		self.player_color = game.player_color
		self.pgn = game.pgn
				
	def init_game_interface(self):
		self.turn_number = Turn_Number(self)
		self.to_move = To_Move(self)
		self.player_button = Player_Button(self)
		self.player_color = Player_Color(self)
		self.new_game_button = New_Game_Button(self)
		self.settings = Settings(self)
		self.pgn = PGN(self)
		self.chat = Chat(self)
		
		self.buttons = [self.turn_number, self.to_move, self.player_button, self.player_color, 
			self.new_game_button, self.settings, self.pgn, self.chat]
	
	def update_interface(self):
		for button in self.buttons:
			button.kill()
		self.update_game_info(self.game)
		self.init_game_interface()
		
	def init_settings_interface(self):
		print("blah")
		
	def init_ai_interface(self):
		print("blee")
		
	def color_to_str(color):
		if color == "wh":
			return "White"
		else:
			return "Black"
		

class Button(pygame.sprite.Sprite):
	def __init__(self, parent):
		pygame.sprite.Sprite.__init__(self, self.containers)
		
		centered = False
		self.dimensions()
		self.centered()
		
		self.width = int((self.w_percent * parent.rect_w) / 100)
		self.height = int((self.h_percent * parent.screen_h) / 100)
		
		
		if (self.centered):	
			x = parent.start_x + int((parent.rect_w - self.width)/2)
		else:
			x = (self.x_percent * parent.rect_w)/100 + parent.start_x + parent.left_button_border
			
		y = parent.top_button_border + (self.y_percent * parent.screen_h)/100
		
		self.rect = pygame.Rect(x, y, self.width, self.height)
		
		s = pygame.Surface((self.width, self.height))
		s.fill((255,255,255))
		
		self.image = s
	
	def dimensions(self):
		self.w_percent = 0
		self.h_percent = 0
		self.x_percent = 0
		self.y_percent = 0
		
	def centered(self):
		self.centered = False
	
	def onClick(self):
		self.click_function()
	
	def click_function(self):
		print("Error: uninitialized button")
		

	
class Turn_Number(Button):
	def __init__(self, parent):
		Button.__init__(self, parent)
		font = pygame.font.Font(None, 50)
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
		
class To_Move(Button):
	def __init__(self, parent):
		Button.__init__(self, parent)
		font = pygame.font.Font(None, 50)
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
		
class Player_Button(Button):
	def __init__(self, parent):
		Button.__init__(self, parent)
		font = pygame.font.Font(None, 50)
		text = "Player: player"
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
		
class Player_Color(Button):
	def __init__(self, parent):
		Button.__init__(self, parent)
		font = pygame.font.Font(None, 50)
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
				
class New_Game_Button(Button):
	def __init__(self, parent):
		Button.__init__(self, parent)
		font = pygame.font.Font(None, 60)
		text = "New Game"
		s = font.render(text, True, (0, 0, 0))
		
		size = font.size(text)
		left_border = (self.width - size[0])/2
		top_border = (self.height - size[1])/2		
		
		self.image.blit(s, (left_border, top_border))
	
	def dimensions(self):
		self.w_percent = 94
		self.h_percent = 6.5
		self.x_percent = 0
		self.y_percent = 16.5
		
	def centered(self):
		self.centered = True
				
class Settings(Button):
	def __init__(self, parent):
		Button.__init__(self, parent)
		font = pygame.font.Font(None, 60)
		text = "Settings"
		s = font.render(text, True, (0, 0, 0))
		
		size = font.size(text)
		left_border = (self.width - size[0])/2
		top_border = (self.height - size[1])/2		
		
		self.image.blit(s, (left_border, top_border))
	
	def dimensions(self):
		self.w_percent = 94
		self.h_percent = 6.5
		self.x_percent = 0
		self.y_percent = 24.5
		
	def centered(self):
		self.centered = True
		
class PGN(Button):
	def __init__(self, parent):
		Button.__init__(self, parent)
		font = pygame.font.Font(None, 40)
		text = "PGN: " + parent.pgn
		
		words = text.split(' ')
		line = ""
		i = 0
		left_border = 0
		top_border = 0	
		
		for word in words:
			if font.size(line + word)[0] > self.width - 5:
				s = font.render(line, True, (0, 0, 0))
				self.image.blit(s, (left_border + 5, top_border + 5 + (i * 35) ))
				line = ""
				i += 1
			line += word + " "
		s = font.render(line, True, (0, 0, 0))
		self.image.blit(s, (left_border + 5, top_border + 5 + (i * 35) ))
	
	def dimensions(self):
		self.w_percent = 94
		self.h_percent = 20
		self.x_percent = 0
		self.y_percent = 33
		
	def centered(self):
		self.centered = True
		
class Chat(Button):
	def __init__(self, parent):
		Button.__init__(self, parent)
		font = pygame.font.Font(None, 40)
		text = "Chat"
		s = font.render(text, True, (0, 0, 0))
		
		size = font.size(text)
		left_border = 0
		top_border = 0	
		
		self.image.blit(s, (left_border, top_border))
	
	def dimensions(self):
		self.w_percent = 94
		self.h_percent = 40
		self.x_percent = 0
		self.y_percent = 55
		
	def centered(self):
		self.centered = True
