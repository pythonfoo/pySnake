import pygame


class Joystick(object):
	def __init__(self):
		self.joystick_names = []
		self.doMove = -1
		self.joyButtonDown = False
		self.myJoystick = None

		# Enumerate joysticks
		for i in range(0, pygame.joystick.get_count()):
			self.joystick_names.append(pygame.joystick.Joystick(i).get_name())

		# By default, load the first available joystick.
		if len(self.joystick_names) > 0:
			self.myJoystick = pygame.joystick.Joystick(0)
			self.myJoystick.init()

	def joystickAvailable(self):
		if self.myJoystick is not None:
			return True
		else:
			return False

	def getAction(self):
		action = ""

		if self.myJoystick is None:
			return action

		try:
			buttonCount = self.myJoystick.get_numbuttons()

			if self.myJoystick.get_button(0) and self.joyButtonDown is False:  # speed up
				action = "speedUp"
			elif self.myJoystick.get_button(1) and self.joyButtonDown is False:  # speed down
				action = "speedDown"
			elif (buttonCount > 9 and self.myJoystick.get_button(9) and self.joyButtonDown is False)\
				or (buttonCount > 3 and  self.myJoystick.get_button(3) and self.joyButtonDown is False):  # (re)start
				action = "restart"
			elif buttonCount > 8 and self.myJoystick.get_button(8) and self.joyButtonDown is False:
				action = 'quit'

			# make sure NO button is down for reset
			someJoyButtonDown = False
			for i in range(0, self.myJoystick.get_numbuttons()):
				if self.myJoystick.get_button(i):
					someJoyButtonDown = True
			self.joyButtonDown = someJoyButtonDown

			if self.doMove != -1 and not action:
				action = "move"

		except Exception as ex:
			print('JOYSTICK ERROR, DEACTIVATING:' + str(ex))
			self.myJoystick = None

		return action

	def processAxis(self):
		if self.myJoystick is None:
			return

		try:
			xAx = 0
			yAx = 0

			# sometimes 2 axis, sometimes 6, wtf?! (X-Box controller)
			if self.myJoystick.get_numaxes() == 2:
				xAx = 0
				yAx = 1
			elif self.myJoystick.get_numaxes() == 3:
				xAx = 0
				yAx = 1
			else:
				xAx = 3
				yAx = 4

			if self.myJoystick.get_axis(xAx) > 0:
				self.doMove = 2
			elif self.myJoystick.get_axis(xAx) < 0:
				self.doMove = 4
			elif self.myJoystick.get_axis(yAx) > 0:
				self.doMove = 3
			elif self.myJoystick.get_axis(yAx) < 0:
				self.doMove = 1

		except Exception as ex:
			print('JOYSTICK ERROR, DEACTIVATING:' + str(ex))
			self.myJoystick = None

	def getMoveAction(self):
		tmp = self.doMove
		if self.doMove != -1:
			self.doMove = -1
		return tmp
