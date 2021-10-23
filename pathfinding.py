'''
Visual A* Pathfinding Project
By: Bhargav Datta Maturi
8/6/21
'''

import pygame
import math
from queue import PriorityQueue

DIMENSION = 1000

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE= (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

window = pygame.display.set_mode((DIMENSION, DIMENSION))
pygame.display.set_caption("Visual A* Pathfinding")

class Node:
	def __init__(self, row, column, dimension, total_rows):
		self.row = row
		self.column = column
		self.x = row * dimension
		self.y = column * dimension
		self.color = WHITE
		self.neighbors = []
		self.dimension = dimension
		self.total_rows = total_rows

	def get_position(self):
		return self.row, self.column

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == YELLOW

	def is_obstacle(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == GREEN

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = YELLOW

	def make_obstacle(self):
		self.color = BLACK

	def make_start(self):
		self.color = GREEN

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, window):
		pygame.draw.rect(window, self.color, (self.x,self.y, self.dimension, self.dimension))

	def update_neighbors(self, grid):
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.column].is_obstacle(): #DOWN
			self.neighbors.append(grid[self.row + 1][self.column])

		if self.row > 0 and not grid[self.row - 1][self.column].is_obstacle(): #UP
			self.neighbors.append(grid[self.row - 1][self.column])

		if self.column < self.total_rows - 1 and not grid[self.row][self.column + 1].is_obstacle(): #RIGHT
			self.neighbors.append(grid[self.row][self.column + 1])

		if self.column > 0 and not grid[self.row][self.column - 1].is_obstacle(): #LEFT
			self.neighbors.append(grid[self.row][self.column - 1])

	def __lt__(self, other):
		return False

def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x2 - x1) + abs(y2 - y1)

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {node: float("inf") for row in grid for node in row}
	g_score[start] = 0
	f_score = {node: float("inf") for row in grid for node in row}
	f_score[start] = h(start.get_position(), end.get_position())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			start.make_start()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_position(), end.get_position())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

def make_grid(rows, dimensions):
	grid = []
	gap = dimensions // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			new_node = Node(i, j, gap, rows)
			grid[i].append(new_node)

	return grid

def draw_grid(window, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(window, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(window, GREY, (j * gap, 0), (j * gap, width))

def draw(window, grid, rows, dimensions):
	window.fill(WHITE)

	for row in grid:
		for node in row:
			node.draw(window)

	draw_grid(window, rows, dimensions)
	pygame.display.update()

def get_clicked_pos(pos, rows, dimensions):
	gap = dimensions // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None 
	end = None 
	run = True 
	done = False

	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0] and not done: 
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				node = grid[row][col]
				if not start and node!= end:
					start = node
					node.make_start()
				elif not end and node != start:
					end = node
					node.make_end()
				elif node!= end and node!= start:
					node.make_obstacle()

			elif pygame.mouse.get_pressed()[2] and not done:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				node = grid[row][col]
				node.reset()

				if node == start:
					start = None
				elif node == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end and not done:
					for row in grid:
						for node in row:
							node.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
					done = True

				if event.key == pygame.K_c:
					start = None
					end = None
					done = False
					grid = make_grid(ROWS, width)

	pygame.quit()

main(window, DIMENSION)