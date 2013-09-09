import pygame

class joystick(object):
	def __init__(self):
		self.joystick_names = []
		self.doMove = -1
		self.joyButtonDown = False
		self.myJoystick = None

		# Enumerate joysticks
		for i in range(0, pygame.joystick.get_count()):
			self.joystick_names.append(pygame.joystick.Joystick(i).get_name())

		# By default, load the first available joystick.
		if (len(self.joystick_names) > 0):
			self.myJoystick = pygame.joystick.Joystick(0)
			self.myJoystick.init()

	def joystickAvailable(self):
		if self.myJoystick != None:
			return True
		else:
			return False

	def haveAction(self):
		if self.myJoystick != None:
			try:
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
					self.doMove = 2
				elif self.myJoystick.get_axis(xAx) < 0:
					self.doMove = 4
				elif  self.myJoystick.get_axis(yAx) > 0:
					self.doMove = 3
				elif  self.myJoystick.get_axis(yAx) < 0:
					self.doMove = 1

				if self.myJoystick.get_button(0) and self.joyButtonDown == False: # speed up
					return "speedUp"
				elif self.myJoystick.get_button(1) and self.joyButtonDown == False: # speed down
					return "speedDown"
				elif (self.myJoystick.get_button(9) and self.joyButtonDown == False)\
					or (self.myJoystick.get_button(3) and self.joyButtonDown == False): # (re)start
					return "restart"
				else:
					# make sure NO button is down for reset
					someJoyButtonDown = False
					for i in range(0, self.myJoystick.get_numbuttons()):
						if (self.myJoystick.get_button(i)):
							someJoyButtonDown = True
					self.joyButtonDown = someJoyButtonDown

				if self.doMove != -1:
					return "move"
			except Exception as ex:
				print('JOYSTICK ERROR, DEACTIVATING:' + str(ex))
				self.myJoystick = None

		return ""

	def getMoveAction(self):
		tmp = self.doMove
		if self.doMove != -1:
			self.doMove = -1
		return tmp
