#!/usr/bin/env python

# notes:
# The Ten Commandments Of Video Game Menus http://kotaku.com/5955855/the-ten-commandments-of-video-game-menus

import pygame
import sys

class ui(object):
	def __init__(self, screen):
		
		# the main screen, result from:
		# pygame.display.set_mode(...)
		self._screen = screen
		self.keymap = {pygame.K_UP:1, pygame.K_RIGHT:2, pygame.K_DOWN:3, pygame.K_LEFT:4}
		
		self.nextAction = None
		
		self.menus = {}
		
	def interaction(self, eventKey):
		canInteract = False
		
		if eventKey in self.keymap:
			canInteract = True
			nextAction = self.keymap[eventKey]
		else:
			# reset the action if multiple times pressed keys before
			# actually did something
			self.nextAction = None
			
		return canInteract
	
	def addMenu(self, menuKey, menuRows):
		''' add an menu
		menuKey: unique name of the menu
		menueRows: [
					{"rowName":"title", "selectable":False, "font":"MS Comic Sans", "fontSize":30, "color":(0,0,255), "text":"UserInterfaceGenerator"},
					{"rowName":"start", "selectable":True, "font":"MS Comic Sans", "fontSize":30, "color":(0,0,255), "text":"Start Game"},
					{"rowName":"q", "selectable":True, "font":"MS Comic Sans", "fontSize":30, "color":(123,55,255), "text":"QUIT"}
					]
		'''
		self.menus[menuKey] = menuRows

	def addSimpleMenu(self, menuKey, menuRows, font="MS Comic Sans", size=30, color=(245, 101, 44)):
		''' add an SIMPLE menu
		menuKey: unique name of the menu
		menueRows: ["You Shall", "NOT PASS"]
		'''
		menu = []
		rowCount = 0
		for row in menuRows:
			menu.append({"rowName":"simple_" + str(rowCount), "selectable":False, "font":font, "fontSize":size, "color":color, "text":row})
		
		self.menus[menuKey] = menu
	
	def draw(self, menuKey):
		if menuKey in self.menus:
			menuToDraw = self.menus[menuKey]
			
			#print fnt.size(resultText)
			menuRowsCount = len(menuToDraw)
			for i in range(menuRowsCount):
				fontSize = menuToDraw[i]["fontSize"]
				fnt = pygame.font.SysFont(menuToDraw[i]["font"] , fontSize)
				xPos = (self._screen.get_width() / 2)
				yPos = (self._screen.get_height() / 30) * menuRowsCount
				txt = menuToDraw[i]["text"]
				self._screen.blit(fnt.render(txt, 1, menuToDraw[i]["color"]), ( xPos - (fnt.size(txt)[0] / 2), yPos +(i * fontSize)))
		else:
			raise Exception("Error menu '"+ menuKey +"' does not exist")
		
if __name__ == "__main__":
	pygame.init()
	screen = pygame.display.set_mode( (1024, 768), 0, 32)
	clock = pygame.time.Clock()
	
	BG_COLOR = (8, 13, 41)
	
	iUi = ui(screen)
	iUi.addMenu("main", [
						{"rowName":"title", "selectable":False, "font":"MS Comic Sans", "fontSize":30, "color":(0,0,255), "text":"UserInterfaceGenerator"},
						{"rowName":"start", "selectable":True, "font":"MS Comic Sans", "fontSize":30, "color":(0,0,255), "text":"Start Game"},
						{"rowName":"q", "selectable":True, "font":"MS Comic Sans", "fontSize":30, "color":(123,55,255), "text":"QUIT"}
						]
				)
	
	while True:	
		# Limit frame speed to 50 FPS
		time_passed = clock.tick(50)
		screen.fill(BG_COLOR)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			elif event.type == pygame.KEYDOWN:
				if iUi.interaction(event.key):
					print "UI catched this key"
				else:
					print "no UI catch, key pressed:", event.key
					
					if event.key == pygame.K_q:
						sys.exit(0)
						
		iUi.draw("main")
		
		pygame.display.flip()
