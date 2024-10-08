import os
import sys
import random
import pygame

import conf
from Ui import Ui
from Joystick import Joystick
from PopUp import PopUp
from TouchScreen import TouchScreen
from Box import Box


class game(object):
	def __init__(self):
		self.screen = None
		self.playerBox = None
		self.ui = None
		self.iUi = None
		self.popUp = None
		self.touchScreen = None

		# Game parameters
		self.SCREEN_WIDTH = conf.SCREEN_WIDTH
		self.SCREEN_HEIGHT = conf.SCREEN_HEIGHT
		self.DRAW_RECT = None  # must be set after pygame initialisation
		self.BG_COLOR = conf.BG_COLOR
		self.BLOCKSIZE = conf.BLOCKSIZE
		self.SNACKS = conf.SNACKS
		self.REST_WITH = self.SCREEN_WIDTH % self.BLOCKSIZE
		self.REST_HEIGHT = self.SCREEN_HEIGHT % self.BLOCKSIZE

		self.gameSpeed = 250
		self.gameSpeedFactors = range(0, 400, 25)
		self.gameSpeedFactor = 0

		self.joystickInteract = None  # must be set after pygame initialisation
		self.elements = []
		self.haveToAdd = []

		
	def move(self, direction):
		if self.playerBox is not None:
			curDir = self.playerBox.getDirection()
			# DONT move backwards!
			if (curDir == 1 and direction == 3) or (curDir == 3 and direction == 1):
				pass
			elif (curDir == 2 and direction == 4) or (curDir == 4 and direction == 2):
				pass			
			else:
				self.playerBox.setDirection(direction)

	def getLastElement(self):
		tmp = self.playerBox
		found = False
		while found is False:
			if tmp.back is None:
				found = True
			else:
				tmp = tmp.back
		return tmp
	
	def getBodyLen(self):
		tmp = self.playerBox
		cnt = 0

		while tmp is not None:
			tmp = tmp.back
			cnt += 1

		return cnt
	
	def fieldContainsBox(self, x, y):
		for elem in self.elements:
			if elem.x == x and elem.y == y:
				return True

		return False
		
	def addSnack(self, elements):
		snackCount = 0
		coords = []
		for elem in elements:
			coords.append([elem.x, elem.y])
			if elem.bType == 'snack':
				snackCount += 1
		
		#print 'snackCount', snackCount
		if snackCount < self.SNACKS:
			xy = [
				random.randint(1, (self.SCREEN_WIDTH / self.BLOCKSIZE)-1),
				random.randint(1, (self.SCREEN_HEIGHT / self.BLOCKSIZE)-1)
			]

			if not xy in coords:
				snack = Box(self.screen, self.BLOCKSIZE, xy[0], xy[1])
				snack.bType = 'snack'
				snack.color = conf.SNACK_COLOR
				snack.direction = 0
				elements.append(snack)
			
	def eatSnack(self, elements):
		for elem in elements:
			if elem.bType == 'snack' and elem.x == self.playerBox.x and elem.y == self.playerBox.y:
				elements.remove(elem)
				return self.playerBox.x, self.playerBox.y

		return None

	def headDied(self, elements):
		dead = False
		# collision with myself or stuff
		for elem in elements:
			if elem.bType != 'head' and elem.bType != 'snack' and elem.bType:
				if self.playerBox.x == elem.x and self.playerBox.y == elem.y:
					dead = True
		
		# border collision
		if self.playerBox.x < 0 or self.playerBox.y < 0 \
			or self.playerBox.x > (self.SCREEN_WIDTH / self.BLOCKSIZE)-1 \
			or self.playerBox.y > (self.SCREEN_HEIGHT / self.BLOCKSIZE)-1:
			dead = True
			
		if dead:
			highscores = '0'
			scores = self.getBodyLen()

			if os.path.isfile("highscore.txt") is True:
				f = open("highscore.txt", 'r')
				highscores = f.read()
				f.close()
				
			if scores > int(highscores):
				highscores = str(scores)
				f = open("highscore.txt", 'w')
				f.write(highscores)
				f.close()

			self.iUi.addSimpleMenu("gameOver",
				[
					"GAME OVER", "POINTS: " + str(scores), "HIGHSCORE "+highscores,
					"Button / Keyboard: 2 = Speed Up",
					"Button / Keyboard: 1 = Speed Down",
					"R = restart / respawn",
					"Q = Quit / Exit"
				],
				color=conf.FONT_COLOR
			)

			self.iUi.draw("gameOver")

		return dead

	def resetGame(self):
		self.screen.fill((0, 0, 0))
		self.playerBox = Box(self.screen, self.BLOCKSIZE, 3, 3)
		self.playerBox.bType = 'head'
		
		self.elements = []
		self.elements.append(self.playerBox)
		
		self.haveToAdd = [[3, 3], [3, 3], [3, 3]]

	def gameSpeedUp(self):
		self.gameSpeedFactor += 1
		if self.gameSpeedFactor >= len(self.gameSpeedFactors):
			self.gameSpeedFactor -= 1
		self.speedChanged()
			
	def gameSpeedDown(self):
		self.gameSpeedFactor -= 1
		if self.gameSpeedFactor < 0:
			self.gameSpeedFactor = 0
		self.speedChanged()

	def speedChanged(self):
		oneBased = self.gameSpeedFactor + 1
		txt = "|" * oneBased
		txt = "[" + txt.ljust(len(self.gameSpeedFactors)) + "]"

		self.popUp.singlePopUp(txt)

	def run_game(self):
		pygame.init()
		self.DRAW_RECT = pygame.Rect(0, 0, self.SCREEN_WIDTH - self.REST_WITH, self.SCREEN_HEIGHT - self.REST_HEIGHT)

		# do fancy window stuff
		pygame.display.set_caption("pySnake")
		pygame.mouse.set_visible(False)

		if not conf.FULLSCREEN:
			os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (conf.WINDOW_POSITION_X, conf.WINDOW_POSITION_Y)
			if not conf.WINDOW_BORDER:
				self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.NOFRAME, 32)

		if self.screen is None:
			self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 0, 32)

		if conf.FULLSCREEN:
			pygame.display.toggle_fullscreen()

		clock = pygame.time.Clock()
		redrawCount = 0
		
		# init the menu, add stuff later
		self.iUi = Ui(self.screen)
		self.popUp = PopUp(self.screen)
		self.popUp.color = conf.FONT_COLOR
		self.touchScreen = TouchScreen(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
		
		pygame.joystick.init()
		self.joystickInteract = Joystick()

		keymap = {
			pygame.K_UP: 1,
			pygame.K_RIGHT: 2,
			pygame.K_DOWN: 3,
			pygame.K_LEFT: 4
		}

		self.playerBox = None
		self.elements = []
		self.haveToAdd = []

		# The main game loop
		gameOver = False
		doMove = -1
		while True:
			if self.playerBox is None:
				self.resetGame()
			
			# Limit frame speed to 50 FPS
			time_passed = clock.tick(50)
			redrawCount += time_passed

			if self.joystickInteract.joystickAvailable():
				self.joystickInteract.processAxis()
				joyAction = self.joystickInteract.getAction()

				if joyAction == "move":
					doMove = self.joystickInteract.getMoveAction()
				elif joyAction == "speedUp":
					self.gameSpeedUp()
				elif joyAction == "speedDown":
					self.gameSpeedDown()
				elif joyAction == "restart":
					self.resetGame()
					gameOver = False
				elif joyAction == 'quit':
					self.exit_game()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.exit_game()
				elif event.type == pygame.KEYDOWN:
					if event.key in keymap:
						doMove = keymap[event.key]
					elif event.key == pygame.K_2:  # speed up game
						self.gameSpeedUp()
					elif event.key == pygame.K_1:  # slow down up game
						self.gameSpeedDown()
					elif event.key == pygame.K_r:  # restart game
						self.resetGame()
						gameOver = False
					elif event.key == pygame.K_q:
						self.exit_game()
					else:
						print("event.key:", event.key)

				else:
					pass
					#print event

			if conf.TOUCH_SCREEN:
				mouseAction = self.touchScreen.getEventBoxes()
				if mouseAction and mouseAction > 0:
					if gameOver:
						self.resetGame()
						gameOver = False
					else:
						doMove = mouseAction

			if gameOver is False and redrawCount >= (self.gameSpeed - self.gameSpeedFactors[self.gameSpeedFactor]):
				# ONLY move, when the timer elapses!
				# otherwise you could change the direction multiple times before the scenery changes and updates
				# strange shit goes on!
				if doMove != -1:
					self.move(doMove)
					doMove = -1
					
				redrawCount = 0

				self.screen.fill(self.BG_COLOR, self.DRAW_RECT)
				
				# move the elements
				for elem in reversed(self.elements):
					elem.update()
				
				# add elements BEFORE blit is called and they change direction!
				# WEIRD stuff would happen otherwise!!!1!!!!!!!!
				if len(self.haveToAdd) > 0:
					for i in range(len(self.haveToAdd)):
						coords = self.haveToAdd[i]
						if self.fieldContainsBox(coords[0], coords[1]) is False:
							lastElem = self.getLastElement()
							lastElem.back = Box(self.screen, self.BLOCKSIZE, coords[0], coords[1])
							lastElem.back.setDirection(lastElem.getDirection())
							self.elements.append(self.getLastElement())
							self.haveToAdd.pop(i)
							break
				else:
					# if there is NOTHING to add to the Snake, add a new snack, if needed
					# preventing from spawning a snack inside the "new" tail of the snake and shit
					self.addSnack(self.elements)
				
				# update elements
				for elem in reversed(self.elements):
					elem.blit()

				# draw touchscreen
				# TODO: draw touch areas

				# draw popups
				self.popUp.drawPopUps()

				# if a snack has been eaten, add it to the to add list
				snackEaten = self.eatSnack(self.elements)
				if snackEaten is not None:
					self.haveToAdd.append(snackEaten)
					self.popUp.singlePopUp(str(self.getBodyLen()))
				
				# collision!
				if self.headDied(self.elements):
					gameOver = True

				pygame.display.flip()

	def exit_game(self):
		sys.exit()
