import sys
import time
import itertools
import pygame
from pygame.locals import *
from pygame import Color


pygame.init()
DISPLAYSURF = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Langton's Ant")
fpsClock = pygame.time.Clock()

text16 = pygame.font.Font("freesansbold.ttf", 16)
text18 = pygame.font.Font("freesansbold.ttf", 18)
text24 = pygame.font.Font("freesansbold.ttf", 24)
text32 = pygame.font.Font("freesansbold.ttf", 32)
				
class Cell(object):
	def __init__(self, size, state_colors, state_map, leftx, topy):
		self.size = size
		self.state_colors = state_colors
		self.states = itertools.cycle(state_colors)
		self.state_map = state_map
		self.state = next(self.states)
		self.rect = pygame.Rect(leftx, topy, size, size)
		
	def update_state(self, surface):
		self.state = next(self.states)
		pygame.draw.rect(surface, Color(self.state), self.rect)


class Ant(object):
	right_directs = {"up": "right", 
				"down": "left",
				"left": "up",
				"right": "down"}
	left_directs = {"up": "left",
				"down": "right",
				"left": "down",
				"right": "up"}
	
	def __init__(self, size, color, starting_direction):
		self.size = size
		self.color = color
		self.direction = starting_direction
	
	def change_direction(self, surface, cells, blit_cells):
		for cell in cells:
			if self.rect.center == cell.rect.center:
				if cell.state_map[cell.state] == "L":
					self.direction = self.left_directs[self.direction]
				elif cell.state_map[cell.state] == "R":
					self.direction = self.right_directs[self.direction]
				cell.update_state(surface)
				blit_cells.append(cell)
				break
				
				
	def move(self):
		if self.direction == "up":
			self.rect.centery -= self.size
		elif self.direction == "down":
			self.rect.centery += self.size
		elif self.direction == "left":
			self.rect.centerx -= self.size
		elif self.direction == "right":
			self.rect.centerx += self.size

