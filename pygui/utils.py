from collections import namedtuple

color_types = 'background fill hovered border clicked focused text'
Colors = namedtuple('Colors', color_types)

class Position(object):
    '''
    This class implements position attribute of an element on the screen.
    '''
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    def __getitem__(self, index):
        return (self.x, self.y, self.w, self.h)[index]

    def is_mouse_in(self, x=None, y=None, w=None, h=None):
        x, y, w, h = (my_pos if pos is None else pos
                      for my_pos, pos in zip(self, (x, y, w, h)))
        return True if x < mouseX < x + w and y < mouseY < y + h else False

    def __enter__(self):
        pushMatrix()
        translate(self.x, self.y)
        return self.w, self.h

    def __exit__(self, exc_type, exc_value, traceback):
        popMatrix()

    def __str__(self):
        return str(tuple(round(c) for c in self))

class Style(object):
    '''
    This class describes all necessary appearance features of a gui element.
    '''
    def __init__(self, colors, border, rounding, padding, spacing):
        self.colors = colors
        self.border, self.rounding = border, rounding
        self.padding, self.spacing = padding, spacing

    def __enter__(self, element=None):
        pushStyle()
        stroke(*self.colors.border)
        strokeWeight(self.border)

    def __exit__(self, exc_type, exc_value, traceback):
        popStyle()

DEFAULT = Style(Colors(background=(255, 255, 255),
                       fill=(150, 150, 150),
                       hovered=(130, 130, 130),
                       border=(100, 100, 100),
                       clicked=(100, 100, 100),
                       focused=(170, 170, 193),
                       text=(191, 191, 191)),
                border=3,
                rounding=5,
                padding=10,
                spacing=5)
