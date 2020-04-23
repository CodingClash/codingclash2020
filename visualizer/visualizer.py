import pygame
import sys
from pygame.locals import *
import random
import time
from copy import deepcopy

white = (255, 255, 255)
black = (0,0,0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
bg = (134, 161, 110)

tank_r = pygame.image.load("tank_r.png")
gunner_r = pygame.image.load("gunner_r.png")
hq_r = pygame.image.load("hq_r.png")

tank_b = pygame.image.load("tank_b.png")
gunner_b = pygame.image.load("gunner_b.png")
hq_b = pygame.image.load("hq_b.png")


class Visualizer:
	def __init__(self, s = 40, t1 = "", t2 = ""):
		pygame.init()
		self.size = s
		self.DISPLAYSURF = pygame.display.set_mode((s*20, s*20))
		pygame.display.set_caption("Coding Clash!")

		self.piece_to_col = {"rg":gunner_r, "rt": tank_r, "rh":hq_r, "bg":gunner_b, "bt": tank_b, "bh":hq_b}
		
		self.t1 = t1
		self.t2 = t2

	def playback(self, filename):
		with open(filename, "r") as file:
			boards = file.readlines()
		boards = [i[1:].strip() for i in boards if i[0]=="#"]
		boards = [[t[i:i+2] for i in range(0, len(t), 2)] for t in boards]
		#print(boards)
		boards = [[j[x*self.size:(x+1)*self.size] for x in range(self.size)] for j in boards]
		#print(boards)
		self.play(boards)
	
	def update(self, board):
		#print(board)
		self.DISPLAYSURF.fill(bg)
		for row in range(len(board)):
			for col in range(len(board)):
				if board[row][col]=="nn":
					continue
				else:
					#print(board[row][col])
					self.DISPLAYSURF.blit(self.piece_to_col[board[row][col]], (20*row, 20*col))
	
	#def string_to_board(self, string):
	#	Eh no need

	def board_to_string(self, board):
		bout = [j for sub in board for j in sub]
		return "#"+"".join(bout)

	def save(self, board_states):
		#print(board_states)
		with open(str(id(self))+".txt", "w+") as file:
			file.write("\n".join(["|blue: "+self.t1, "|red: "+self.t2]+[self.board_to_string(b) for b in board_states]))


	def play(self, board_states):
		x = 0
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
			if x<len(board_states):
				print("ok")
				self.update(board_states[x])
			time.sleep(1)
			x+=1
			pygame.display.update()
	
	def view(self, board):
		self.update(board)
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
			pygame.display.update()

	def gen_random(self, t = 5):
		board = [["nn" for i in range(self.size)] for j in range(self.size)]
		hqlocks = [(5, 5), (4, 5), (3, 5), (5, 4), (4, 4), (3, 4), (5, 3), (4, 3), (3, 3)]
		for (r, c) in hqlocks: board[r][c] = "rh"
		for (r, c) in hqlocks: board[self.size-r][self.size-c] = "bh"
		out = []
		#board[5][5] = "rh"
		#board[35][35] = "bh"

		for i in range(100):
			x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
			if board[x][y]=="nn":
				board[x][y]=random.choice(list(set(self.piece_to_col.keys()).difference({"rh", "bh"})))

		out.append(deepcopy(board))
		for _ in range(t):
			moved_to = set()
			for r in range(self.size):
				for c in range(self.size):
					if (r, c) in moved_to: continue
					elif board[r][c][0]=="r":
						if r+1<self.size and board[r+1][c]=="nn" and board[r][c][1]!="h":
							board[r+1][c]=board[r][c]
							moved_to.add((r+1, c))
							board[r][c]="nn"

					elif board[r][c][0]=="b":
						if r-1>=0 and board[r-1][c]=="nn" and board[r][c][1]!="h":
							board[r-1][c]=board[r][c]
							moved_to.add((r-1, c))
							board[r][c]="nn"
			out.append(deepcopy(board))

		return out

#v = Visualizer()
#print(id(v))
#v.view(v.gen_random())
#v.save(v.gen_random())
#v.playback("58879920.txt")

