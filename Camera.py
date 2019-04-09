#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tango
from tango.server import Device, command, attribute, run

# Tango Device Server class that represents a camera
class Camera(Device):

	# device initialization
	def init_device(self):
		super(Camera, self).init_device()
		self.set_state(tango.DevState.OFF)
		self._Pictures = 0
		self._Available = 500

	# pictures taken
	@attribute(dtype='int')
	def Pictures(self):
		return self._Pictures

	# number of pictures that can be taken to fill the memory
	@attribute(dtype='int')
	def Available(self):
		if self.dev_state() == tango.DevState.ON and self._Available == 0:
			self.set_state(tango.DevState.ALARM)
		return self._Available

	@command
	def TurnOn(self):
		if self.dev_state() == tango.DevState.OFF:
			self.set_state(tango.DevState.ON)
		else:
			pass

	@command
	def TurnOff(self):
		if self.dev_state() == tango.DevState.ON or self.dev_state() == tango.DevState.ALARM:
			self.set_state(tango.DevState.OFF)
		else:
			pass

	# take a picture
	@command
	def TakePicture(self):
		if self.dev_state() == tango.DevState.ON:
			self._Pictures += 1
			self._Available -= 1
		else:
			pass

if __name__ == "__main__":
	run([Camera])
