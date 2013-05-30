#!/usr/bin/python

#############################################################################
#                                                                           #
#   Calder Phillips-Grafflin -- WPI/Drexel Darpa Robotics Challenge Team    #
#                                                                           #
#   Service interface to the Hubo CBiRRT planner class                      #
#                                                                           #
#############################################################################

import subprocess

import roslib; roslib.load_manifest('hubo_planner')
import rospy
from std_msgs.msg import *
from sensor_msgs.msg import *
from trajectory_msgs.msg import *
from hubo_planner.srv import *

import hubo_trajectory_reader
import hubo_plus_wheel_turning


class HuboPlannerInterface:

    def __init__(self, path):

        self.debug = True
        rospy.loginfo("Starting Hubo planner interface...")
        self.path = path
        self.current_config = None

        path_to_robot = path + '/../openHubo/huboplus/rlhuboplus_mit.robot.xml'
        path_to_wheel = path + '/../../drc_common/models/driving_wheel.robot.xml'
        self.planner = hubo_plus_wheel_turning.HuboPlusWheelTurning( path_to_robot, path_to_wheel )
        self.planner.SetViewer(True)
        self.planner.SetStopKeyStrokes(False)

        rospy.loginfo("Loaded Hubo CBiRRT wrapper")
        self.config_cb = rospy.Subscriber("/joint_states", JointState, self.Hubo_CB)
        self.RequestHandler = rospy.Service("hubo_planner/PlanningQuery", PlanValveTurning, self.RequestHandler)
        rospy.loginfo("Service host loaded, Planner interface running")
        
        
    def RequestHandler(self, request):

        # Set wheel location
        wheel_trans = [request.valve_position.position.x, request.valve_position.position.y, request.valve_position.position.z]
        wheel_rot = [request.valve_position.orientation.x, request.valve_position.orientation.y, request.valve_position.orientation.z, request.valve_position.orientation.w]

        if( not self.debug ):
            self.planner.SetWheelPosition( wheel_trans, wheel_rot )
        else:
            print wheel_trans
            print wheel_rot

        if( not self.debug ):
            while (self.current_config is None):
                rospy.logwarn("Planner is waiting to recieve joint states of the robot!")
            self.planner_wrapper.SetRobotConfig(self.current_config)

        # Call to CBiRRT
        trajectory_files = self.planner.Run()

        if (trajectory_files is None or trajectory_files == []):
            # Make an error response
            error = None
            return error
        else:
            return self.BuildResponse(trajectory_files)


    def BuildResponse(self, trajectory_files):

        traj_array = []

        for f in trajectory_files:
            traj_array.append( hubo_trajectory_reader.read( f ) )

        #return traj_array
        print traj_array
        return True


    def Hubo_CB(self, msg):
        # Assemble a new config
        new_config = {}
        if (len(msg.name) != len(msg.position)):
            rospy.logerr("Malformed JointState!")
        else:
            for joint_index in range(len(msg.name)):
                new_config[msg.name[joint_index]] = msg.position[joint_index]
            self.current_config = new_config
    
    def Hook(self):
        print "End planner node"
        self.planner.KillOpenrave()
       

if __name__ == '__main__':
    path = subprocess.check_output("rospack find hubo_planner", shell=True)
    path = path.strip("\n")
    rospy.init_node("hubo_planner_interface")
    # Maybe we will need params some day?
    huboplan = HuboPlannerInterface( path )
    rospy.on_shutdown( huboplan.Hook )
    print "Robot ready to plan, waiting for a valve pose update..."
    rospy.spin()
    

