#!/usr/bin/env python

# notes:
# The Ten Commandments Of Video Game Menus http://kotaku.com/5955855/the-ten-commandments-of-video-game-menus

import pygame
import sys


class Ui(object):
	def __init__(self, screen):
		
		# the main screen, result from:
		# pygame.display.set_mode(...)
		self._screen = screen
		self.keymap = {pygame.K_UP: 1, pygame.K_RIGHT: 2, pygame.K_DOWN: 3, pygame.K_LEFT: 4}  # pygame.K_RETURN:5}
		self.selectedColor = (245, 101, 44)  # orange ;)
		self.nextAction = None
		
		self.menus = {}

		self._selectedMenu = ''  # menu 'name'
		self._selectedMenuItem = ''  # selected index
		self._selectedMenuItemIndex = -1  # selected index
		
	def interaction(self, eventKey):
		canInteract = False
		
		if eventKey in self.keymap:
			canInteract = True
			self.nextAction = self.keymap[eventKey]
			if self.nextAction == 1:  # UP
				self.selectMenuItem(-1)
			elif self.nextAction == 3:  # DOWN
				self.selectMenuItem(1)
			elif self.nextAction == 5:  # SELECTED
				pass
		else:
			# reset the action if multiple times pressed keys before
			# actually did something
			self.nextAction = None
			
		return canInteract
	
	def addMenu(self, menuKey, menuRows):
		""" add a menu
		@menuKey: unique name of the menu
		@menuRows: [
			{"rowName":"title", "selectable":False, "font":"MS Comic Sans", "fontSize":30, "color":(0,0,255), "text":"UserInterfaceGenerator"},
			{"rowName":"start", "selectable":True, "font":"MS Comic Sans", "fontSize":30, "color":(0,0,255), "text":"Start Game"},
			{"rowName":"q", "selectable":True, "font":"MS Comic Sans", "fontSize":30, "color":(123,55,255), "text":"QUIT"}
		]
		"""
		self.menus[menuKey] = menuRows

	def addSimpleMenu(self, menuKey, menuRows, font="MS Comic Sans", size=30, color=(245, 101, 44)):
		""" add an SIMPLE menu
			@menuKey: unique name of the menu
			@menuRows: ["You Shall", "NOT PASS"]
		"""
		menu = []
		rowCount = 0
		for row in menuRows:
			menu.append(
				{
					"rowName": "simple_" + str(rowCount),
					"selectable": False,
					"font": font,
					"fontSize": size,
					"color": color,
					"text": row
				}
			)
		
		self.menus[menuKey] = menu

	def __getAvailableIndexes(self):
		indexList = []
		if self._selectedMenu in self.menus:
			for i in range(len(self.menus[self._selectedMenu])):
				if self.menus[self._selectedMenu][i]['selectable']:
					indexList.append(i)
		return indexList

	def selectMenuItem(self, direction=0):
		""" select the menu item
			@direction: +1 (down) or -1 (up), 0 for the first selectable item in the current menu
		"""
		#self._selectedIndex

		indexList = self.__getAvailableIndexes()
		if len(indexList) == 0:
			print('NO SELECTABLE MENU ITEMS')
			return -1

		if self._selectedMenu in self.menus and direction == 0:
			self._selectedMenuItemIndex = indexList[0]
			self._selectedMenuItem = self.menus[self._selectedMenu][indexList[0]]
		else:
			currentIndex = 0
			if self._selectedMenuItemIndex in indexList:
				currentIndex = indexList.index(self._selectedMenuItemIndex)
			nextIndex = currentIndex + direction

			# allow top-down / down-top switching
			if nextIndex >= len(indexList):  # last element of list!
				self._selectedMenuItemIndex = indexList[0]
				self._selectedMenuItem = self.menus[self._selectedMenu][self._selectedMenuItemIndex]
			elif nextIndex < 0:
				self._selectedMenuItemIndex = indexList[-1]  # last element of list!
				self._selectedMenuItem = self.menus[self._selectedMenu][self._selectedMenuItemIndex]
			else:
				self._selectedMenuItemIndex = indexList[nextIndex]
				self._selectedMenuItem = self.menus[self._selectedMenu][self._selectedMenuItemIndex]

		return self._selectedMenuItem

	def getSelectedItem(self):
		if self._selectedMenu in self.menus and self._selectedMenuItemIndex >= 0:
			return self.menus[self._selectedMenu][self._selectedMenuItemIndex]

		print("WARNING! NO SELECTED MENU ITEM FOUND!")
		return None

	def draw(self, menuKey=''):
		if menuKey in self.menus:
			self._selectedMenu = menuKey
		elif menuKey == '':
			if self._selectedMenu == '' and 'main' in self.menus:
				self._selectedMenu = 'main'
		else:
			raise Exception("Error menu '" + menuKey + "' does not exist and there is no 'main' menu")

		menuToDraw = self.menus[self._selectedMenu]

		if self._selectedMenuItemIndex == -1:
			self.selectMenuItem(0)

		if menuToDraw is not None:
			#print fnt.size(resultText)
			menuRowsCount = len(menuToDraw)
			for i in range(menuRowsCount):
				fontSize = menuToDraw[i]["fontSize"]
				fnt = pygame.font.SysFont(menuToDraw[i]["font"], fontSize)
				xPos = (self._screen.get_width() / 2)
				yPos = (self._screen.get_height() / 30) * menuRowsCount
				txt = menuToDraw[i]["text"]

				color = menuToDraw[i]["color"]
				if i == self._selectedMenuItemIndex:
					color = self.selectedColor

				self._screen.blit(fnt.render(txt, True, color), (xPos - (fnt.size(txt)[0] / 2), yPos + (i * fontSize)))
		else:
			raise Exception("Error menu '" + menuKey + "' does not exist")
		
if __name__ == "__main__":
	pygame.init()
	screen = pygame.display.set_mode((1024, 768), 0, 32)
	clock = pygame.time.Clock()
	
	BG_COLOR = (8, 13, 41)
	
	iUi = Ui(screen)
	iUi.addMenu("main",
		[
			{"rowName":"title", "selectable":False, "font":"MS Comic Sans", "fontSize":30, "color":(0,0,255), "text":"UserInterfaceGenerator"},
			{"rowName":"start", "selectable":True, "font":"MS Comic Sans", "fontSize":30, "color":(0,0,255), "text":"Start Game"},
			{"rowName":"info",  "selectable":True, "font":"MS Comic Sans", "fontSize":30, "color":(123,55,255), "text":"1NF0$"},
			{"rowName":"q",     "selectable":True, "font":"MS Comic Sans", "fontSize":30, "color":(123,55,255), "text":"QUIT"},
			{"rowName":"notes", "selectable":False, "font":"MS Comic Sans", "fontSize":30, "color":(123,55,255), "text":"sometext"},
		]
	)
	
	while True:	
		# Limit frame rate to 60 FPS
		time_passed = clock.tick(60)
		screen.fill(BG_COLOR)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			elif event.type == pygame.KEYDOWN:
				if iUi.interaction(event.key):
					print("UI catched this key:", event.key)
				else:
					print("no UI catch, key pressed:", event.key)
					if pygame.K_RETURN == event.key:
						print("selected item:", iUi.getSelectedItem())
					
					if event.key == pygame.K_q:
						sys.exit(0)
						
		iUi.draw("main")
		
		pygame.display.flip()
