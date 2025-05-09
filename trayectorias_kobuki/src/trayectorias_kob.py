#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from trayectorias_kobuki.msg import angulo
from matplotlib.cbook import tostr


class KobukiMove:
    def __init__(self):
        rospy.init_node('Kobuki_line_node',anonymous=True)

        self.pub=rospy.Publisher('/mobile_base/commands/velocity',Twist,queue_size=10)
        self.angulo_stop=0
        self.angulo_actual=0
        self.move_line=Twist()
        self.rate=rospy.Rate(50)


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
        orientacion_stop=rospy.wait_for_message('/angulo_odometria',angulo)
        #rospy.loginfo('El valor de parada obtenido es %.2f' , orientacion_stop.ang)
        self.angulo_stop=orientacion_stop.ang


    def callback_angulo_actual(self,data):
        #rospy.loginfo("Se ha recibido el dato actual de angulo")
        self.angulo_actual=data.ang

    ####   TRAYECTORIAS  ####
    def rotate(self,theta):
        rospy.Subscriber('/angulo_odometria', angulo, self.callback_angulo_actual)

        while not rospy.is_shutdown() and ((360+self.angulo_actual - self.angulo_stop) % 360) < theta:
            self.move_line.linear.x = 0
            self.move_line.angular.z = 0.4
            self.pub.publish(self.move_line)
            print("El robot ha girado %.2f de %.2f" %(((360+self.angulo_actual - self.angulo_stop) % 360) ,theta))
            self.rate.sleep()


    def trayectoria_a(self): ## Linea recta
        self.moving_line(4,0.3)
        self.stop_robot()
        self.rotate(180) ## Aproximadamente 180 grados
        self.stop_robot()
        self.moving_line(4, 0.5)
        self.stop_robot()
        self.rotate(180)  ## Aproximadamente 180 grados
        self.stop_robot()
        self.moving_line(4, 0.7)
        self.stop_robot()
        self.rotate(180)  ## Aproximadamente 180 grados
        self.stop_robot()
        self.moving_line(4, 1)
        self.stop_robot()
        self.rotate(180)  ## Aproximadamente 180 grados
        self.stop_robot()

    def lado_cuadrado(self):  ## 2 cuadrados
        self.moving_line(2,0.3)
        self.stop_robot()
        self.rotate(90)
        self.stop_robot()

    def trayectoria_b(self):
        for i in range (4):
            self.lado_cuadrado()

    def trayectoria_c(self,duration):
        self.move_line.linear.x=0.4
        self.move_line.angular=0.3
        inicio = rospy.get_time()
        rospy.loginfo("Movimiento rectilineo")

        while rospy.get_time() - inicio < duration:
            self.pub.publish(self.move_line)
            self.rate.sleep()

        self.stop_robot()

    def trayectoria_d(self):
        self.moving_line(2, 0.3)
        self.stop_robot()

    def prueba(self):
        self.stop_robot()


if __name__=='__main__':
    try:
        print("Elige la trayectoria introduciendo el numero correspondiente: \n"
              "0.Prueba \n"
              "1.Zigzag en difreentes velocidades \n"
              "2.Cuadrado (2 vueltas) \n"
              "3.Trayectoria curva.\n"
              "4.Una linea recta.\n")

        trayectoria = KobukiMove()
        opcion=2


        if opcion==0:
            print("El robot no hara nada")
            trayectoria.prueba()
        elif opcion==1:
            print("Opcion 1 elegida")
            trayectoria.trayectoria_a()
        elif opcion==2:
            print("Opcion 2 elegida")
            trayectoria.trayectoria_b()
        elif opcion==3:
            print("Opcion 3 elegida")
            trayectoria.trayectoria_c(4)
        elif opcion==4:
            print("Opcion 3 elegida")
            trayectoria.trayectoria_d()


    except rospy.ROSInterruptException:
        pass
