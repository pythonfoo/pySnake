from __future__ import print_function

try:
	import pygame_sdl2 as pygame
except ImportError:
	print("pygame_sdl2 not found; falling back to pygame.")
	import pygame


class touchScreen(object):
	def __init__(self, width, height):
		self.width = width
		self.height = height

		one4width = self.width / 4
		one4height = self.height / 4

		self.regions = []
		self.regions.append(pygame.Rect(one4width, 0, self.width / 2, one4height))  # top
		self.regions.append(pygame.Rect(one4width * 3, one4height,  one4width, self.height / 2))  # right
		self.regions.append(pygame.Rect(one4width, one4height * 3,  self.width / 2, one4height))  # down
		self.regions.append(pygame.Rect(0, one4height,  one4width, self.height / 2))  # left

	def getEventBoxes(self):
		for i in range(len(self.regions)):
			mPosX, mPosY = pygame.mouse.get_pos()
			if pygame.mouse.get_pressed()[0] and self.regions[i].collidepoint(mPosX, mPosY):
				return i + 1

		return -1
