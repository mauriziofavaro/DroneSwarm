from LeaderDrone import LeaderDrone
import tango
from tango.test_context import DeviceTestContext
from assertpy import assert_that
from mock import Mock
import time

# class used for the test: it sets the other members of the swarm as dummies
class LeaderDroneTest(LeaderDrone):

	def init_device(self):
		super(LeaderDroneTest, self).init_device()
		self.left_drone = Mock() # dummy
		self.right_drone = Mock() # dummy

# auxiliary function for the test that updates the attribute Z
def update_attr_Z(device):
	t = time.time()
	while time.time() < t+0.1:
		z = device.Z

# test that the leader drone alone can take off and turn right and left maintaining the correct
# direction and state
def test_leader_take_off_and_changing_directions_with_left_and_right_dummies():
	#setup
	leader_context = DeviceTestContext(LeaderDroneTest)
	with leader_context as leader_test:
		leader_test.TurnOn()
		#exercise
		leader_test.TakeOff()
		update_attr_Z(leader_test) # updating attribute and state
		leader_test.Stop()
		update_attr_Z(leader_test) # updating attribute and state
		leader_test.TurnLeft()
		update_attr_Z(leader_test) # updating attribute and state
		leader_test.TurnRight()
		update_attr_Z(leader_test) # updating attribute and state
		leader_test.TurnRight()
		update_attr_Z(leader_test) # updating attribute and state
		#verify
		assert_that(leader_test.Z).is_greater_than(0)
		assert_that(leader_test.direction).is_equal_to('East')
		assert_that(leader_test.State()).is_equal_to(tango.DevState.STANDBY)
