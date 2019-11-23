import time
from pygui import *
from robot import Robot
from layout import ControlGui
from styles import DEFAULT

layout = ControlGui(Robot(arm_1=137.5, arm_2=100, offset=41))
gui.root_element = layout

@callback('connect.btn')
def connect():
    layout.connect()

@callback('calibrate.btn')
def reset():
    layout.reset_encoders()

@callback('read.btn')
def read_serial():
    layout.read_serial()

@callback('Joint.ctrl.btn')
def move_joint():
    layout.move_angles()

@callback('Cartesian.ctrl.btn')
def move_cartesian():
    layout.move_cartesian()

@callback('up.btn')
def pen_up():
    layout.pen_up(True)

@callback('down.btn')
def pen_down():
    layout.pen_up(False)

@callback('Joint.ctrl.tgl')
def enable_manual():
    if gui.elements['Joint.ctrl'].is_manual():
        layout.robot.move_manual(enable=True)
    else:
        layout.robot.move_manual(enable=False)

def setup():
    # size(1300, 600)
    fullScreen()
    gui.initialize((0, 0, width, height), DEFAULT)

def draw():
    background(0)
    gui.render()

def mouseMoved():
    gui.update_hover()

def mousePressed():
    gui.on_click()

def mouseReleased():
    gui.on_release()

def keyPressed():
    gui.on_key()
    if gui.elements['Joint.ctrl'].is_manual():
        layout.robot.move_manual(key=key)
    if key == 'h':
        layout.robot.move_circle(50, 140, 10)
    # if key == 'f':
    #     layout.robot.move_cartesian(50, 100)
    #     time.sleep(0.5)
    #     layout.robot.move_cartesian(50, 160)
    #     time.sleep(0.5)
    #     layout.robot.move_cartesian(-70, 160)
    #     time.sleep(0.5)
    #     layout.robot.move_cartesian(-70, 100)
    # if key == 'q':
    #     while keyPressed:
    #         # layout.robot.read_angles()
    #         theta, gamma = layout.robot.read_angles()
    #         layout.robot.move_angles(theta+10, gamma)
