from pygui import *
from styles import BORDERLESS

class ControlGui(Column):
    def __init__(self, robot):
        super(ControlGui, self).__init__('main', self.create_children(), [1, 1, 5, 3])
        self.robot = robot

    @staticmethod
    def create_children():
        return [
            Label('title', 22*' '+'DRAWING SCARA CONTROL STATION'),
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
                        Button('down.btn', 'DOWN'),
                        NumEntry('down.ntry', 590),
                    ], [1, 1, 1, 1]),
                    Row('sqare.row', [
                        Button('square.btn', 'Rect'),
                        NumEntry('square.p0', 0),
                        NumEntry('square.p1', 0),
                        NumEntry('square.p2', 0),
                        NumEntry('square.p3', 0),
                    ], [2, 1, 1, 1, 1]),
                    Row('circle.row', [
                        Button('circle.btn', 'Circle'),
                        NumEntry('circle.p0', 0),
                        NumEntry('circle.p1', 0),
                        NumEntry('circle.p2', 0),
                    ], [2, 1, 1, 1])
                ], [1, 1, 1, 1, 1])
            ], [1, 1, 1]),
            Logger('logger', BORDERLESS)
        ]

    def log(self, text):
        gui.elements['logger'].log(text)

    def connect(self):
        port = gui.elements['port.ntry'].text
        self.log('[ GUI ] CONNECTING TO PORT ' + port)
        self.log(self.robot.connect(port))

    def reset_encoders(self):
        self.log('[ GUI ] RESETTING ENCODERS')
        self.log(self.robot.reset_encoders())

    def read_serial(self):
        self.log('[SERIAL] ' + str(self.robot.read_port()))

    def pen_up(self, up):
        entry = 'up.ntry' if up else 'down.ntry'
        steps = int(gui.elements[entry].value)
        self.log('[ GUI ] MOVING PEN TO ' + str(steps))
        self.log(self.robot.move_pen(steps))

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

    def move_square(self):
        x_1, y_1, x_n, y_n = [gui.elements['square.p'+str(i)].value for i in range(4)]
        self.log(self.robot.move_square(x_1, y_1, x_n, y_n))

    def move_circle(self):
        r, x, y = [gui.elements['circle.p'+str(i)].value for i in range(3)]
        self.log(self.robot.move_circle(r, x, y))

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
            Button(title+'.ctrl.btn', button_title),
            Row(title+'.ctrl.mode', [
                Toggle(title+'.ctrl.tgl', False, 'Automatic'),
                Label(title+'ctrl.lbl2', '  Manual')
            ], [1.8, 1], BORDERLESS)
        ]

    def is_manual(self):
        return gui.elements[self.name+'.tgl'].value

class Logger(Column):
    def __init__(self, name, style=None):
        super(Logger, self).__init__(name, self.get_children(name), [1 for _ in range(1, 8)], style)

    @staticmethod
    def get_children(name):
        return [
            Label(name+'.lbl1', ''),
            Label(name+'.lbl2', ''),
            Label(name+'.lbl3', ''),
            Label(name+'.lbl4', ''),
            Label(name+'.lbl5', ''),
            Label(name+'.lbl6', ''),
            Label(name+'.lbl7', '')
        ]

    def log(self, text):
        lbl_1, lbl_2, lbl_3, lbl_4, lbl_5, lbl_6, lbl_7 = self._children
        lbl_1.text = lbl_2.text
        lbl_2.text = lbl_3.text
        lbl_3.text = lbl_4.text
        lbl_4.text = lbl_5.text
        lbl_5.text = lbl_6.text
        lbl_6.text = lbl_7.text
        lbl_7.text = text
