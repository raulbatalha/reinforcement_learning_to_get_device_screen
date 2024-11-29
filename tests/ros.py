import math

import rospy
from std_msgs.msg import Float32


class PhantomXController:
    def __init__(self):
        rospy.init_node('publisher', anonymous=True)
        self.rate = rospy.Rate(2)  # 2Hz

        # Dimensões do PhantomX Pincher
        self.l1 = 0.35  # Comprimento do primeiro elo (Alcance Vertical)
        self.l2 = 0.31  # Comprimento do segundo elo (Alcance Horizontal)

        # Publicadores das posições das articulações
        self.pub_ang1 = rospy.Publisher('/ang1', Float32, queue_size=10)
        self.pub_ang2 = rospy.Publisher('/ang2', Float32, queue_size=10)
        self.pub_ang3 = rospy.Publisher('/ang3', Float32, queue_size=10)
        self.pub_ang4 = rospy.Publisher('/ang4', Float32, queue_size=10)

    def calculate_joint_angles(self, x, y, z):
        # Aplicar cinemática inversa para calcular as posições das articulações
        d = math.sqrt(x**2 + y**2)
        ang1 = math.atan2(y, x) * 180 / math.pi
        ang2 = -90
        ang3 = -(math.acos((d**2 + (z-0.25)**2 - self.l1**2 - self.l2**2) / (2*self.l1*self.l2)) * 180 / math.pi - 90)
        ang4 = -(math.acos((self.l1**2 + self.l2**2 - d**2 - (z-0.25)**2) / (2*self.l1*self.l2)) * 180 / math.pi)

        return ang1, ang2, ang3, ang4

    def publish_joint_angles(self, ang1, ang2, ang3, ang4):
        # Publicar as posições das articulações
        msg_ang1 = Float32()
        msg_ang1.data = ang1
        self.pub_ang1.publish(msg_ang1)

        msg_ang2 = Float32()
        msg_ang2.data = ang2
        self.pub_ang2.publish(msg_ang2)

        msg_ang3 = Float32()
        msg_ang3.data = ang3
        self.pub_ang3.publish(msg_ang3)

        msg_ang4 = Float32()
        msg_ang4.data = ang4
        self.pub_ang4.publish(msg_ang4)

    def run(self):
        while not rospy.is_shutdown():
            x = +0.021  # Coordenada X desejada
            y = +0.002  # Coordenada Y desejada
            z = +0.00  # Coordenada Z desejada

            ang1, ang2, ang3, ang4 = self.calculate_joint_angles(x, y, z)
            self.publish_joint_angles(ang1, ang2, ang3, ang4)

            self.rate.sleep()

if __name__ == '__main__':
    try:
        controller = PhantomXController()
        controller.run()
    except rospy.ROSInterruptException:
        pass
