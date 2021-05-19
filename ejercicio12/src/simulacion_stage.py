#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist 

def callback(msg):

    izquierda = msg.ranges[0]
    derecha = msg.ranges[-1]
    frente = msg.ranges[len(msg.ranges)//2]

  
    if frente > 1.0:
        comando=Twist()
        comando.linear.x=0.5
        print("Se mueve con distancia al frente de -----> {} m".format(frente))

    
    #a partir de aqui introduzco jerarquia condicionales para evitar que el robot se choque
    if frente < 1.0:
        comando=Twist()
        comando.angular.z=0.5
        print("Distancia frente:  Fallo -----> {} m".format(frente))


    elif frente < 1.0 and izquierda < 1.0:
        comando=Twist()
        comando.angular.z=0.5
        print("Distancia frente/izquierda:  Fallo -----> {} m".format(frente))

    elif frente < 1.0 and derecha < 1.0:
        comando=Twist()
        comando.angular.z=-0.5
        print("Distancia frente/derecha:  Fallo -----> {} m".format(frente))

    
    elif izquierda < 1.0:
        comando=Twist()
        comando.angular.z=0.5
        print("\nDistancia izquierda:  Fallo --> {} m".format(izquierda))

    elif derecha < 1.0:
        comando=Twist()
        comando.angular.z=-0.5
        print("\nDistancia derecha:  Fallo ----> {} m".format(derecha))
        

    print("")
    #print("Distancia izquierda --> {}\n".format(izquierda))
    #print("Distancia frente -----> {}\n".format(frente))
    #print("Distancia derecha ----> {}\n".format(derecha))

    pub=rospy.Publisher("/mobile_base/commands/velocity",Twist,queue_size=1) 
    pub.publish(comando)
    rate=rospy.Rate(2)
    


rospy.init_node("move_turtle")
sub=rospy.Subscriber("/scan",LaserScan,callback) 
rospy.spin()

        
