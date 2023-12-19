#!/usr/bin/env python

import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn
import math

turtle1_pose = None
turtle2_pose = None

def callback_turtle1_pose(data):
    global turtle1_pose
    turtle1_pose = data

def callback_turtle2_pose(data):
    global turtle2_pose
    turtle2_pose = data

def main():
    rospy.init_node('my_turtle_control_node')
    rospy.Subscriber('/turtle1/pose', Pose, callback_turtle1_pose)
    rospy.Subscriber('/turtle2/pose', Pose, callback_turtle2_pose)
    pub = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)
    rospy.wait_for_service('/spawn')
    try:
        spawn_turtle = rospy.ServiceProxy('/spawn', Spawn)
        spawn_turtle(4, 4, 0, 'turtle2')
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
    while not rospy.is_shutdown():
        if turtle1_pose is not None and turtle2_pose is not None:
            msg = Twist()
            dx = turtle1_pose.x - turtle2_pose.x
            dy = turtle1_pose.y - turtle2_pose.y
            angle_to_goal = math.atan2(dy, dx)
            angle_diff = angle_to_goal - turtle2_pose.theta
            if angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            elif angle_diff < -math.pi:
                angle_diff += 2 * math.pi
            msg.linear.x = 1.0 * math.sqrt(dx**2 + dy**2)
            msg.angular.z = 4.0 * angle_diff
            pub.publish(msg)
            rospy.loginfo(msg)
        rate.sleep()

if __name__ == '__main__':
    main()