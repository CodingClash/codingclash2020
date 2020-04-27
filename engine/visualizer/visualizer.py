import os
import pygame
import sys
from pygame.locals import *
import random
import time
from ..game import constants as GameConstants

white = (255, 255, 255)
black = (0,0,0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
bg = (134, 161, 110)
FRAME_SIZE = 600

assets_folder = "engine/visualizer/assets/images/"
#assets_folder = "assets/images/"

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 25)

class Visualizer:
	def __init__(self, t1 = "", t2 = ""):
		pygame.init()
		self.size = GameConstants.BOARD_WIDTH
		self.block_size = 15
		self.DISPLAYSURF = pygame.display.set_mode((self.size * self.block_size, self.size * self.block_size))
		self.clock = pygame.time.Clock()
		pygame.display.set_caption("Coding Clash!")

		self.piece_to_img = {"G": self.load_image("gunner_r.png"),
		                     "T": self.load_image("tank_r.png"),
							 "H": self.load_image("hq_r.png"),
							 "g": self.load_image("gunner_b.png"),
							 "t": self.load_image("tank_b.png"),
							 "h": self.load_image("hq_b.png")}

		self.spawnables = ["G", "T", "g", "t"]
		self.piece_to_team = {"G": "r", "T": "r", "H": "r", "g": "b", "t": "b", "h": "b", "n": None}

		self.t1 = t1
		self.t2 = t2


	def load_image(self, img_name):
		return pygame.transform.scale(pygame.image.load(assets_folder + img_name), (self.block_size, self.block_size))


	def playback(self, filename):
		with open(filename, "r") as file:
			boards = file.readlines()
		boards = [i[1:].strip() for i in boards if i[0]=="#"]
		boards = [[board[x*self.size:(x+1)*self.size] for x in range(self.size)] for board in boards]
		self.play(boards)
	

	def update(self, board):
		self.DISPLAYSURF.fill(bg)
		for row in range(len(board)):
			for col in range(len(board)):
				if board[row][col] not in self.piece_to_img.keys():
					continue
				self.DISPLAYSURF.blit(self.piece_to_img[board[row][col]], (self.block_size*row, self.block_size*col))


	def copy(self, board):
		return [row.copy() for row in board]


	def play(self, board_states, delay=0.5):
		for board in board_states:
			if type(board)==str: continue
			self.update(board)
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					return
					#sys.exit()
			pygame.display.update()
			self.clock.tick(1 / delay)
		# Pause on the last frame
		while True:
			self.view(board)

	
	def view(self, board, delay=0.5):
		self.update(board)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		pygame.display.update()
		self.clock.tick(1 / delay)


	def gen_random(self, t=5):
		# CAPITALIZED MEANS RED TEAM, LOWERCASE MEANS BLUE TEAM
		board = [["n" for i in range(self.size)] for j in range(self.size)]
		hqlocs = [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)]
		for (r, c) in hqlocs:
			board[r][c] = "H"
			board[self.size-r][self.size-c] = "h"

		for i in range(100):
			x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
			if board[x][y]=="n":
				board[x][y]=random.choice(self.spawnables)

		out = []
		out.append(self.copy(board))
		for _ in range(t):
			moved_to = set()
			for r in range(self.size):
				for c in range(self.size):
					if (r, c) in moved_to: continue
					if board[r][c] in ["h", "H"]: continue
					elif self.piece_to_team[board[r][c]] == "r":
						if r + 1 < self.size and board[r+1][c] == "n":
							board[r+1][c] = board[r][c]
							moved_to.add((r+1, c))
							board[r][c] = "n"

					elif self.piece_to_team[board[r][c]] == "b":
						if r - 1 >= 0 and board[r-1][c] == "n":
							board[r-1][c]=board[r][c]
							moved_to.add((r-1, c))
							board[r][c] = "n"

			out.append(self.copy(board))

		return out

#v = Visualizer()
#print(id(v))
#v.play(v.gen_random())
#v.save(v.gen_random())
#v.playback("58879920.txt")
