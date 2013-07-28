#!/usr/bin/env python


import os
import sys
import random
import pygame
from ui import ui
from pygame.sprite import Sprite

#sys.stdout = os.devnull
#sys.stderr = os.devnull

class box(object):
	def __init__(self, screen, blockSize, x, y, bType = 'body'):
		self.screen = screen
		self.blockSize = blockSize
		self.direction = 2
		self.bType = bType
		self.x = x
		self.y = y
		self.color = (245, 101, 44)
		self.back = None
		self.directionChanged = 0
	
	def getDirection(self):
		return self.direction
	
	def setDirection(self, direction):
		#self.directionChanged = 1
		self.direction = direction
		
	def update(self):
		if self.direction == 1:
			self.y = self.y -1
		elif self.direction == 2:
			self.x = self.x +1
		elif self.direction == 3:
			self.y = self.y +1
		elif self.direction == 4:
			self.x = self.x -1

		#if self.back != None:
		#	self.back.setDirection(self.direction)

	def blit(self):
		relX = self.x * self.blockSize
		relY = self.y * self.blockSize
		pygame.draw.rect(self.screen, self.color, (relX, relY,  self.blockSize, self.blockSize) )
		if self.back != None:
			self.back.setDirection(self.direction)

class game(object):
	def __init__(self):
		self.screen = None
		self.playerBox = None
		self.ui = None
		

	def move(self, direction):
		#print 'direction:', direction
		if self.playerBox != None:
			curDir = self.playerBox.getDirection()
			# DONT move backwards!
			if (curDir == 1 and direction == 3) or (curDir == 3 and direction == 1):
				pass
			elif (curDir == 2 and direction == 4) or (curDir == 4 and direction == 2) :
				pass			
			else:
				self.playerBox.setDirection(direction)

	def getLastElement(self):
		tmp = self.playerBox
		found = False
		while found == False:
			if tmp.back == None:
				found = True
			else:
				tmp = tmp.back
		return tmp
	
	def getBodyLen(self):
		tmp = self.playerBox
		cnt = 0
		while tmp != None:
			tmp = tmp.back
			cnt += 1
		return cnt
	
	def fieldContainsBox(self, elements, x, y):
		for elem in elements:
			if elem.x == x and elem.y == y:
				return True
		return False
		
	def addSnack(self, elements):
		snackCount = 0
		coords = []
		for elem in elements:
			coords.append([ elem.x, elem.y ])
			if elem.bType == 'snack':
				snackCount += 1
		
		#print 'snackCount', snackCount
		if snackCount < self.SNACKS:
			xy = [random.randint(1, (self.SCREEN_WIDTH / self.BLOCKSIZE)-1), random.randint(1, (self.SCREEN_HEIGHT / self.BLOCKSIZE-1))]
			if not xy in coords:
				snack = box(self.screen, self.BLOCKSIZE, xy[0], xy[1])
				snack.bType = 'snack'
				snack.color = (99, 255, 99)
				snack.direction = 0
				elements.append(snack)
			
	def eatSnack(self, elements):
		for elem in elements:
			if elem.bType == 'snack' and elem.x == self.playerBox.x and elem.y == self.playerBox.y:
				elements.remove(elem)
				return (self.playerBox.x, self.playerBox.y)
		return None

	def headDied(self, elements):
		dead = False
		# collision with myself or stuff
		for elem in elements:
			if elem.bType != 'head' and elem.bType != 'snack' and elem.bType:
				if self.playerBox.x == elem.x and self.playerBox.y == elem.y:
					dead = True
		
		# border collision
		if self.playerBox.x < 0 or self.playerBox.y < 0 or self.playerBox.x > (self.SCREEN_WIDTH / self.BLOCKSIZE)-1 or self.playerBox.y > (self.SCREEN_HEIGHT / self.BLOCKSIZE)-1:
			dead = True
			
		if dead == True:
			highscores = '0'
			scores = self.getBodyLen()
			if os.path.isfile("highscore.txt") == True:
				f = open("highscore.txt", 'r')
				highscores = f.read()
				f.close()
				
			if scores > int(highscores):
				highscores = str(scores)
				f = open("highscore.txt", 'w')
				f.write(highscores)
				f.close()
			
			
			self.iUi.addSimpleMenu("gameOver", ["GAME OVER", "POINTS: " + str(scores), "HIGHSCORE "+highscores, "Button / Keyboard: 1 = Speed Up", "Button / Keyboard: 2 = Speed Down", "R = restart / respawn", "Q = Quit / Exit"])
			self.iUi.draw("gameOver")

		return dead

	def resetGame(self):
		self.playerBox = box(self.screen, self.BLOCKSIZE, 3, 3)
		self.playerBox.bType = 'head'
		
		self.elements = []
		self.elements.append(self.playerBox)
		
		self.haveToAdd = [[3, 3], [3, 3], [3, 3]]

	def gameSpeedUp(self):
		self.gameSpeedFactor += 1
		if self.gameSpeedFactor >= len(self.gameSpeedFactors):
			self.gameSpeedFactor -= 1
			
	def gameSpeedDown(self):
		self.gameSpeedFactor -= 1
		if self.gameSpeedFactor < 0:
			self.gameSpeedFactor = 0

	def run_game(self):
		# Game parameters
		self.SCREEN_WIDTH = 1024
		self.SCREEN_HEIGHT = 600
		BG_COLOR = (8, 13, 41)
		ORANGE = (245, 101, 44)
		self.BLOCKSIZE = 10
		self.SNACKS = 10
		self.gameSpeed = 250
		self.gameSpeedFactors = range(0, 300, 25)
		self.gameSpeedFactor = 0
		pygame.init()
		
		# do fancy window stuff
		pygame.display.set_caption("pySnake")
		#pygame.display.set_icon(pygame.image.load('imgs/bandit.jpg'))
		pygame.mouse.set_visible(False)
		
		self.screen = pygame.display.set_mode( (self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 0, 32)
		#TODO: make it optional
		#pygame.display.toggle_fullscreen()
		clock = pygame.time.Clock()
		redrawCount = 0
		
		# init the menu, add stuff later
		self.iUi = ui(self.screen)
		
		pygame.joystick.init()
		self.myJoystick = None
		self.joystick_names = []

		# Enumerate joysticks
		for i in range(0, pygame.joystick.get_count()):
			self.joystick_names.append(pygame.joystick.Joystick(i).get_name())

		# By default, load the first available joystick.
		if (len(self.joystick_names) > 0):
			self.myJoystick = pygame.joystick.Joystick(0)
			self.myJoystick.init()
		
		keymap = {pygame.K_UP:1, pygame.K_RIGHT:2, pygame.K_DOWN:3, pygame.K_LEFT:4}

		
		self.playerBox = None
		self.elements = []
		self.haveToAdd = []

		
		# The main game loop
		#
		gameOver = False
		doMove = -1
		joyButtonDown = False
		while True:
			if self.playerBox == None:
				self.resetGame()
			
			# Limit frame speed to 50 FPS
			#
			time_passed = clock.tick(50)
			redrawCount += time_passed
			worldChanged = False
			
			if self.myJoystick != None:
				xAx = 0
				yAx = 0
				# sometimes 2 axis, sometimes 6, wtf?!
				if self.myJoystick.get_numaxes() == 2:
					xAx = 0
					yAx = 1
				else:
					xAx = 3
					yAx = 4
				if self.myJoystick.get_axis(xAx) > 0:
					doMove = 2
				elif self.myJoystick.get_axis(xAx) < 0:
					doMove = 4
				elif  self.myJoystick.get_axis(yAx) > 0:
					doMove = 3
				elif  self.myJoystick.get_axis(yAx) < 0:
					doMove = 1
				
				if self.myJoystick.get_button(0) and joyButtonDown == False: # speed up
					joyButtonDown = True
					self.gameSpeedUp()
				elif self.myJoystick.get_button(1) and joyButtonDown == False: # speed down
					joyButtonDown = True
					self.gameSpeedDown()
				elif self.myJoystick.get_button(9) and joyButtonDown == False: # (re)start
					joyButtonDown = True
					self.resetGame()
					gameOver = False
				else:
					# make shure NO button is down for reset
					someJoyButtonDown = False
					for i in range(0, self.myJoystick.get_numbuttons()):
						if (self.myJoystick.get_button(i)):
							someJoyButtonDown = True
					joyButtonDown = someJoyButtonDown
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.exit_game()

				elif event.type == pygame.KEYDOWN:
					if event.key in keymap:
						doMove = keymap[event.key]
					elif event.key == pygame.K_1: # speed up game
						self.gameSpeedUp()
					elif event.key == pygame.K_2: # slow down up game
						self.gameSpeedDown()
					elif event.key == pygame.K_r: # restart game
						self.resetGame()
						gameOver = False
					elif event.key == pygame.K_q:
						self.exit_game()
					else:
						print event.key
					#if event.key == pygame.K_UP:
					#	self.move(1)
				else:
					pass
					#print event
			
			if gameOver == False and  redrawCount >= (self.gameSpeed - self.gameSpeedFactors[self.gameSpeedFactor]): #or worldChanged == True:
				# ONLY move, when the timer elapses!
				# otherwise you could change the direction multiple times before the scenery changes and upates
				# strange shit goes on!
				if doMove != -1:
					self.move(doMove)
					doMove = -1
					
				redrawCount = 0
				self.screen.fill(BG_COLOR)
				
				# move the elements
				for elem in reversed(self.elements):
					elem.update()
				
				# add elements BEVORE blit is called and they change direction!
				# WEIRD stuff would happen otherwise!!!1!!!!!!!!
				if len(self.haveToAdd) > 0:
					for i in range(len(self.haveToAdd)):
						coords = self.haveToAdd[i]
						if self.fieldContainsBox(self.elements, coords[0], coords[1]) == False:
							lastElem = self.getLastElement()
							lastElem.back = box(self.screen, self.BLOCKSIZE, coords[0], coords[1])
							lastElem.back.setDirection(lastElem.getDirection())
							self.elements.append(self.getLastElement())
							self.haveToAdd.pop(i)
							break
				else:
					# if theres NOTHING to add to the Snake, add a new snak, if needed
					# preventing from spawning a snack inside the "new" tail of the snake and shit
					self.addSnack(self.elements)
				
				# update elements
				for elem in reversed(self.elements):
					elem.blit()

				# if a snak has been eaten, add it to the to add list
				snackEaten = self.eatSnack(self.elements)
				if snackEaten != None:
					self.haveToAdd.append(snackEaten)
				
				# collision!
				if self.headDied(self.elements) == True:
					gameOver = True
				
				pygame.display.flip()

				
	def exit_game(self):
		sys.exit()
		
		
snk = game()
snk.run_game()
