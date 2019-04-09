from LeaderDrone import LeaderDrone
from LeftDrone import LeftDrone
from RightDrone import RightDrone
import tango
from tango.test_context import DeviceTestContext
from assertpy import assert_that
from mock import Mock
import time
from nose.tools import with_setup

# class used for the test: it sets the camera as a dummy
class LeftDroneTest(LeftDrone):

	def init_device(self):
		super(LeftDroneTest, self).init_device()
		self.camera = Mock() # dummy

# class used for the test: it sets the videocamera as a dummy
class RightDroneTest(RightDrone):

	def init_device(self):
		super(RightDroneTest, self).init_device()
		self.videocamera = Mock() # dummy

# test contexts global variables
left_context = None
right_context = None
leader_context = None
left = None
right = None
leader = None

# setup function: creates the test contexts and starts them, then makes the swarm take off
def setup_func():
	global left_context
	global right_context
	global leader_context
	global left
	global right
	global leader
	left_context = DeviceTestContext(LeftDroneTest, process=True)
	right_context = DeviceTestContext(RightDroneTest, process=True)
	left = left_context.__enter__()
	right = right_context.__enter__()
	properties = {'left_drone_address': left_context.get_device_access(),
					'right_drone_address': right_context.get_device_access()}
	leader_context = DeviceTestContext(LeaderDrone, properties=properties, process=True)
	leader = leader_context.__enter__()
	leader.TurnOn()
	leader.TakeOff()
	update_attr(leader, left, right, 0.1) # updating attributes and state
	leader.Stop()
	update_attr(leader, left, right, 0.1) # updating attributes and state

# teardown function: stops the test contexts
def teardown_func():
	leader_context.stop()
	right_context.stop()
	left_context.stop()

# auxiliary function for the test that updates the attributes (positions) of the contexts
def update_attr(leader, left, right, delay):
	t = time.time()
	while time.time() < t + delay:
		leader_z = leader.Z
		left_z = left.Z
		right_z = right.Z
		leader_x = leader.X
		left_x = left.X
		right_x = right.X
		leader_y = leader.Y
		left_y = left.Y
		right_y = right.Y

# test that the swarm behaves correctly when it moves forward and then stops
@with_setup(setup_func, teardown_func) #setup / teardown
def test_formation_after_moving_forward():
	#exercise
	leader.Forward()
	update_attr(leader, left, right, 1) # updating attributes and state
	leader.Stop()
	update_attr(leader, left, right, 0.1) # updating attributes and state
	#verify
	left_z = left.Z
	right_z = right.Z
	left_y = left.Y
	right_y = right.Y
	left_state = left.State()
	right_state= right.State()
	assert_that(leader.Z).is_equal_to(left_z).is_equal_to(right_z).is_greater_than(0)
	assert_that(leader.Y).is_equal_to(left_y+1).is_equal_to(right_y+1).is_greater_than(0)
	assert_that(leader.State()).is_equal_to(left_state).is_equal_to(right_state)\
		.is_equal_to(tango.DevState.STANDBY)

# test that the swarm behaves correctly when turns right while moving forward
@with_setup(setup_func, teardown_func) #setup / teardown
def test_formation_turn_right_while_moving():
	#exercise
	leader.Forward()
	update_attr(leader, left, right, 1) # updating attributes and state
	leader.TurnRight()
	update_attr(leader, left, right, 0.1) # updating attributes and state
	#verify
	left_dir = left.direction
	right_dir = right.direction
	left_z = left.Z
	right_z = right.Z
	left_x = left.X
	right_x = right.X
	left_y = left.Y
	right_y = right.Y
	left_state = left.State()
	right_state= right.State()
	assert_that(leader.direction).is_equal_to(left_dir).is_equal_to(right_dir).is_equal_to('East')
	assert_that(leader.X).is_equal_to(left_x+1).is_equal_to(right_x+1)
	assert_that(leader.Y).is_equal_to(left_y-1).is_equal_to(right_y+1)
	assert_that(leader.Z).is_equal_to(left_z).is_equal_to(right_z)
	assert_that(leader.State()).is_equal_to(left_state).is_equal_to(right_state)\
		.is_equal_to(tango.DevState.MOVING)

# test that the swarm behaves correctly when it lands
@with_setup(setup_func, teardown_func) #setup / teardown
def test_landing():
	#exercise
	leader.Land()
	update_attr(leader, left, right, 0.1) # updating attributes and state
	#verify
	left_z = left.Z
	right_z = right.Z
	left_state = left.State()
	right_state= right.State()
	assert_that(leader.Z).is_equal_to(left_z).is_equal_to(right_z).is_equal_to(0)
	assert_that(leader.State()).is_equal_to(left_state).is_equal_to(right_state)\
		.is_equal_to(tango.DevState.ON)
