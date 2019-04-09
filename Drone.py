#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tango
from tango.server import Device, command, attribute, run

# Tango Device Server class that provides attributes and commands for a generic drone
class Drone(Device):

	# device initialization
	def init_device(self):
		super(Drone, self).init_device()
		self.set_state(tango.DevState.OFF)
		self._direction = 'North'

	# direction towards which the drone is aimed
	@attribute(dtype='str')
	def direction(self):
		return self._direction

	# set the State to ON
	@command
	def TurnOn(self):
		if self.dev_state() == tango.DevState.OFF:
			self.set_state(tango.DevState.ON)
		else:
			pass

	# set the State to OFF
	@command
	def TurnOff(self):
		if self.dev_state() == tango.DevState.ON:
			self.set_state(tango.DevState.OFF)
		else:
			pass

	# set the State to OPEN
	@command
	def TakeOff(self):
		if self.dev_state() != tango.DevState.ON:
			pass
		else:
			self.set_state(tango.DevState.OPEN)

	# set the State to CLOSE
	@command
	def Land(self):
		if self.dev_state() != tango.DevState.STANDBY:
			pass
		else:
			self.set_state(tango.DevState.CLOSE)

	# set the State to MOVING
	@command
	def Forward(self):
		if self.dev_state() != tango.DevState.STANDBY:
			pass
		else:
			self.set_state(tango.DevState.MOVING)

	# set the State to STANDBY
	@command
	def Stop(self):
		if self.dev_state() == tango.DevState.MOVING or self.dev_state() == tango.DevState.OPEN:
			self.set_state(tango.DevState.STANDBY)
		else:
			pass

	# turn the direction to the right
	@command
	def TurnRight(self):
		if self.dev_state() == tango.DevState.STANDBY or self.dev_state() == tango.DevState.MOVING:
			if self._direction == 'North':
				self._direction = 'East'
			elif self._direction == 'East':
				self._direction = 'South'
			elif self._direction == 'West':
				self._direction = 'North'
			elif self._direction == 'South':
				self._direction = 'West'
			else:
				self.set_state(tango.DevState.FAULT)
		else:
			pass

	# turn the direction to the left
	@command
	def TurnLeft(self):
		if self.dev_state() == tango.DevState.STANDBY or self.dev_state() == tango.DevState.MOVING:
			if self._direction == 'North':
				self._direction = 'West'
			elif self._direction == 'East':
				self._direction = 'North'
			elif self._direction == 'West':
				self._direction = 'South'
			elif self._direction == 'South':
				self._direction = 'East'
			else:
				self.set_state(tango.DevState.FAULT)
		else:
			pass

if __name__ == "__main__":
	run([Drone])
