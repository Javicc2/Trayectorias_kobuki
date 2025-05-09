#!/usr/bin/env python
import time
import rospy
import datetime
import os
from nav_msgs.msg import Odometry
from std_msgs.msg import Empty
from trayectorias_kobuki.msg import angulo
import tf
from tf.transformations import euler_from_quaternion
from math import degrees

x, y, th = 0.0, 0.0, 0.0

def to_positive_angle(th):
    while True:
        if th < 0:
            th += 360
        if th > 0:
            ans = th % 360
            return ans
            break


def callback_odom(data):
    global x,y,th
    #rospy.loginfo("Se ha llamado al subscriptor del odometro")
    x = data.pose.pose.position.x
    y = data.pose.pose.position.y
    q1 = data.pose.pose.orientation.x
    q2 = data.pose.pose.orientation.y
    q3 = data.pose.pose.orientation.z
    q4 = data.pose.pose.orientation.w
    q = (q1, q2, q3, q4)
    e = euler_from_quaternion(q)
    th = degrees(e[2])
    th = to_positive_angle(th)
    dato_angulo.ang=th
    pub2.publish(th)

def sub_odom():
    sub=rospy.Subscriber('/odom',Odometry, callback_odom)





rospy.init_node("sub_odom")
rate = rospy.Rate(50)

## Reset odometry
pub = rospy.Publisher('/mobile_base/commands/reset_odometry' ,Empty, queue_size=10)
pub.publish()
time.sleep(1)




if __name__ == '__main__':
    #Creamos la comunicacion
    dato_angulo = angulo()
    pub2 = rospy.Publisher('/angulo_odometria',angulo, queue_size=10)


    # Creacion del suscriptor y proceso de guardado de datos en txt
    start=time.time()
    sub_odom()

    # Creacion del archivo .txt
    filepath = os.path.dirname((os.path.abspath(__file__))) + '/datos_odom/'
    filename = "Odom_" + str(datetime.datetime.now()) + ".txt"
    full_filename = filepath + filename
    file = open(full_filename, "a")
    # rospy.loginfo("Se ha abierto archivo de texto en %s",full_filename)
    file.write("t           x            y            deg \n")


    while not rospy.is_shutdown():
        t = time.time() - start
        #print("t:%.3f x:%.2f y:%.2f deg%.2f" % (t, x, y, th))
        file.write("%.3f      %.2f      %.2f      %.2f \n" % (t, x, y, th))
        # rospy.loginfo("Dato guardado con exito en txt")
        #rospy.loginfo("La th del odometro es: %.2f", th)
        rate.sleep()



    file.close()
    #rospy.loginfo("Archivo cerrado con exito")