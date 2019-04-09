from LeaderDrone import LeaderDrone
from LeftDrone import LeftDrone
from RightDrone import RightDrone
import tango
from tango.test_context import DeviceTestContext
from assertpy import assert_that

# class used for the test: it sets the camera and its methods as stubs
# the stub camera has only 1 picture available, then the memory will be full
class LeftDroneTest(LeftDrone):

	def init_device(self):
		super(LeftDroneTest, self).init_device()
		self.camera = Mock(Pictures=0, State=tango.DevState.OFF)
		self.camera.read_attribute = Mock(side_effect= lambda s: Mock(value = self.camera.Pictures))
		self.camera.state = Mock(side_effect= lambda: self.camera.State)
		self.camera.command_inout = Mock(side_effect= lambda s: self.command_cam(s))

	# auxiliary function to mock command_inout behaviour on the camera stub
	def command_cam(self, s):
		if s == 'TurnOn':
			self.camera.State = tango.DevState.ON
		elif s == 'TurnOff':
			self.camera.State = tango.DevState.OFF
		elif s == 'TakePicture':
			self.camera.Pictures += 1
			self.camera.State = tango.DevState.ALARM
		else:
			pass

# class used for the test: it sets the videocamera as a dummy
class RightDroneTest(RightDrone):

	def init_device(self):
		super(RightDroneTest, self).init_device()
		self.videocamera = Mock() # dummy

# left and right drone test contexts
left_context = DeviceTestContext(LeftDroneTest, process=True)
right_context = DeviceTestContext(RightDroneTest, process=True)

# test that the behaviour of the swarm is correct when the camera gets full, using an
# almost full stub camera
def test_swarm_with_almost_full_stub_camera():
	#setup
	with left_context as left, right_context as right:
		properties = {'left_drone_address': left_context.get_device_access(),
						'right_drone_address': right_context.get_device_access()}
		leader_context = DeviceTestContext(LeaderDrone, properties=properties, process=True)
		with leader_context as leader:
			leader.TurnOn()
			#exercise
			leader.TakePicture()
			#verify
			assert_that(leader.Pictures).is_equal_to(1)
			assert_that(leader.Camera_State).is_equal_to('MEMORY FULL')
