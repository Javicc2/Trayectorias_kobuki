#!/usr/bin/env python
import time
import rospy
import datetime
import os
from nav_msgs.msg import Odometry
from std_msgs.msg import Empty
import tf
from tf.transformations import euler_from_quaternion
from math import degrees


def to_positive_angle(th):
    while True:
        if th < 0:
            th += 360
        if th > 0:
            ans = th % 360
            return ans
            break

def sub_odom():
    sub = rospy.Subscriber('/odom',Odometry, callback_odom)


def callback_odom(data):
    global x,y,th
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

x, y, th = 0.0, 0.0, 0.0

rospy.init_node("sub_odom")
rate = rospy.Rate(100)

## Reset odometry
pub = rospy.Publisher('/mobile_base/commands/reset_odometry' ,Empty, queue_size=10)
pub.publish()
time.sleep(1)

if __name__ == '__main__':
    sub_odom()

    # Creacion del archivo .txt
    filepath = os.path.dirname((os.path.abspath(__file__)))+'/datos_odom/'
    filename = "Odom_"+str(datetime.datetime.now())+".txt"
    full_filename=filepath+filename
    file=open(full_filename,"a")
    rospy.loginfo("Se ha abierto archivo de texto en %s",full_filename)
    file.write("t    x     y    deg \n")


    start=time.time()
    while not rospy.is_shutdown():
        t=time.time()-start
        #print("t:%.3f x:%.2f y:%.2f deg%.2f" % (t, x, y, th))
        file.write("%.3f   %.2f   %.2f   %.2f \n"%(t, x, y, th))
        #rospy.loginfo("Dato guardado con exito en txt")
        rate.sleep()

    file.close()
    rospy.loginfo("Archivo cerrado con exito")