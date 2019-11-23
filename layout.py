from pygui import *
from styles import BORDERLESS, GREEN

class ControlGui(Column):
    def __init__(self, robot):
        super(ControlGui, self).__init__('main', self.create_children(), [1, 1, 4, 1])
        self.robot = robot

    @staticmethod
    def create_children():
        return [
            Label('title', 'DRAWING SCARA CONTROL STATION'),
            Row('up_row', [
                Label('port.lbl', 'serial port'),
                Entry('port.ntry', 'COM6'),
                Button('connect.btn', 'Connect')
            ], [1, 1, 1]),
            Row('low_row', [
                ControlUnit('Joint', ['theta', 'gamma'], 'Move'),
                ControlUnit('Cartesian', ['X', 'Y'], 'Move'),
                Column('pen_col', [
                    Button('calibrate.btn', 'Reset Encoders'),
                    Button('read.btn', 'Read Serial'),
                    Row('penup.row', [
                        Button('up.btn', 'UP'),
                        NumEntry('up.ntry', 0),
                    ], [1, 1], GREEN),
                    Row('pendown.row', [
                        Button('down.btn', 'DOWN'),
                        NumEntry('down.ntry', 290),
                    ], [1, 1], GREEN)
                ], [1, 1, 1, 1])
            ], [1, 1, 1]),
            Logger('logger', BORDERLESS)
        ]

    def log(self, text):
        lbl_1, lbl_2, lbl_3 = [gui.elements['logger.lbl'+str(i)] for i in range(1, 4)]
        lbl_1.text = lbl_2.text
        lbl_2.text = lbl_3.text
        lbl_3.text = text

    def connect(self):
        port = gui.elements['port.ntry'].text
        self.log('[ GUI ] CONNECTING TO PORT ' + port)
        self.log(self.robot.connect(port))

    def reset_encoders(self):
        self.log('[ GUI ] RESETTING ENCODERS')
        self.log(self.robot.reset_encoders())

    def move_cartesian(self):
        x = gui.elements['Cartesian.ctrl.ntry1'].value
        y = gui.elements['Cartesian.ctrl.ntry2'].value
        self.log('[ GUI ] SENDING SERIAL CARTESIAN MOVE: ' + str(x) + ', ' + str(y))
        self.log(self.robot.move_cartesian(x, y))

    def move_angles(self):
        theta = int(gui.elements['Joint.ctrl.ntry1'].value)
        gamma = int(gui.elements['Joint.ctrl.ntry2'].value)
        self.log('[ GUI ] SENDING SERIAL ANGLES MOVE: ' + str(theta) + ', ' + str(gamma))
        self.log(self.robot.move_angles(theta, gamma))

    def pen_up(self, up):
        entry = 'up.ntry' if up else 'down.ntry'
        steps = int(gui.elements[entry].value)
        self.log('[ GUI ] MOVING PEN TO ' + str(steps))
        self.log(self.robot.move_pen(steps))

class ControlUnit(Column):
    def __init__(self, title, labels, button_title):
        children = self.create_children(title, labels, button_title)
        super(ControlUnit, self).__init__(title+'.ctrl', children, [1 for _ in range(len(children))])

    @staticmethod
    def create_children(title, labels, button_title):
        return [
            Label(title+'.ctrl.lbl', title),
            Row(title+'.row1', [
                Label(title+'.ctrl.lbl1', labels[0]),
                NumEntry(title+'.ctrl.ntry1', 0)
            ], [1, 2], BORDERLESS),
            Row(title+'.row2', [
                Label(title+'.ctrl.lbl1', labels[1]),
                NumEntry(title+'.ctrl.ntry2', 0)
            ], [1, 2], BORDERLESS),
            Button(title+'.ctrl.btn', button_title)
        ]

class Logger(Column):
    def __init__(self, name, style=None):
        super(Logger, self).__init__(name, self.get_children(name), [1, 1, 1], style)

    @staticmethod
    def get_children(name):
        return [
            Label(name+'.lbl1', ''),
            Label(name+'.lbl2', ''),
            Label(name+'.lbl3', 'LOG')
        ]
