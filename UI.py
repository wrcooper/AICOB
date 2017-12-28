import pygame, pieces

class UI(pygame.sprite.Sprite):
	def __init__(self, screen_info, game, image):
		pygame.sprite.Sprite.__init__(self, self.containers)
		
		self.elements = []
		
		self.screen_w = screen_info.current_w
		self.screen_h = screen_info.current_h
		
		# dimensions for ui
		self.screen_offset = (self.screen_w - self.screen_h) / 2
		self.edge_dist = self.screen_offset / 10 
		
		self.start_x = (2 * self.edge_dist) + self.screen_h
		self.end_x = self.screen_w - self.edge_dist
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
		
	"""
	def clicked(self, click):
		if (click.pos[0] > self.start_x and click.pos[0] < self.end_x and click.pos[1] > 0):	
			for element in self.elements:
				element.clicked(click)
	"""			

	def update_game_info(self, game):
		self.current_move = game.current_move
		self.turn_number = game.turn_number
		self.player_color = game.player_color
		self.pgn = game.pgn
				
	def init_game_interface(self):
		self.turn_number = Turn_Number(self)
		self.to_move = To_Move(self)
		self.player_name = Player_Name(self)
		self.player_color = Player_Color(self)
		self.new_game_button = New_Game_Button(self)
		self.settings = Settings(self)
		self.pgn = PGN(self)
		self.chat = Chat(self)
		
		self.elements = [self.turn_number, self.to_move, self.player_name, self.player_color, 
			self.new_game_button, self.settings, self.pgn, self.chat]
			
	def update_interface(self):
		for element in self.elements:
			element.kill()
		self.update_game_info(self.game)
		self.init_game_interface()
		
	def open_pawn_promotion(self, color, my_board):
		self.pawn_prom = Pawn_Promotion(self, color, my_board)
		self.elements.append(self.pawn_prom)
		
	def init_settings_interface(self):
		print("blah")
		
	def init_ai_interface(self):
		print("blee")
		
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
		print("Error: uninitialized element")
		

	
class Turn_Number(Element):
	def __init__(self, parent):
		Element.__init__(self, parent)
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
		
class To_Move(Element):
	def __init__(self, parent):
		Element.__init__(self, parent)
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
		
class Player_Name(Element):
	def __init__(self, parent):
		Element.__init__(self, parent)
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
		
class Player_Color(Element):
	def __init__(self, parent):
		Element.__init__(self, parent)
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
				
class New_Game_Button(Element):
	def __init__(self, parent):
		Element.__init__(self, parent)
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
				
class Settings(Element):
	def __init__(self, parent):
		Element.__init__(self, parent)
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
		
class PGN(Element):
	def __init__(self, parent):
		Element.__init__(self, parent)
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
		
class Chat(Element):
	def __init__(self, parent):
		Element.__init__(self, parent)
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
					print(str(self.piece_selection[i-1]))
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
		