def setup(surface, screen_width, screen_height, frame_rate):
	color_scheme = "monochrome"
	rule_string = "LR"
	start_direct = "up"
	mode = "normal"
	cell_size = 5
	tail_length = 250
	title_text = text32.render("Langton's Ant", True, Color("blue"))
	title_rect = title_text.get_rect(midtop = (screen_width/2, 10))
	while True:
		cell_text = text24.render("Cell Size: {0}".format(cell_size), True, Color("white"))
		cell_rect = cell_text.get_rect(topleft = (50, title_rect.bottom + 20))
		add5_text = text18.render(" + 5 ", True, Color("blue"), Color("lightgray"))
		add5_rect = add5_text.get_rect(topleft = (50, cell_rect.bottom + 20))
		sub5_text = text18.render(" - 5 ", True, Color("blue"), Color("lightgray"))
		sub5_rect = sub5_text.get_rect(topleft = (add5_rect.right + 20, add5_rect.top))
		scheme_text = text24.render("Color Scheme: {0}".format(color_scheme.capitalize()), True, Color("white"))
		scheme_rect = scheme_text.get_rect(topleft = (50, sub5_rect.bottom + 20))
		cool_text = text18.render("Cool", True, Color("blue"), Color("lightgray"))
		cool_rect = cool_text.get_rect(topleft = (50, scheme_rect.bottom + 20))
		warm_text = text18.render("Warm", True, Color("blue"), Color("lightgray"))
		warm_rect = warm_text.get_rect(topleft = ( cool_rect.right + 20,cool_rect.top))
		mono_text = text18.render("Monochrome", True, Color("blue"), Color("lightgray"))
		mono_rect = mono_text.get_rect(topleft = (warm_rect.right + 20, cool_rect.top))
		rule_text = text24.render("Rule-string: {0}".format(rule_string), True, Color("white"))
		rule_rect = rule_text.get_rect(topleft = (50, mono_rect.bottom + 20))
		left_text = text18.render("Left", True, Color("blue"), Color("lightgray"))
		left_rect = left_text.get_rect(topleft = (50, rule_rect.bottom + 20))
		right_text = text18.render("Right", True, Color("blue"), Color("lightgray"))
		right_rect = right_text.get_rect(topleft = (left_rect.right + 20, left_rect.top))
		remove_text = text18.render("Delete", True, Color("blue"), Color("lightgray"))
		remove_rect = remove_text.get_rect(topleft = (right_rect.right + 20, left_rect.top))
		direct_text = text24.render("Ant Starting Direction: {0}".format(start_direct.capitalize()), True, Color("white"))
		direct_rect = direct_text.get_rect(topleft = (50, right_rect.bottom + 20))
		aup_text = text18.render("Up", True, Color("blue"), Color("lightgray"))
		aup_rect = aup_text.get_rect(topleft = (50, direct_rect.bottom + 20))
		adown_text = text18.render("Down", True, Color("blue"), Color("lightgray"))
		adown_rect = adown_text.get_rect(topleft = (aup_rect.right + 20, aup_rect.top))
		aleft_text = text18.render("Left", True, Color("blue"), Color("lightgray"))
		aleft_rect = aleft_text.get_rect(topleft = (adown_rect.right + 20, aup_rect.top))
		aright_text = text18.render("Right", True, Color("blue"), Color("lightgray"))
		aright_rect = aright_text.get_rect(topleft = (aleft_rect.right + 20, aup_rect.top))
		mode_text = text24.render("Mode: {0}   Tail Length: {1}".format(mode.capitalize(), tail_length), True, Color("white"))
		mode_rect = mode_text.get_rect(topleft = (50, aright_rect.bottom + 20))
		normal_text = text18.render("Normal", True, Color("blue"), Color("lightgray"))
		normal_rect = normal_text.get_rect(topleft = (50, mode_rect.bottom + 20))
		tail_text = text18.render("Tail", True, Color("blue"), Color("lightgray"))
		tail_rect = tail_text.get_rect(topleft = (normal_rect.right + 20, normal_rect.top))
		add_length_text = text18.render(" + Tail", True, Color("blue"), Color("lightgray"))
		add_length_rect = add_length_text.get_rect(topleft = (tail_rect.right + 100, normal_rect.top))
		sub_length_text = text18.render(" - Tail", True, Color("blue"), Color("lightgray"))
		sub_length_rect = sub_length_text.get_rect(topleft = (add_length_rect.right + 20, normal_rect.top))
		instruct1_text = text16.render("While running, use the Up and Down arrow keys to adjust", True, Color("white"))
		instruct1_rect = instruct1_text.get_rect(midtop = (screen_width/2, normal_rect.bottom + 20))
		instruct2_text = text16.render("max frame rate, SPACE to pause and 'd' to toggle drawing.", True, Color("white"))
		instruct2_rect = instruct2_text.get_rect(midtop = (screen_width/2, instruct1_rect.bottom + 10))
		done_text = text24.render("Done", True, Color("blue"), Color("lightgray"))
		done_rect = done_text.get_rect(midbottom = (screen_width/2, screen_height - 10))
		blitters = [(title_text, title_rect),(cell_text, cell_rect), (add5_text, add5_rect),
					(sub5_text, sub5_rect),(scheme_text, scheme_rect),(cool_text, cool_rect),
					(warm_text, warm_rect),(mono_text, mono_rect),(rule_text, rule_rect),
					(left_text, left_rect),(right_text, right_rect),(direct_text, direct_rect),
					(aup_text, aup_rect),(adown_text, adown_rect),(aleft_text, aleft_rect),
					(aright_text, aright_rect),(mode_text, mode_rect),(normal_text, normal_rect),
					(tail_text, tail_rect),(add_length_text, add_length_rect),
					(sub_length_text, sub_length_rect),(instruct1_text, instruct1_rect),
					(instruct2_text, instruct2_rect),(done_text, done_rect),
					(remove_text, remove_rect)]
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				x, y = event.pos
				if len(rule_string) < 12:
					if left_rect.collidepoint(x,y):
						rule_string += "L"
					elif right_rect.collidepoint(x, y):
						rule_string += "R"
				if remove_rect.collidepoint(x, y) and len(rule_string) > 0:
					rule_string = rule_string[:-1]
				if add5_rect.collidepoint(x, y):
					if cell_size < 5:
						cell_size += 1
					else:
						cell_size += 5
				elif sub5_rect.collidepoint(x, y):
					if cell_size < 6:
						cell_size -= 1
					else:
						cell_size -= 5
				elif cool_rect.collidepoint(x, y):
					color_scheme = "cool"
				elif warm_rect.collidepoint(x, y):
					color_scheme = "warm"
				elif mono_rect.collidepoint(x, y):
					color_scheme = "monochrome"
				elif aup_rect.collidepoint(x, y):
					start_direct = "up"
				elif adown_rect.collidepoint(x, y):
					start_direct = "down"
				elif aleft_rect.collidepoint(x, y):
					start_direct = "left"
				elif aright_rect.collidepoint(x, y):
					start_direct = "right"
				elif normal_rect.collidepoint(x, y):
					mode = "normal"
				elif tail_rect.collidepoint(x, y):
					mode = "tail"
				elif add_length_rect.collidepoint(x, y):
					tail_length += 25
				elif sub_length_rect.collidepoint(x, y):
					tail_length -= 25
				elif done_rect.collidepoint(x, y):
					cells = make_cells(screen_width, screen_height, cell_size, color_scheme, rule_string)
					ants = make_ants(screen_width, screen_height, cell_size, color_scheme, 1, start_direct)
					return [screen_width, screen_height, frame_rate, mode, cells, ants, tail_length, rule_string]
		
		surface.fill(Color("black"))
		for elem in blitters:
			surface.blit(elem[0], elem[1])
		pygame.display.update()
		fpsClock.tick(30)
		
		
