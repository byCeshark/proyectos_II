#!/usr/bin/env python

import rospy
import numpy as np 
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


""" LA VELOCIDAD DEL ROBOT VA A SER SUPERIOR A LA 
    EMPLEADA PARA EL REAL, ACELERANDO LA MUESTRA 
    DEL PROGRAMA Y EL COMPORTAMIENTO PARA EL VIDEO """

front_range = 5
right_range = 5
left_range  = 5 
range_fright = 5  
#equivalente al /kinetic max_range 


def callback(msg):
    
    global front_range, right_range, left_range, range_fright

    front_range = msg.ranges[len(msg.ranges)/2]  
    right_range = msg.ranges[0]  
    left_range  = msg.ranges[-1]  #no es necesaria su inicializacion pero se deja por caso de ser necesaria

    position_degree = 3
    range_fright  = msg.ranges[len(msg.ranges)/(2*position_degree)]  #rango entre el frente del robot y su derecha
    #range_120 = msg.ranges[-len(msg.ranges)/3] #rango de 120 degrees


def follow_wall():


    umbral_right = 4.0
    vel_turn = abs(( (umbral_right - right_range ) * 0.1) + 1.0)
    #creo una variable para ajustar la velocidad en aquellas situaciones donde se presenta una distancia critica para el funcionamiento
    #actua de manera que cuanto mayor sea la diferencia entre el umbral definido a la derecha y la distancia de este mismo lado,
    #mas lenta sera la velocidad de giro en el eje Z y al irse acercando a un obstaculo esta velocidad ira aumentando con el siguiente principio



    """Utilizo el sensor laser kinetic para la realizacion de la prueba del robot y la deteccion de paredes u obstaculos a su derecha"""
    

    rospy.init_node ('move_turtlebot')
    pub=rospy.Publisher('/mobile_base/commands/velocity',Twist,queue_size=1)
    scan_sub=rospy.Subscriber('/kinetic',LaserScan,callback) #sensor kinetic
    
    rate=rospy.Rate(20)
    move=Twist()

    dist_limit  = 0.5

    while not rospy.is_shutdown():
    

        if front_range > dist_limit and right_range < 1.5: #el robot se debe mover mientras no detecte un objeto al frente y al encontrarse cerca de una pared.
            move.linear.x = 0.5
            move.angular.z = 0.0
            print("\n")
            print("moviendo..")
            print ("distancia frente -->",front_range)

            if right_range < 1.0:
                print ("distancia derecha -->",right_range)


        elif front_range < dist_limit*2:
            move.linear.x = 0.0
            move.angular.z = 0.5
            print("\n")
            print("rotando..")
            print ("distancia frente -->",front_range)


        elif right_range > 2.0 and range_fright > 1.0: #en caso de que detecta un campo vacio
            move.linear.x = 0.5
            move.angular.z = -vel_turn
            print("\n")
            print("rotando..")
            print ("distancia derecha -->",right_range)


        elif range_fright > umbral_right: #modificar velocidad giro segun las distancias detectadas
            move.linear.x = 0.5
            move.angular.z = -vel_turn
            print("\n")
            print("rotando..")
            print ("distancia lateral -->",range_fright)


        #Grupo de condicionales que rompan con los niveles anteriores forzando un giro cuando el sensor intermedio entre la el frente y la derecha del robot, detecta cerca una pared.
        
        # Distancias que me han parecido las mas adecuadas para la seguridad y control del turtlebot
        if range_fright < 1.6:
            move.linear.x = 0.3
            move.angular.z = 0.8
            print("\n")
            print("rotando..")
            print ("distancia frente derecha -->",range_fright)

        elif range_fright < 1.2 and front_range < 0.5:
            move.linear.x = 0.0
            move.angular.z = 0.5
            print("\n")
            print("rotando..")
            print ("distancia frente derecha -->",range_fright)


        pub.publish(move)

        rate.sleep()

        

if __name__ == '__main__':
	
    try:
        follow_wall()
    except rospy.ROSInterruptException:
        rospy.loginfo("terminando simulacion... ")

        

