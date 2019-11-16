from pygui import *
from robot import Robot
from layout import ControlGui
import time, struct
add_library('serial')
port = None


DEFAULT = Style(Colors(background=(20, 20, 20),
                       fill=(37, 120, 157),
                       hovered=(25, 104, 139),
                       border=(15, 60, 80),
                       clicked=(15, 60, 80),
                       focused=(170, 170, 193),
                       text=(191, 191, 203)), 2, 5, 10, 15)

scara = Robot(arm_1=10, arm_2=10, height=5)
layout = ControlGui(scara)
gui.root_element = layout.gui

@callback('connect.btn')
def connect():
    global layout
    # layout.connect()
    global port
    port = Serial(this, 'COM6', 460800)
    layout.log('CONNECTED')

@callback('Joint.ctrl.btn')
def move_joint():
    global port
    message = struct.pack('<ccc', '1', '0', '0')
    # print('SENDING', message, message)
    port.clear()
    port.write(message)
    # time.sleep(0.1)
    port.write(message)
    # ControlGui.move_angles(layout)

@callback('Cartesian.ctrl.btn')
def move_cartesian():
    global port
    print(port.readString())
    # ControlGui.move_angles(layout)

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