def make_cells(screen_width, screen_height, cell_size, color_scheme, rule_string):
	if color_scheme == "cool":
		state_colors = ["black", "darkblue", "purple4", "darkgreen", "blue1",
						"purple1", "green3", "turquoise3", "royalblue3",
						"deepskyblue", "dodgerblue3", "aquamarine2"]
	elif color_scheme == "warm":
		state_colors = ["black", "red3", "orangered2", "gold", "red1",
						"darkorange", "yellow1", "chocolate3", "orangered4",
						"orangered1", "tomato3", "tomato1"]
	elif color_scheme == "monochrome":
		state_colors = ["black", "white", "gray70", "gray90", "gray20",
						"gray60",  "gray80", "gray10", "gray50", "gray30",
						"gray40", "gray5"]
	state_colors = state_colors[:len(rule_string)]	
	state_map = {}
	for n in range(len(rule_string)):
		state_map[state_colors[n]] = rule_string[n]
		
	cells = []
	x = 0
	y = 0
	for i in range(screen_height/cell_size):
		for j in range(screen_width/cell_size):
			cell = Cell(cell_size, state_colors, state_map, x, y)
			cells.append(cell)
			x += cell_size
		y += cell_size
		x = 0
	return cells

def make_ants(screen_width, screen_height, cell_size, color_scheme, num, starting_direction):
	if color_scheme == "cool" or color_scheme == "monochrome":
		ant_color = "red"
	elif color_scheme == "warm":
		ant_color = "blue"
	ants = []	
	for i in range(num):
		ant = Ant(cell_size, ant_color, starting_direction)
		ant.rect = pygame.Rect(screen_width/2, screen_height/2, ant.size, ant.size)
		ants.append(ant)
	return ants

def end_screen(surface, screen_width, screen_height):
	menu_text = text32.render("Setup Menu", True, Color("blue"), Color("lightgray"))
	menu_rect = menu_text.get_rect(midtop = (screen_width/2, 200))
	exit_text = text32.render("Exit", True, Color("blue"), Color("lightgray"))
	exit_rect = exit_text.get_rect(midtop = (screen_width/2, menu_rect.bottom + 50))
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				x, y = event.pos
				if menu_rect.collidepoint(x, y):
					return True
				elif exit_rect.collidepoint(x, y):
					pygame.quit()
					sys.exit()
		surface.fill(Color("black"))
		surface.blit(menu_text, menu_rect)
		surface.blit(exit_text, exit_rect)
		pygame.display.update()
		fpsClock.tick(30)
	
def main(surface, screen_width, screen_height, frame_rate, mode, cells, ants, tail_length, rule_string):
	for cell in cells:
		pygame.draw.rect(surface, Color(cell.state), cell.rect)
	blit_cells = []
	accelerating = False
	decelerating = False
	drawing = True
	step = 0
	while True:
		step_text = text16.render("Step: {0}".format(step), True, Color("black"), Color("lightgray"))
		step_rect = step_text.get_rect(bottomleft = (0, screen_height))
		rate = text16.render("FPS: {0}".format(frame_rate), True, Color("black"), Color("lightgray"))
		rate_rect = rate.get_rect(bottomleft = (150, screen_height))
		rule_text = text16.render(rule_string, True, Color("white"))
		rule_rect = rule_text.get_rect(topright = (screen_width - 10, rate_rect.top)) 
		start = time.time()
		for ant in ants:
			ant.change_direction(DISPLAYSURF, cells, blit_cells)
		if mode == "tail":
			if len(blit_cells) > tail_length:
				blit_cells = blit_cells[-tail_length:]
		for ant in ants:
			if ant.rect.right > screen_width or ant.rect.left < 0:
				if end_screen(surface, screen_width, screen_height):
					return
			elif ant.rect.bottom > screen_height or ant.rect.top < 0:
				if end_screen(surface, screen_width, screen_height):
					return
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_SPACE:
					paused = True
					while paused:
						for event in pygame.event.get():
							if event.type == KEYDOWN and event.key == K_SPACE:
								paused = False
				elif event.key == K_UP:
					accelerating = True
				elif event.key == K_DOWN:
					decelerating = True
				elif event.key == K_d:
					drawing = not drawing
			elif event.type == KEYUP:	
				if event.key == K_UP:
					accelerating = False
				elif event.key == K_DOWN:
					decelerating = False
		if accelerating and frame_rate < 120:
			frame_rate += 1
		if decelerating and frame_rate > 1:
			frame_rate -= 1
		if mode == "tail":
			surface.fill(Color("white"))
		else:	
			surface.fill(Color("black"))
		if drawing:
			for cell in set(blit_cells):
				pygame.draw.rect(surface, Color(cell.state), cell.rect)
		for ant in ants:
			pygame.draw.rect(surface, Color(ant.color), ant.rect)
		for ant in ants:
			ant.move()
		surface.blit(step_text, step_rect)
		surface.blit(rate, rate_rect)
		surface.blit(rule_text, rule_rect)
		x_point = rate_rect.right + 20
		y_point = rate_rect.centery   
		for color in cells[0].state_colors:
			pygame.draw.line(surface, Color(color), (x_point, y_point), (x_point + 20, y_point), 5)
			x_point += 20
		pygame.display.update()
		fpsClock.tick(frame_rate)
		step += 1
		now = time.time()
		print now - start
	
while True:		
	params = setup(DISPLAYSURF, 600, 600, 5)
	main(DISPLAYSURF, params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7])


# RLLR @ 18000 == spongebob in envelope					