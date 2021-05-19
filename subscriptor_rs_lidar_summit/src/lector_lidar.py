#!/usr/bin/env python
import rospy
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
import math


def callback(msg):
    #print msg.data
    #Podemos ver las caracteristicas de barrido....
    rospy.loginfo("height %d",msg.height) #point cloud heidth in pixels
    rospy.loginfo("width %d",msg.width) # Point cloud width in pixels
    #rospy.loginfo("datos 0",msg.data[0])
    #rospy.loginfo("angle_increment %f",msg.angle_increment)  # angular distance between measurements [rad]
    #xyz=rosReadXYZ(msg)
    #gen = pc2.read_points(cloud, skip_nans=True, field_names=("x", "y", "z"))
    dato=0
    for p in pc2.read_points(msg, field_names = ("x", "y", "z"), skip_nans=True):
        print ("dato: ",dato," ")
        print " x : %f  y: %f  z: %f" %(p[0],p[1],p[2])
        distancia=math.sqrt(p[0]**2+p[1]**2+p[2]**2)
        print "distancia ",distancia
        dato=dato+1

rospy.init_node('subscriptor_lidar')

sub=rospy.Subscriber('/robot/lidar_3d/point_cloud',PointCloud2,callback)
rospy.spin()