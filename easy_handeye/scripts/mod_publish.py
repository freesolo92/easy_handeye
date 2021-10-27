#!/usr/bin/env python

import rospy
import tf2_ros
import geometry_msgs.msg
from easy_handeye.handeye_calibration import HandeyeCalibration
import easy_handeye_msgs as ehm
from easy_handeye_msgs import srv

def callback_server(requ):
    # rospy.init_node('handeye_calibration_publisher')
    while rospy.get_time() == 0.0:
        pass

    # inverse = rospy.get_param('inverse')
    # filename = rospy.get_param('calibration_file')
    inverse = False
    filename = "/home/jetson/.ros/easy_handeye/my_calibration_eye_on_hand.yaml"

    if filename == '':
        rospy.logdebug('No path specified for the calibration file, loading from the standard location')
        # filename = HandeyeCalibration.filename_for_namespace(rospy.get_namespace())
        filename = "my_calibration"

    rospy.loginfo("Loading the calibration from file: %s", filename)
    calib = HandeyeCalibration.from_filename(filename)

    if calib.parameters.eye_on_hand:
        # overriding_robot_effector_frame = rospy.get_param('robot_effector_frame')
        overriding_robot_effector_frame = ""
        if overriding_robot_effector_frame != "":
            calib.transformation.header.frame_id = overriding_robot_effector_frame
    else:
        # overriding_robot_base_frame = rospy.get_param('robot_base_frame')
        overriding_robot_base_frame = ""
        if overriding_robot_base_frame != "":
            calib.transformation.header.frame_id = overriding_robot_base_frame
    # overriding_tracking_base_frame = rospy.get_param('tracking_base_frame')
    overriding_tracking_base_frame = ""
    if overriding_tracking_base_frame != "":
        calib.transformation.child_frame_id = overriding_tracking_base_frame

    rospy.loginfo('loading calibration parameters into namespace {}'.format(
        rospy.get_namespace()))
    HandeyeCalibration.store_to_parameter_server(calib)

    orig = calib.transformation.header.frame_id  # tool or base link
    dest = calib.transformation.child_frame_id  # tracking_base_frame

    broadcaster = tf2_ros.StaticTransformBroadcaster()
    static_transformStamped = geometry_msgs.msg.TransformStamped()

    static_transformStamped.header.stamp = rospy.Time.now()
    static_transformStamped.header.frame_id = orig
    static_transformStamped.child_frame_id = dest

    static_transformStamped.transform = calib.transformation.transform

    broadcaster.sendTransform(static_transformStamped)
    # rospy.spin()
    return ehm.srv.pubResponse(True)
        
    # else:
     
    #     # rospy.signal_shutdown('Terminate publishing tf calibration')
    #     return ehm.srv.pubResponse(requ.state)

def init_server():
    rospy.init_node('handeye_calibration_publisher')
    s = rospy.Service('/my_calibration_eye_on_hand/publish_calibration', ehm.srv.pub, callback_server)
    rospy.spin()

def main():
    init_server()

if __name__ == "__main__":
    main()