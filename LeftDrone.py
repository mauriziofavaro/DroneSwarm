#!/usr/bin/env python
# -*- coding:utf-8 -*-

from Drone import Drone
import tango
from tango.server import attribute, command, device_property, run
from tango import DeviceProxy, AttrWriteType

# Tango Device Server class that represents the member on the left of the drone swarm
class LeftDrone(Drone):

	# device property that contains the name of the camera equipped on the drone
	camera_address = device_property(dtype='str', default_value='sim/test/cam')

	# store the previous state of the device to restore it when needed
	prev_state = tango.DevState.STANDBY

	# device initialization
	def init_device(self):
		super(LeftDrone, self).init_device()
		self._X = -1
		self._Y = -1
		self._Z = 0
		self._leader_X = 0
		self._leader_Y = 0
		self._leader_Z = 0
		self._Pictures = 0
		self.camera = DeviceProxy(self.camera_address)

	@attribute(dtype='int')
	def X(self):
		if self.dev_state() == tango.DevState.MOVING and self._direction == 'East':
			self._X += 1
		elif self.dev_state() == tango.DevState.MOVING and self._direction == 'West':
			self._X -= 1
		else:
			pass
		return self._X

	@attribute(dtype='int')
	def Y(self):
		if self.dev_state() == tango.DevState.MOVING and self._direction == 'North':
			self._Y += 1
		elif self.dev_state() == tango.DevState.MOVING and self._direction == 'South':
			self._Y -= 1
		else:
			pass
		return self._Y

	@attribute(dtype='int')
	def Z(self):
		if self.dev_state() == tango.DevState.RUNNING:
			self.fix_formation()
		elif self.dev_state() == tango.DevState.OPEN:
			self._Z += 1
		elif self._Z == 0 and self.dev_state() == tango.DevState.CLOSE:
			self.set_state(tango.DevState.ON)
		elif self._Z > 0 and self.dev_state() == tango.DevState.CLOSE:
			self._Z -= 1
		else:
			pass
		return self._Z

	# leader_X, leader_Y and leader_Z are the writable attributes that contain the
	# position of the leader. They are together with their read and write methods
	leader_X = attribute(dtype=int, access=AttrWriteType.READ_WRITE)

	def read_leader_X(self):
		return self._leader_X

	def write_leader_X(self, ld_X):
		self._leader_X = ld_X

	leader_Y = attribute(dtype=int, access=AttrWriteType.READ_WRITE)

	def read_leader_Y(self):
		return self._leader_Y

	def write_leader_Y(self, ld_Y):
		self._leader_Y = ld_Y

	leader_Z = attribute(dtype=int, access=AttrWriteType.READ_WRITE)

	def read_leader_Z(self):
		return self._leader_Z

	def write_leader_Z(self, ld_Z):
		self._leader_Z = ld_Z

	@attribute(dtype='int')
	def Pictures(self):
		camera_pictures_attr = self.camera.read_attribute('Pictures')
		self._Pictures = camera_pictures_attr.value
		return self._Pictures

	# attribute that shows a string that interprets the state of the camera
	@attribute(dtype='str')
	def Camera_State(self):
		camera_state = self.camera.state()
		if camera_state == tango.DevState.OFF:
			self._Camera_State = 'OFF'
		elif camera_state == tango.DevState.ON:
			self._Camera_State = 'READY'
		elif camera_state == tango.DevState.ALARM:
			self._Camera_State = 'MEMORY FULL'
		else:
			self._Camera_State = 'ERROR'
		return self._Camera_State

	# method that checks and fixes the position of this drone in the formation of the swarm
	def fix_formation(self):
		leader_Z = self.read_leader_Z()
		leader_X = self.read_leader_X()
		leader_Y = self.read_leader_Y()
		if self._Z != leader_Z:
			self.fix_Z()
		elif (self._direction == 'North' or self._direction == 'East') and (self._X != leader_X-1):
			self.fix_X()
		elif (self._direction == 'West' or self._direction == 'South') and (self._X != leader_X+1):
			self.fix_X()
		elif (self._direction == 'North' or self._direction == 'West') and (self._Y != leader_Y-1):
			self.fix_Y()
		elif (self._direction == 'East' or self._direction == 'South') and (self._Y != leader_Y+1):
			self.fix_Y()
		else:
			self.set_state(tango.DevState.STANDBY)

	def fix_X(self):
		leader_X = self.read_leader_X()
		if self._direction == 'North' or self._direction == 'East':
			if self._X > leader_X-1:
				self._X -= 1
			elif self._X < leader_X-1:
				self._X += 1
			else:
				pass
		elif self._direction == 'West' or self._direction == 'South':
			if self._X > leader_X+1:
				self._X -= 1
			elif self._X < leader_X+1:
				self._X += 1
			else:
				pass
		else:
			self.set_state(tango.DevState.FAULT)

	def fix_Y(self):
		leader_Y = self.read_leader_Y()
		if self._direction == 'North' or self._direction == 'West':
			if self._Y > leader_Y-1:
				self._Y -= 1
			elif self._Y < leader_Y-1:
				self._Y += 1
			else:
				pass
		elif self._direction == 'East' or self._direction == 'South':
			if self._Y > leader_Y+1:
				self._Y -= 1
			elif self._Y < leader_Y+1:
				self._Y += 1
			else:
				pass
		else:
			self.set_state(tango.DevState.FAULT)

	def fix_Z(self):
		leader_Z = self.read_leader_Z()
		if self._Z > leader_Z:
			self._Z -= 1
		elif self._Z < leader_Z:
			self._Z += 1
		else:
			pass

	@command
	def TurnOn(self):
		super(LeftDrone, self).TurnOn()
		if self.dev_state() == tango.DevState.ON:
			self.camera.command_inout('TurnOn')
		else:
			pass

	@command
	def TurnOff(self):
		super(LeftDrone, self).TurnOff()
		if self.dev_state() == tango.DevState.OFF:
			self.camera.command_inout('TurnOff')
		else:
			pass

	@command
	def Stop(self):
		if self.dev_state() == tango.DevState.MOVING or self.dev_state() == tango.DevState.OPEN:
			self.prev_state = tango.DevState.STANDBY
			self.set_state(tango.DevState.RUNNING)
		else:
			pass

	@command
	def TurnRight(self):
		super(LeftDrone, self).TurnRight()
		self.prev_state = self.dev_state()
		self.set_state(tango.DevState.RUNNING)

	@command
	def TurnLeft(self):
		super(LeftDrone, self).TurnLeft()
		self.prev_state = self.dev_state()
		self.set_state(tango.DevState.RUNNING)

	# restore the previous state
	@command
	def Restore(self):
		self.set_state(self.prev_state)

	@command
	def TakePicture(self):
		if self.dev_state() != tango.DevState.OFF:
			self.camera.command_inout('TakePicture')

if __name__ == "__main__":
	run([LeftDrone])
