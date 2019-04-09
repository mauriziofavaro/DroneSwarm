#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tango
from tango.server import Device, command, attribute, run

# Tango Device Server class that represents a videocamera
class VideoCamera(Device):

	# device initialization
	def init_device(self):
		super(VideoCamera, self).init_device()
		self.set_state(tango.DevState.OFF)
		self._Videos = 0
		self._Available = 1200

	# videos shot
	@attribute(dtype='int')
	def Videos(self):
		return self._Videos

	# seconds of video that can be shot to fill the memory
	@attribute(dtype='int')
	def Available(self):
		if self.dev_state() == tango.DevState.INSERT and self._Available == 0:
			self.StopRecording()
			self.set_state(tango.DevState.ALARM)
		elif self.dev_state() == tango.DevState.ON and self._Available == 0:
			self.set_state(tango.DevState.ALARM)
		elif self.dev_state() == tango.DevState.INSERT:
			self._Available -= 1
		else:
			pass
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
		if self.dev_state() == tango.DevState.INSERT:
			self.StopRecording()
			self.set_state(tango.DevState.OFF)
		else:
			pass

	# start recording a video
	@command
	def StartRecording(self):
		if self.dev_state() == tango.DevState.ON:
			self._Available -= 1
			self.set_state(tango.DevState.INSERT)
		else:
			pass

	# stop recording a video
	@command
	def StopRecording(self):
		if self.dev_state() == tango.DevState.INSERT:
			self.set_state(tango.DevState.ON)
			self._Videos += 1
		else:
			pass

if __name__ == "__main__":
	run([Camera])
