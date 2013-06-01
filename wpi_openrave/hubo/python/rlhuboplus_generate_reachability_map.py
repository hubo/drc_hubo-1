# Bener Suay, May 2013
#
# benersuay@wpi.edu
#

## OPENRAVE ##
import openravepy
if not __openravepy_build_doc__:
    from openravepy import *
    from numpy import *

from openravepy.misc import OpenRAVEGlobalArguments

## ROBOT PLACEMENET ##
from Reachability import *

## MATH ##
from random import *

## SYSTEM - FILE OPS ##
import sys
import os
from datetime import datetime
import time
import commands

## Constraint Based Manipulation ##
from rodrigues import *
from TransformMatrix import *
from str2num import *
from TSR import *

env = Environment()
env.SetViewer('qtcoin')

robot = env.ReadRobotURI('../../../openHubo/huboplus/rlhuboplus.robot.xml')
env.Add(robot)

leftRm = ReachabilityMap("./rlhuboplus_rightArm_ik_solver",robot,robot.GetManipulators()[1])

leftRm.xmax=0.3
leftRm.xmin=0.0

leftRm.ymax=0.0
leftRm.ymin=-0.3

leftRm.zmax=0.3
leftRm.zmin=0.0

leftRm.r = 1
leftRm.g = 0
leftRm.b = 0

leftRm.free_joint_val = 0.0
leftRm.free_joint_index = None

leftRm.generate(env)

# print "Done. Press Enter to save the reachability map."
# sys.stdin.readline()


# Clean the object, just in case
del leftRm

print "Done. Press Enter to exit..."
sys.stdin.readline()

env.Destroy()
RaveDestroy()

