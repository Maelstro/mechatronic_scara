from pygui import *

class ControlGui:
    def __init__(self, robot):
        self.robot = robot
        self.gui = self.create_gui()

    @staticmethod
    def create_gui():
        return Column('main_col', [
            Row('up_row', [
                Label('title', 'SCARA'),
                Row('port', [
                    Label('port.lbl', 'PORT'),
                    Entry('port.ntry', 'COM6')
                ], [1, 2.5]),
                Button('connect.btn', 'Connect')
            ], [1, 1, 1]),
            Row('low_row', [
                ControlUnit('Joint', ['theta', 'gamma'], 'Move'),
                ControlUnit('Cartesian', ['X', 'Y'], 'Move'),
            ], [1, 1]),
            Logger('logger')
        ], [1, 4, 1])

    def log(self, text):
        print('KURWA CHUJ')
        lbl_1, lbl_2, lbl_3 = gui.elements['logger.lbl1'], gui.elements['logger.lbl2'], gui.elements['logger.lbl3'] 
        lbl_1.text = lbl_2.text
        lbl_2.text = lbl_3.text
        lbl_3.text = text

    def connect(self):
        if self.robot.connect(gui.elements['port.ntry'].text):
            self.log('CONNECTED')
        else:
            self.log('CONNECTION FAILED')

    def move_angles(self):
        theta = gui.elements['Joint.ctrl.ntry1'].value
        gamma = gui.elements['Joint.ctrl.ntry2'].value
        self.log('SENDING SERIAL JOINT MOVE: ' + str(int(theta)) + ', ' + str(int(gamma)))
        self.robot.move_to(angles=(theta, gamma))

    def move_cartesian(self):
        x = gui.elements['Cartesian.ctrl.ntry1'].value
        y = gui.elements['Cartesian.ctrl.ntry2'].value
        self.robot.move_to(pos=(x, y))
        self.log('SENDING SERIAL CARTESIAN MOVE: ' + str(int(x)) + ', ' + str(int(y)))

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
            ], [1, 2.5]),
            Row(title+'.row2', [
                Label(title+'.ctrl.lbl1', labels[1]),
                NumEntry(title+'.ctrl.ntry2', 0)
            ], [1, 2.5]),
            Button(title+'.ctrl.btn', button_title)
        ]

class Logger(Column):
    def __init__(self, name):
        children = self.get_children(name)
        super(Logger, self).__init__(name, children, [1, 1, 1])

    def get_children(self, name):
        return [
            Label(name+'.lbl1', ''),
            Label(name+'.lbl2', ''),
            Label(name+'.lbl3', 'LOG')
        ]
