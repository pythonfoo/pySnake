from __future__ import print_function
try:
	import pygame_sdl2 as pygame
except ImportError:
	print("pygame_sdl2 not found; falling back to pygame.")
	import pygame
import time


class popUp(object):
	def __init__(self, screen):
		self._screen = screen
		self.fnt = pygame.font.SysFont("MS Comic Sans", 30)
		self.color = (245, 101, 44)  # orange ;)
		self.popUps = []
		self.defaultDuration = 3

	def singlePopUp(self, txt, duration=0):
		if duration == 0:
			duration = self.defaultDuration
		self.popUps = []
		self.popUps.append({"txt": txt, "start": time.time(), "duration": duration})

	def addPopUp(self, txt, duration=0):
		if duration == 0:
			duration = self.defaultDuration
		self.popUps.append({"txt": txt, "start": time.time(), "duration": duration})

	def drawPopUps(self):
		if len(self.popUps) == 0:
			return False

		fullText = ""
		for i in range(len(self.popUps)):
			if time.time() > self.popUps[i]['start'] + self.popUps[i]['duration']:
				self.popUps.pop(i)
				break

		for popUp in self.popUps:
			fullText += popUp['txt'] + " "

		# TODO: multilines!
		# http://stackoverflow.com/questions/2770886/pygames-message-multiple-lines
		if fullText != "":
			xPos = (self._screen.get_width() / 2)
			self._screen.blit(self.fnt.render(fullText, 1, self.color), (xPos - (self.fnt.size(fullText)[0] / 2), 5))

		return True
