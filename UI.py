import pygame

class UI(pygame.sprite.Sprite):
	def __init__(self, screen_info, image):
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
		
		self.top_button_border = (self.screen_h / 20)
		self.left_button_border = (self.rect_w / 20)
		
		self.rect = pygame.Rect(self.start_x, 0, self.rect_w, self.screen_h)

		s = pygame.Surface((self.rect_w, self.screen_h))
		s.blit(image, (0,0), (0, 0, self.rect_w, self.screen_h))

		self.image = s

	
	def clicked(self, click):
		if (click.pos[0] > self.start_x and click.pos[0] < self.end_x and click.pos[1] > 0):	
			for button in self.buttons:
				button.clicked(click)
				
	def init_buttons(self):
		new_game_button = New_Game_Button(self)

class Button(pygame.sprite.Sprite):
	def __init__(self, parent):
		pygame.sprite.Sprite.__init__(self, self.containers)
		
		centered = False
		self.dimensions()
		self.centered()
		
		width = int((self.w_percent * parent.rect_w) / 100)
		height = int((self.h_percent * parent.screen_h) / 100)
		
		if (self.centered):	
			x = parent.start_x + int((parent.rect_w - width)/2)
		else:
			x = parent.start_x + self.x + parent.left_button_border
			
		y = parent.top_button_border + self.y
		
		self.rect = pygame.Rect(x, y, width, height)
		
		s = pygame.Surface((width, height))
		s.fill((255,255,255))
		
		self.image = s
	
	def dimensions(self):
		self.w_percent = 0
		self.h_percent = 0
		self.x = 0
		self.y = 0
		
	def centered(self):
		self.centered = False
	
	def onClick(self):
		self.click_function()
	
	def click_function(self):
		print("Error: uninitialized button")
		
		
class New_Game_Button(Button):
	def dimensions(self):
		self.w_percent = 90
		self.h_percent = 10
		self.x = 0
		self.y = 0
		
	def centered(self):
		self.centered = True
	
		
		
