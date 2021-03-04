#!/usr/bin/env python

import rospy
import numpy as np 
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

range_ahead, range_right, range_left, range_120, range_60 = 5, 5, 5, 5, 5

def callback(msg):
    global range_ahead, range_right, range_left, range_60, range_120

    #float32 angle_min  , start angle of the scan [rad]
    #float32 angle_max   , end angle of the scan [rad]
    # with zero angle being forward along the x axis
    
    #Podemos ver las caracteristicas de barrido....
    #rospy.loginfo("angle min %f",msg.angle_min)
    #rospy.loginfo("angle max %f",msg.angle_max)
    #rospy.loginfo("angle_increment %f",msg.angle_increment)  # angular distance between measurements [rad]
    
    #anglemin=np.rad2deg(msg.angle_min)
    #anglemax=np.rad2deg(msg.angle_max)
    #angleincrement=np.rad2deg(msg.angle_increment)
    #rospy.loginfo ("deg min %f",anglemin)
    #rospy.loginfo ("deg max %f",anglemax)
    #rospy.loginfo("deg increment %f",angleincrement)

    #Podemos ver los valores devueltos por el escaner laser
    #for i in range (0,len(msg.ranges),1):
    #    currentangle=anglemin+i*angleincrement
    #    rospy.loginfo ("i %d current angle %f distance %f",i,currentangle,msg.ranges[i])

    #coge haz laser hacia la mitad del array...



    range_ahead=msg.ranges[len(msg.ranges)/2]  
    range_right=msg.ranges[0]  
    range_left=msg.ranges[-1]  
    range_60=msg.ranges[len(msg.ranges)/6]  #aumentar el numero en el que dividir?
    range_120=msg.ranges[-len(msg.ranges)/3]


def dodge_and_follow():
    rospy.init_node ('move_turtlebot')
    pub=rospy.Publisher('/mobile_base/commands/velocity',Twist,queue_size=1)
    scan_sub=rospy.Subscriber('/kinetic',LaserScan,callback)
    rate=rospy.Rate(20)
    move=Twist()

    umbral_derecho = 4.0
    vel_turn = abs(( (umbral_derecho - range_right ) * 0.1) + 1.0)
    #cosas como factores de los que dependa la velocidad de giro o de movimiento segun ciertas distancias estudidas.


    #print ("distancia delante ",range_ahead)
    """Utilizo el sensor laser kinetic para la realizacion de la prueba del robot y deteccion de paredes"""
    
    while not rospy.is_shutdown():
    
        if range_ahead > 0.5 and range_right < 1.5: #el robot se debe mover mientras no detecte un objeto al frente y al encontrarse cerca de una pared.
            move.linear.x = 0.5
            move.angular.z = 0.0
            print("\n")
            print("moviendo..")
            print ("dist frente -->",range_ahead)

        elif range_ahead < 1.0:
            move.linear.x = 0.0
            move.angular.z = 0.5
            print("\n")
            print("rotando..")
            print ("dist frente -->",range_ahead)

        elif range_right > 2.0 and range_60 > 1.0: #revisar el 1.8
            move.linear.x = 0.5
            move.angular.z = -vel_turn #-v_giro (necesito ajustarla mejor de manera que se comporte mejor en ciertas partes)
            print("\n")
            print("rotando..")
            print ("dist der -->",range_right)

        elif  range_60 > umbral_derecho: #modificar velocidad giro segun las distancias detectadas
            move.linear.x = 0.5
            move.angular.z = -vel_turn
            print("\n")
            print("rotando..")
            print ("dist 60 -->",range_60)



        if range_60 < 1.6:   # o 1.8
            move.linear.x = 0.3
            move.angular.z = 0.8

        elif range_60 < 1.2 and range_ahead < 0.5:
            move.linear.x = 0.0
            move.angular.z = 0.5


        pub.publish(move)

        rate.sleep()

        

if __name__ == '__main__':
	
    try:
        dodge_and_follow()
    except rospy.ROSInterruptException:
        rospy.loginfo("terminando... ")

