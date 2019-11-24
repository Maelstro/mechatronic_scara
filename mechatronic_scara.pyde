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

@callback('up.btn')
def pen_up():
    layout.pen_up(True)

@callback('down.btn')
def pen_down():
    layout.pen_up(False)

@callback('Joint.ctrl.btn')
def move_joint():
    layout.move_angles()

@callback('Cartesian.ctrl.btn')
def move_cartesian():
    layout.move_cartesian()

@callback('Joint.ctrl.tgl')
def enable_manual_joint():
    if gui.elements['Joint.ctrl'].is_manual():
        layout.robot.move_manual_joint(enable=True)
    else:
        layout.robot.move_manual_joint(enable=False)

@callback('Cartesian.ctrl.tgl')
def enable_manual_cartesian():
    if gui.elements['Cartesian.ctrl'].is_manual():
        layout.robot.move_manual_cartesian(enable=True)
    else:
        layout.robot.move_manual_cartesian(enable=False)

@callback('square.btn')
def draw_square():
    layout.move_square()

@callback('circle.btn')
def draw_circle():
    layout.move_circle()

def setup():
    # size(1300, 600)
    fullScreen(P3D)
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
        layout.robot.move_manual_joint(key=key)
    if gui.elements['Cartesian.ctrl'].is_manual():
        layout.robot.move_manual_cartesian(key=key)
    if key == 'h':
        layout.robot.draw_circle_in_a_square(*(gui.elements['square.p'+str(i)].value for i in range(4)))
