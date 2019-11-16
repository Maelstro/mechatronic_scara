from pygui import gui
from pygui.elements import Element

class Clickable(Element):
    '''
    This class implements abtract GUI element that can be clicked.
    '''
    @property
    def is_clicked(self):
        return gui.clicked_element == self

    def on_click(self):
        gui.clicked_element = self

    def on_release(self):
        gui.clicked_element = None

class Button(Clickable):
    '''
    This class implements Button element, which calls callback when clicked.
    '''
    def __init__(self, name, text, style=None):
        super(Button, self).__init__(name, style)
        self.text = text
        self.__callback = lambda: None
        self.__args = ()
        self.__kwargs = {}

    def on_click(self):
        super(Button, self).on_click()
        self.__callback(*self.__args, **self.__kwargs)

    def add_callback(self, callback, *args, **kwargs):
        if callable(callback):
            self.__callback, self.__args, self.__kwargs = callback, args, kwargs
        else:
            raise TypeError('Callback needs to be callable.')

    def render(self):
        with self.style, self.pos as (w, h):
            if self.is_clicked: fill(*self.style.colors.clicked)
            elif self.is_hovered: fill(*self.style.colors.hovered)
            else: fill(*self.style.colors.fill)
            rect(0, 0, w, h, self.style.rounding)
            fill(*self.style.colors.text)
            textSize(0.6*h)
            textAlign(CENTER, TOP)
            text(self.text, 0.5*w, 0.15*h)

class BistableButton(Clickable):
    '''
    This class implements Button element, which stays pressed after click.
    '''
    def __init__(self, name, text, initial_state, style=None):
        super(BistableButton, self).__init__(name, style)
        self.text = text
        self.is_pressed = initial_state

    def on_click(self):
        super(BistableButton, self).on_click()
        self.is_pressed = not self.is_pressed

    def render(self):
        with self.style, self.pos as (w, h):
            if self.is_clicked: fill(*self.style.colors.clicked)
            elif self.is_hovered: fill(*self.style.colors.hovered)
            elif self.is_pressed: fill(*self.style.colors.text)
            else: fill(*self.style.colors.fill)
            rect(0, 0, w, h, self.style.rounding)
            if self.is_pressed: fill(*self.style.colors.fill)
            else: fill(*self.style.colors.text)
            textSize(0.6*h)
            textAlign(CENTER, TOP)
            text(self.text, 0.5*w, 0.15*h)

class Toggle(Clickable):
    '''
    This class implements Toggle element, which toggles its value True/False when clicked.
    '''
    def __init__(self, name, initial_value, text, style=None):
        super(Toggle, self).__init__(name, style)
        self.value = initial_value
        self.text = text

    def update_hover(self):
        if self.pos.is_mouse_in(x=self.pos.x+0.7*self.pos.w):
            gui.hovered_element = self
            return True
        return False

    def on_click(self):
        super(Toggle, self).on_click()
        self.value = not self.value

    def render(self):
        with self.style, self.pos as (w, h):
            fill(*self.style.colors.text)
            textSize(0.6*h)
            textAlign(LEFT, TOP)
            text(self.text, 0, 0.15*h)
            stroke(*self.style.colors.fill)
            strokeWeight(0.2*h)
            line(0.8*w, 0.5*h, 0.9*w, 0.5*h)
            strokeWeight(self.style.border)
            stroke(*self.style.colors.border)
            if self.is_hovered: fill(*self.style.colors.hovered)
            else: fill(*self.style.colors.fill)
            ellipse((0.9 if self.value else 0.8)*w, 0.5*h, 0.4*h, 0.4*h)

class Slider(Clickable):
    '''
    This class implements Slider element, which computes its value based on slider position.
    '''
    def __init__(self, name, minimum, maximum, style=None):
        super(Slider, self).__init__(name, style)
        self.min, self.max = minimum, maximum
        self.value = (minimum + maximum)/2

    def update_hover(self):
        x, y, w, h = self.pos
        slider_pos = map(self.value, self.min, self.max, x+0.1*w, x+0.9*w)
        if self.pos.is_mouse_in(slider_pos-0.2*h, y+0.1*h, 0.4*h, 0.8*h):
            gui.hovered_element = self
            return True
        return False

    def render(self):
        '''
        This method renders the Slider.
        '''
        with self.style, self.pos as (w, h):
            stroke(*self.style.colors.fill)
            strokeWeight(0.2*h)
            fill(*self.style.colors.fill)
            line(0.1*w, h/2, 0.9*w, h/2)
            ellipse(0.1*w, h/2, h*0.2, h*0.2)
            ellipse(0.9*w, h/2, h*0.2, h*0.2)
            if self.is_clicked:
                fill(*self.style.colors.clicked)
                slider_pos = constrain(mouseX, self.pos.x+0.1*w, self.pos.x+0.9*w)
                self.value = map(slider_pos-self.pos.x, 0.1*w, 0.9*w, self.min, self.max)
            elif self.is_hovered:
                fill(*self.style.colors.hovered)
                slider_pos = map(self.value, self.min, self.max, self.pos.x+0.1*w, self.pos.x+0.9*w)
            else:
                fill(*self.style.colors.fill)
                slider_pos = map(self.value, self.min, self.max, self.pos.x+0.1*w, self.pos.x+0.9*w)
            stroke(*self.style.colors.border)
            strokeWeight(self.style.border)
            rectMode(CENTER)
            rect(slider_pos-self.pos.x, h/2, 0.4*h, 0.8*h, self.style.rounding)
