from pygui import *
import struct, time
from math import atan, sqrt, sin, cos
add_library('serial')
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

    def convert_cartesian(self, pos_x, pos_y):
        pos_x += 10
        if not -100 <= pos_x <= 100:
            print('[ROBOT] POS X OUT OF RANGE', pos_x)
            return '[ROBOT] POS X OUT OF RANGE'
        if not 0 <= pos_y <= 200:
            print('[ROBOT] POS Y OUT OF RANGE', pos_y)
            return '[ROBOT] POS Y OUT OF RANGE'
        pos_y += self.offset
        first, sec = self.arms
        print('XY:', pos_x, pos_y)
        D = float(pos_x*pos_x + pos_y*pos_y - first*first - sec*sec)/float(2*first*sec)
        print(D)
        gamma = atan2(-sqrt(1-D*D), D)
        theta = atan2(pos_y, pos_x) - atan2((sec*sin(gamma)), (first+sec*cos(gamma)))
        return degrees(theta), degrees(gamma)
    
    def move_cartesian(self, pos_x, pos_y):
        return self.move_angles(*self.convert_cartesian(pos_x, pos_y))

    def convert_angles(self, theta, gamma):
        print(theta, gamma)
        if not 0 <= theta <= 180:
            print('[ROBOT] THETA OUT OF RANGE:' + str(theta))
            return '[ROBOT] THETA OUT OF RANGE:' + str(theta)
        if not -120 <= gamma <= 120:
            print('[ROBOT] GAMMA OUT OF RANGE', gamma)
            return '[ROBOT] GAMMA OUT OF RANGE'
        theta_steps, gamma_steps = int(14*theta), int(9.33*gamma)
        return [theta_steps, gamma_steps]

    def move_angles(self, theta, gamma):
        return self.write_port(1, self.convert_angles(theta, gamma))

    def move_pen(self, steps):
        return self.write_port(2, [steps])

    def move_manual(self, key=None, enable=None):
        if enable is not None:
            if enable:
                self.write_port(5, [])
            else:
                self.write_port(bytes('q'), [])
        else:
            self.write_port(bytes(key), [])

    def generate_line(self, x_1, y_1, x_n, y_n):
        if x_1 == x_n:
            points = []
            for y in range(y_1, y_n, 3):
                points.append([x_1, y])
        else:
            a = float((y_1 - y_n))/float((x_1 - x_n))
            b = y_1 - a*x_1
            print('A I B:', a, b)
            points = []
            for x in range(x_1, x_n, 10):
                points.append([x, a*x+b])
        print('POINTS:' + str(points))
        points.append([x_n, y_n])
        return points

    def generate_square(self, x_1, y_1, x_n, y_n):
        points = self.generate_line(x_1, y_1, x_1, y_n)
        points.extend(self.generate_line(x_1, y_n, x_n, y_n))
        points.extend(self.generate_line(x_n, y_n, x_n, y_1))
        points.extend(self.generate_line(x_n, y_1, x_1, y_1))
        return points

    def generate_circle(self, x, y, radius):
        n = 100
        points = [[cos(2*PI/n*o)*radius + x, sin(2*PI/n*o)*radius + y] for o in range(n)]
        points = [self.convert_angles(*self.convert_cartesian(point[0], point[1])) for point in points]
        steps = []
        for point in points:
            steps.extend([point[0], point[1]])
        return steps

    def move_line(self, x_1, y_1, x_n, y_n):
        self.move_points(self.generate_line(x_1, y_1, x_n, y_n))

    def move_square(self, x_1, y_1, x_n, y_n):
        self.move_points(self.generate_square(x_1, y_1, x_n, y_n))

    def move_circle(self, x, y, radius):
        self.move_points(self.generate_circle(x, y, radius))

    def move_points(self, points):
        print('POINTS:', points)
        steps_up = int(gui.elements['up.ntry'].value)
        steps_down = int(gui.elements['down.ntry'].value)
        self.move_angles(points[0], points[1])
        time.sleep(5)
        self.move_pen(steps_down)
        time.sleep(1)
        self.write_port(4, points)

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
            print(message)
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

    # def read_angles(self):
    #     self.port.clear()
    #     self.write_port(7, [])
    #     time.sleep(0.1)
    #     theta, gamma = str(self.read_port()).split('\n')[:-1]
    #     theta, gamma = -float(theta)/14, float(gamma)/9.33
    #     return  theta, gamma

    # def get_position(self):
    #     theta, gamma = self.read_angles()
    #     first, sec = self.arms
    #     x = first * cos(theta) + sec * cos(theta + gamma)
    #     y = first * sin(theta) + sec * sin(theta + gamma)
    #     return x, y
