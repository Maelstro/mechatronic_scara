'''
Pygui's main module managing the root, hovered, clicked and focused elements.
'''
elements = {}
root_element = None
hovered_element = None
clicked_element = None
focused_element = None

def initialize(pos, style):
    root_element.initialize(pos, style)

def render():
    if root_element.is_visible: root_element.render()

def update_hover():
    global hovered_element
    if hovered_element is not None and hovered_element.is_visible:
        if hovered_element.update_hover(): return
    hovered_element = None
    if root_element.is_visible: root_element.update_hover()

def on_click():
    if focused_element is not None: focused_element.unfocus()
    try:
        hovered_element.on_click()
    except AttributeError:
        pass

def on_release():
    if clicked_element is not None: clicked_element.on_release()

def on_key():
    if focused_element is not None: focused_element.on_key()

def callback(name, *args, **kwargs):
    def decorator(func):
        elements[name].add_callback(func, *args, **kwargs)
        return func
    return decorator
