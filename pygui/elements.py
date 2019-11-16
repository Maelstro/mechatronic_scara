from pygui import gui
from pygui.utils import Position
#just Jython things
class Object(object): pass

class Element(Object):
    '''
    This class implements generic Element, the parent class for all GUI elements.
    '''
    def __init__(self, name, style):
        gui.elements[name] = self
        self.name = name
        self.style = style
        self.pos = None
        self.__is_visible = True

    def initialize(self, pos, style):
        self.pos = Position(*pos)
        if self.style is None:
            self.style = style

    @property
    def is_visible(self):
        return self.__is_visible

    def show(self):
        self.__is_visible = True

    def hide(self):
        self.__is_visible = False

    @property
    def is_hovered(self):
        return gui.hovered_element == self

    def update_hover(self):
        if self.pos.is_mouse_in():
            gui.hovered_element = self
            return True
        return False

    def render(self):
        pass

    def __str__(self):
        return str(self.__class__.__name__) + "('" + self.name + "', " + str(self.pos) + ')'

class Label(Element):
    '''
    This class implements Label element, which displays short text.
    '''
    def __init__(self, name, text, style=None):
        super(Label, self).__init__(name, style)
        self.text = text

    def render(self):
        with self.style, self.pos as (_, h):
            fill(*self.style.colors.text)
            textSize(0.6*h)
            textAlign(LEFT, TOP)
            text(self.text, 0, 0.15*h)

class Bar(Element):
    '''
    This class implements Bar element, which shows progress bar based on a value 0-1.
    '''
    def __init__(self, name, style=None):
        super(Bar, self).__init__(name, style)
        self.__value = 0

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = constrain(value, 0, 1)

    def render(self):
        with self.style, self.pos as (w, h):
            fill(*self.style.colors.background)
            rect(0, 0, w, h, self.style.rounding)
            fill(*self.style.colors.fill)
            strokeWeight(0)
            rect(0.1*h, 0.1*h, (w-0.2*h)*self.value, 0.8*h, self.style.rounding)
