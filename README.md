DroneSwarm
==========


File list
----------
* `DroneSwarm.py`: Device Server container  
* `Drone.py`: Generic drone Device Server implementation  
* `LeaderDrone.py`: Leader of the swarm implementation  
* `LeftDrone.py`: Drone on the left of formation  
* `RightDrone.py`: Drone on the right of formation  
* `Camera.py`: Camera connected to LeftDrone  
* `VideoCamera.py`: Videocamera connected to RightDrone  
* `test_TakeOff_and_directions.py`: Test for leader behaviour with dummies  
* `test_with_almost_full_stub_camera.py`: Test with almost full stub Camera  
* `test_formation_with_setup.py`: Test formation using with_setup  
* `README.md`: This File


Requirements
-------------
* [Python](https://www.python.org/) (better if >= 2.7)
* [PyTango](https://pytango.readthedocs.io/en/stable/) >= 9.2.1
* [nose](https://nose.readthedocs.io/en/latest/index.html) (1.3.7)
* [assertpy](https://github.com/ActivisionGameScience/assertpy)
* [mock](https://github.com/testing-cabal/mock) (if Python < 3.3)

**WARNING:**  
If Python >= 3.3:
on `test_TakeOff_and_directions.py`, `test_with_almost_full_stub_camera.py` and
`test_formation_with_setup.py`, the line  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; **from mock import Mock**  
should be replaced with  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;**from unittest.mock import Mock**



Project
--------
DroneSwarm is a Tango Device Server with multiple device classes that represents a group of three
drones and their payloads. There are three test cases for the Device Server that check his
behaviour using test doubles and other tools.


How-To
-------
To run the Device Server, `DronesSwarm.py` must be registered on Tango database with Jive.
To work correctly, the instances of the devices should be created like this:
- one device from LeaderDrone
- one device from LeftDrone called "sim/test/left"
- one device from RightDrone called "sim/test/right"
- one device from Camera called "sim/test/cam"
- one device from VideoCamera called "sim/test/vid"
`DroneSwarm.py`, `Drone.py`, `LeaderDrone.py`, `LeftDrone.py`, `RightDrone.py`, `Camera.py` and `VideoCamera.py`
must stay in the same directory.

The test cases (`test_TakeOff_and_directions.py`, `test_with_almost_full_stub_camera.py` and
`test_formation_with_setup.py`) are meant to be executed with nose. The last one uses a specific
nose tool (with_setup).
To work, they must stay in the same directory with all the other files of this project.
