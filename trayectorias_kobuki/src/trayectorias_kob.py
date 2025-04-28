#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from matplotlib.cbook import tostr


class kobuki_line:
    def __init__(self):
        rospy.init_node('Kobuki_line_node',anonymous=True)

        self.pub=rospy.Publisher('/mobile_base/commands/velocity',Twist,queue_size=10)

        self.move_line=Twist()
        self.rate=rospy.Rate(100)

    def moving_line(self,duration,velocidad):
        self.move_line.linear.x = velocidad
        self.move_line.angular.z = 0
        inicio = rospy.get_time()

        while rospy.get_time() - inicio < duration:
            self.pub.publish(self.move_line)
            self.rate.sleep()

        self.stop_robot()

    def stop_robot(self):
        self.move_line.linear.x = 0
        self.move_line.angular.z = 0
        self.pub.publish(self.move_line)

    def rotate(self,duration):
        self.move_line.linear.x=0
        self.move_line.angular.z=0.5
        inicio = rospy.get_time()

        while rospy.get_time() - inicio < duration:
            self.pub.publish(self.move_line)
            self.rate.sleep()

    def trayectoria_a(self): ## Linea recta
        self.moving_line(4,0.3)
        self.stop_robot()
        self.rotate(8) ## Aproximadamente 180 grados
        self.stop_robot()
        self.moving_line(4, 0.5)
        self.stop_robot()
        self.rotate(8)  ## Aproximadamente 180 grados
        self.stop_robot()
        self.moving_line(4, 0.7)
        self.stop_robot()
        self.rotate(8)  ## Aproximadamente 180 grados
        self.stop_robot()
        self.moving_line(4, 1)
        self.stop_robot()
        self.rotate(8)  ## Aproximadamente 180 grados
        self.stop_robot()

    def lado_cuadrado(self):  ## 2 cuadrados
        self.moving_line(3,0.3)
        self.stop_robot()
        self.rotate(4)
        self.stop_robot()

    def trayectoria_b(self):
        for i in range (4):
            self.lado_cuadrado()

    def trayectoria_c(self,duration):
        self.move_line.linear.x=0.4
        self.move_line.angular=0.3
        inicio = rospy.get_time()

        while rospy.get_time() - inicio < duration:
            self.pub.publish(self.move_line)
            self.rate.sleep()

        self.stop_robot()


if __name__=='__main__':
    try:
        print("Elige la trayectoria introduciendo el numero correspondiente: \n"
              "1.Zigzag en difreentes velocidades \n"
              "2.Cuadrado (2 vueltas) \n"
              "3.Trayectoria curva.\n")

        trayectoria = kobuki_line()
        opcion=0

        while opcion not in [1,2,3] :
            opcion=int(input('Elige una letra:'))
            if opcion==1:
                print("Opcion 1 elegida")
                trayectoria.trayectoria_a()
            elif opcion==2:
                print("Opcion 2 elegida")
                trayectoria.trayectoria_b()
            elif opcion==3:
                print("Opcion 3 elegida")
                trayectoria.trayectoria_c(5)
            else:
                print('Letra no valida, realizando traycetoria 1 por defecto')
                trayectoria.trayectoria_a()

    except rospy.ROSInterruptException:
        pass
