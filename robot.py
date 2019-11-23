import struct
from math import atan, sqrt, sin, cos
from processing.serial import *

class Robot:
    def __init__(self, arm_1, arm_2, offset):
        self.arms = arm_1, arm_2
        self.offset = offset
        self.port = None

    def connect(self, port_name):
        try:
            self.port = Serial(this, port_name, 460800)
        except:
            return '[ROBOT] CONNECTION FAILED'
        else:
            return '[ROBOT] CONNECTED'

    def reset_encoders(self):
        return self.write_port(3, [])

    def move_cartesian(self, pos_x, pos_y):
        if not -100 <= pos_x <= 100:
            return '[ROBOT] POS X OUT OF RANGE'
        if not 0 <= pos_y <= 200:
            return '[ROBOT] POS Y OUT OF RANGE'
        pos_y += self.offset
        first, second = self.arms
        D = (pos_x*pos_x + pos_y*pos_y - first*first - second*second)/2*first*second
        gamma = atan(sqrt(1-D*D)/D)
        theta = atan(pos_y/pos_x) - atan((second*sin(gamma))/(first+second*cos(gamma)))
        return self.move_angles(theta, gamma)

    def move_angles(self, theta, gamma):
        if not 0 <= theta <= 180:
            return '[ROBOT] THETA OUT OF RANGE'
        if not -90 <= gamma <= 90:
            return '[ROBOT] GAMMA OUT OF RANGE'
        theta_steps, gamma_steps = int(14*theta), int(9.33*gamma)
        return self.write_port(1, [theta_steps, gamma_steps])

    def move_pen(self, steps):
        return self.write_port(2, [steps])

    def write_port(self, id, payload):
        nums = ['+'+str(num) if num >= 0 else str(num) for num in payload]
        payload = []
        for num in nums:
            missing = 5 - len(num)
            if missing >= 0:
                payload.append(num[0] + '0'*missing + num[1:])
            else:
                break
        else:
            num_of_bytes = str(1+5*len(payload)) + 'c'
            message = struct.pack(num_of_bytes,
                                  bytes(id),
                                  *[bytes(bt) for word in payload for bt in word])
            try:
                self.port.clear()
                self.port.write(message)
            except:
                return '[ROBOT] FAILED TO SEND MESSAGE: ' + str(message)
            else:
                return '[ROBOT] SENT MESSAGE: ' + str(message)
        return '[ROBOT] PAYLOAD OUT OF RANGE'

    def read_port(self):
        return self.port.readString()

    # def get_position(self):
    #     theta, gamma = self.read_angles()
    #     first, second = self.arms
    #     x = first * cos(theta) + second * cos(theta + gamma)
    #     y = first * sin(theta) + second * sin(theta + gamma)
    #     return x, y
