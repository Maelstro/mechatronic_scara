import struct
from math import atan, sqrt, sin, cos
add_library('serial')

class Robot:
    def __init__(self, arm_1, arm_2, height):
        self.arms = arm_1, arm_2
        self.height = height
        self.port = None

    def connect(self, port_name):
        try:
            print(port_name)
            self.port = Serial(this, port_name, 460800)
            # self.port.clear()
        except:
            return False
        else:
            return True

    def move_to(self, angles=None, pos=None):
        if angles is None:
            x, y = pos
            first, second = self.arms
            D = (x*x + y*y - first*first - second*second)/2*first*second
            gamma = atan(sqrt(1-D*D)/D)
            theta = atan(y/x) - atan((second*sin(gamma))/(first+second*cos(gamma)))
            self.send_angles(theta, gamma)
        else:
            self.send_angles(*angles)

    def get_position(self):
        theta, gamma = self.read_angles()
        first, second = self.arms
        x = first * cos(theta) + second * cos(theta + gamma)
        y = first * sin(theta) + second * sin(theta + gamma)
        return x, y

    def pen_up(self):
        pass

    def send_angles(self, theta, gamma):
        self.port.write(struct.pack('i', int(theta)))
        self.port.write(struct.pack('i', int(gamma)))

    def read_port(self):
        return self.port.readString()
