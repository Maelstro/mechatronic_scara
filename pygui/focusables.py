from pygui import gui
from pygui.clickables import Clickable

class Focusable(Clickable):
    '''
    This class implements abstract GUI element that can be focused (receive keyboard input).
    '''
    def on_click(self):
        super(Focusable, self).on_click()
        self.focus()

    @property
    def is_focused(self):
        return gui.focused_element == self

    def focus(self):
        gui.focused_element = self

    def unfocus(self):
        gui.focused_element = None

    def on_key(self):
        raise NotImplementedError

class Entry(Focusable):
    '''
    This class implements Entry element, which displays a text that can be edited.
    '''
    def __init__(self, name, initial_text, style=None):
        super(Entry, self).__init__(name, style)
        self.text = initial_text
        self._text_when_focused = initial_text
        self.validate = lambda text: text != ''

    def focus(self):
        super(Entry, self).focus()
        self._text_when_focused = self.text

    def unfocus(self):
        super(Entry, self).unfocus()
        if self.validate(self._text_when_focused):
            self.text = self._text_when_focused

    def on_key(self):
        if key in (ENTER, ESC, RETURN):
            self.unfocus()
        elif key == BACKSPACE:
            self._text_when_focused = self._text_when_focused[:-1]
        elif key == DELETE:
            self._text_when_focused = ''
        elif key != CODED:
            self._text_when_focused += key

    def render(self):
        with self.style, self.pos as (w, h):
            if self.is_focused:
                text_color = self.style.colors.fill
                fill_color = self.style.colors.text
                txt = self._text_when_focused
            elif self.is_clicked:
                text_color = self.style.colors.text
                fill_color = self.style.colors.clicked
                txt = self.text
            elif self.is_hovered:
                text_color = self.style.colors.text
                fill_color = self.style.colors.hovered
                txt = self.text
            else:
                text_color = self.style.colors.text
                fill_color = self.style.colors.fill
                txt = self.text
            fill(*fill_color)
            rect(0, 0, w, h, self.style.rounding)
            fill(*text_color)
            textSize(0.6*h)
            textAlign(CENTER, TOP)
            text(txt, 0.5*w, 0.15*h)

class NumEntry(Entry):
    '''
    This class implements NumEntry element, which displays a numerical __value that can be edited.
    '''
    def __init__(self, name, initial_value, rounding=2, style=None):
        super(NumEntry, self).__init__(name, str(initial_value), style)
        self.__value = initial_value
        self.rounding = rounding

    def focus(self):
        super(NumEntry, self).focus()
        self._text_when_focused = self.text

    def unfocus(self):
        try:
            self.__value = float(self._text_when_focused)
        except ValueError:
            pass
        super(NumEntry, self).unfocus()
        self.text = str(round(self.__value, self.rounding))
        if self.text.endswith('.0'):
            self.text = self.text[:-2]

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            self.__value = float(value)
        except ValueError:
            pass
        else:
            self.text = str(round(self.__value, self.rounding))
            if self.text.endswith('.0'):
                self.text = self.text[:-2]
