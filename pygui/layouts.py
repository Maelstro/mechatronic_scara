from pygui.elements import Element
from pygui.clickables import Button

class Layout(Element):
    '''
    This class implements abstract GUI element that can store and manage other elements.
    '''
    def __init__(self, name, children, weights, style=None):
        super(Layout, self).__init__(name, style)
        self._children = list(children)
        self._weights = list(weights)

    def show(self):
        super(Layout, self).show()
        for child in self._children:
            child.show()

    def hide(self):
        super(Layout, self).hide()
        for child in self._children:
            child.hide()

    def update_hover(self):
        if self.pos.is_mouse_in():
            for child in self._children:
                if child.is_visible and child.update_hover():
                    return True
        return False

    def render(self):
        with self.style, self.pos as (w, h):
            strokeWeight(0)
            fill(*self.style.colors.background)
            rect(0, 0, w, h, self.style.rounding)
        for child in self._children:
            if child.is_visible:
                child.render()

class Margin(Layout):
    '''
    This class implements Margin container, which stores its child with margins around.
    '''
    def __init__(self, name, child, margins, style=None):
        super(Margin, self).__init__(name, child, 1, style)
        self.left, self.right, self.upper, self.lower = margins

    def initialize(self, pos, style):
        super(Margin, self).initialize(pos, style)
        ppw_horizontal = self.pos.w/(self.left + 1 + self.right)
        ppw_vertical = self.pos.h/(self.upper + 1 + self.lower)
        self._children[0].initialize((
            self.pos.x+ppw_horizontal*self.left,
            self.pos.y+ppw_vertical*self.upper,
            ppw_horizontal,
            ppw_vertical
        ), self.style)

class Column(Layout):
    '''
    This class implements Column container, which renders its children vertically.
    '''
    def initialize(self, pos, style):
        super(Column, self).initialize(pos, style)
        ppw = (self.pos.h-2*self.style.padding-(len(self._children)-1)*self.style.spacing)/sum(self._weights)
        for i, child in enumerate(self._children):
            child.initialize((
                self.pos.x+self.style.padding,
                self.pos.y+self.style.padding+sum(self._weights[:i])*ppw+i*self.style.spacing,
                self.pos.w-2*self.style.padding,
                self._weights[i]*ppw
            ), self.style)

class Row(Layout):
    '''
    This class implements Row container, which renders its children horizontally.
    '''
    def initialize(self, pos, style=None):
        super(Row, self).initialize(pos, style)
        ppw = (self.pos.w-2*self.style.padding-(len(self._weights)-1)*self.style.spacing)/sum(self._weights)
        for i, child in enumerate(self._children):
            child.initialize((
                self.pos.x+self.style.padding+sum(self._weights[:i])*ppw+i*self.style.spacing,
                self.pos.y+self.style.padding,
                self._weights[i]*ppw,
                self.pos.h-2*self.style.padding
            ), self.style)

class Tab(Layout):
    def __init__(self, name, elements, bar_height, style=None):
        self._elements = list(elements[1::2])
        self._labels = list(elements[::2])
        self._bar_height = bar_height
        super(Tab, self).__init__(name, self._create_children(name), 0, 0, style)

    def _create_children(self, name):
        buttons = []
        for i, label in enumerate(self._labels):
            btn = Button(name+'.btn'+str(i), label)
            btn.add_callback(self.set_active_child, i)
            buttons.extend([1, btn])
        row = Row(name+'.row', buttons, 0, 0)
        return (self._bar_height, row, 1, self._elements[0])

    def initialize(self, pos, style=None):
        super(Tab, self).initialize(pos, style)
        bar_height = self._bar_height*self.pos.h
        self._children[0].initialize((self.pos.x, self.pos.y, self.pos.w, bar_height), self.style)
        for element in self._elements:
            element.initialize((self.pos.x, self.pos.y+bar_height, self.pos.w, self.pos.h-bar_height), self.style)

    def set_active_child(self, index):
        self._children[-1] = self._elements[index]
