from pygui import *
from robot import Robot
from layout import ControlGui
from styles import DEFAULT

layout = ControlGui(Robot(arm_1=137.5, arm_2=90, offset=40))
gui.root_element = layout

@callback('connect.btn')
def connect():
    layout.connect()

@callback('calibrate.btn')
def reset():
    layout.reset_encoders()

@callback('read.btn')
def read_serial():
    print(layout.robot.read_port())

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

def setup():
    size(1300, 600)
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
