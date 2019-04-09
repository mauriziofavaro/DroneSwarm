#!/usr/bin/env python
# -*- coding:utf-8 -*-

from LeaderDrone import LeaderDrone
from LeftDrone import LeftDrone
from RightDrone import RightDrone
from Camera import Camera
from VideoCamera import VideoCamera
from tango.server import run

# Tango Device Server that contains all the devices of the drone swarm and
# their instruments so they can be executed all together
run([LeaderDrone, LeftDrone, RightDrone, Camera, VideoCamera])
