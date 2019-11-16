import serial
from math import atan, sqrt, sin, cos
from utils import Position, Angles

class Robot:
    def __init__(self, arm_1, arm_2, height):
        self.arms = arm_1, arm_2
        self.height = height

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
        pass

    def read_angles(self):
        return 0, 0
