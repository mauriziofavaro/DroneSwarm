#!/usr/bin/env python
# -*- coding:utf-8 -*-

from Drone import Drone
import tango
from tango.server import attribute, command, device_property, run
from tango import DeviceProxy

# Tango Device Server class that represents the leader of the drone swarm
class LeaderDrone(Drone):

	# device properties that contain the names of the other drones in the swarm
	left_drone_address = device_property(dtype='str', default_value='sim/test/left')
	right_drone_address = device_property(dtype='str', default_value='sim/test/right')

	# store the previous state of the device to restore it when needed
	prev_state = tango.DevState.STANDBY

	# device initialization
	def init_device(self):
		super(LeaderDrone, self).init_device()
		self._X = 0
		self._Y = 0
		self._Z = 0
		self._Pictures = 0
		self._Videos = 0
		self.left_drone = DeviceProxy(self.left_drone_address)
		self.right_drone = DeviceProxy(self.right_drone_address)

	# position X
	@attribute(dtype='int')
	def X(self):
		if self.dev_state() == tango.DevState.MOVING and self._direction == 'East':
			self._X += 1
		elif self.dev_state() == tango.DevState.MOVING and self._direction == 'West':
			self._X -= 1
		else:
			pass
		return self._X

	# position Y
	@attribute(dtype='int')
	def Y(self):
		if self.dev_state() == tango.DevState.MOVING and self._direction == 'North':
			self._Y += 1
		elif self.dev_state() == tango.DevState.MOVING and self._direction == 'South':
			self._Y -= 1
		else:
			pass
		return self._Y

	# position Z (height)
	@attribute(dtype='int')
	def Z(self):
		if self.dev_state() == tango.DevState.RUNNING:
			self.restore()
			self._Z = self._Z
		elif self.dev_state() == tango.DevState.OPEN:
			self._Z += 1
		elif self._Z == 0 and self.dev_state() == tango.DevState.CLOSE:
			self.set_state(tango.DevState.ON)
		elif self._Z > 0 and self.dev_state() == tango.DevState.CLOSE:
			self._Z -= 1
		else:
			pass
		return self._Z

	# pictures taken
	@attribute(dtype='int')
	def Pictures(self):
		left_pictures_attr = self.left_drone.read_attribute('Pictures')
		self._Pictures = left_pictures_attr.value
		return self._Pictures

	# info about the camera state
	@attribute(dtype='str')
	def Camera_State(self):
		camera_state = self.left_drone.read_attribute('Camera_State')
		self._Camera_State = camera_state.value
		return self._Camera_State

	# videos shot
	@attribute(dtype='int')
	def Videos(self):
		right_videos_attr = self.right_drone.read_attribute('Videos')
		self._Videos = right_videos_attr.value
		return self._Videos

	# info about the videocamera state
	@attribute(dtype='str')
	def VideoCamera_State(self):
		videocamera_state = self.right_drone.read_attribute('VideoCamera_State')
		self._VideoCamera_State = videocamera_state.value
		return self._VideoCamera_State

	@command
	def TurnOn(self):
		super(LeaderDrone, self).TurnOn()
		self.left_drone.command_inout('TurnOn')
		self.right_drone.command_inout('TurnOn')

	@command
	def TurnOff(self):
		super(LeaderDrone, self).TurnOff()
		self.left_drone.command_inout('TurnOff')
		self.right_drone.command_inout('TurnOff')

	@command
	def TakeOff(self):
		super(LeaderDrone, self).TakeOff()
		self.left_drone.command_inout('TakeOff')
		self.right_drone.command_inout('TakeOff')

	@command
	def Land(self):
		super(LeaderDrone, self).Land()
		self.left_drone.command_inout('Land')
		self.right_drone.command_inout('Land')

	@command
	def Forward(self):
		super(LeaderDrone, self).Forward()
		self.left_drone.command_inout('Forward')
		self.right_drone.command_inout('Forward')

	@command
	def Stop(self):
		if self.dev_state() == tango.DevState.MOVING or self.dev_state() == tango.DevState.OPEN:
			self.prev_state = tango.DevState.STANDBY
			self.set_state(tango.DevState.RUNNING)
			self.send_position()
			self.left_drone.command_inout('Stop')
			self.right_drone.command_inout('Stop')
		else:
			pass

	# send the position of this drone to the others of the swarm
	def send_position(self):
		self.left_drone.write_attribute('leader_X', self._X)
		self.left_drone.write_attribute('leader_Y', self._Y)
		self.left_drone.write_attribute('leader_Z', self._Z)
		self.right_drone.write_attribute('leader_X', self._X)
		self.right_drone.write_attribute('leader_Y', self._Y)
		self.right_drone.write_attribute('leader_Z', self._Z)

	# restore the previous state when the formation finished fixing the positions
	def restore(self):
		if (self.left_drone.state() == tango.DevState.RUNNING or
			self.right_drone.state() == tango.DevState.RUNNING):
			pass
		else:
			self.set_state(self.prev_state)
			self.left_drone.command_inout('Restore')
			self.right_drone.command_inout('Restore')

	@command
	def TurnRight(self):
		super(LeaderDrone, self).TurnRight()
		if self.dev_state() == tango.DevState.STANDBY or self.dev_state() == tango.DevState.MOVING:
			self.prev_state = self.dev_state()
			self.set_state(tango.DevState.RUNNING)
			self.send_position()
			self.left_drone.command_inout('TurnRight')
			self.right_drone.command_inout('TurnRight')
		else:
			pass

	@command
	def TurnLeft(self):
		super(LeaderDrone, self).TurnLeft()
		if self.dev_state() == tango.DevState.STANDBY or self.dev_state() == tango.DevState.MOVING:
			self.prev_state = self.dev_state()
			self.set_state(tango.DevState.RUNNING)
			self.send_position()
			self.left_drone.command_inout('TurnLeft')
			self.right_drone.command_inout('TurnLeft')
		else:
			pass

	# send a message to take a picure
	@command
	def TakePicture(self):
		if self.dev_state() != tango.DevState.OFF:
			self.left_drone.command_inout('TakePicture')

	# send a message to start recording a video
	@command
	def StartRecording(self):
		if self.dev_state() != tango.DevState.OFF:
			self.right_drone.command_inout('StartRecording')

	# send a message to stop recording a video
	@command
	def StopRecording(self):
		if self.dev_state() != tango.DevState.OFF:
			self.right_drone.command_inout('StopRecording')

if __name__ == "__main__":
	run([LeaderDrone])
