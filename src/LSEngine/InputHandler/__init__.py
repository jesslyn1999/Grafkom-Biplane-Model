import glfw
import LSEngine
import enum

# Keyboard handler
_pressed_key = {}
_key_event_down = {}
_key_event_up = {}

def _key_pressed_callback(window, key, scancode, action, modifier):
    if action == glfw.PRESS:
        _pressed_key[key] = True
        _key_event_down[key] = True
    elif action == glfw.RELEASE:
        _pressed_key[key] = False
        _key_event_up[key] = True

def is_key_down(key):
    '''Returns true if the key is pressed; otherwise false.'''
    return key in _pressed_key and _pressed_key[key]

def is_key_up(key):
    '''Returns false if the key is pressed; otherwise true.'''
    return not is_key_down(key)

def on_key_down(key):
    return key in _key_event_down and _key_event_down[key]

def on_key(key):
    return is_key_down(key)

def on_key_up(key):
    return key in _key_event_up and _key_event_up[key]

def flush_keys():
    for k, _ in _key_event_down.items():
        _key_event_down[k] = False
    for k, _ in _key_event_up.items():
        _key_event_up[k] = False

def initialize_keyboard():
    '''Initialize keyboard event listener to GLUT.'''
    glfw.set_key_callback(LSEngine.current_windowid, _key_pressed_callback)

# Mouse Handler
_pressed_mouse = {}
_mouse_position = (0, 0)

def get_mouse_position():
    return _mouse_position

def get_mouse_x():
    return _mouse_position[0]

def get_mouse_y():
    return _mouse_position[1]

def _mouse(window, button, action, modifier):
    '''Called as mouse action callback from GLFW.'''
    if action == glfw.PRESS:
        _pressed_mouse[button] = True
    elif action == glfw.RELEASE:
        _pressed_mouse[button] = False

def _mouse_pos(window, x, y):
    global _mouse_position
    _mouse_position = (x, y)

def is_mouse_down(button):
    '''Returns true if the button is pressed; otherwise false'''
    return button in _pressed_mouse and _pressed_mouse[button]

def is_mouse_up(button):
    '''Returns false if the button is pressed; otherwise true'''
    return not is_mouse_down(button)

def initialize_mouse():
    '''Initialize mouse event listener to GLUT.'''
    glfw.set_mouse_button_callback(LSEngine.current_windowid, _mouse)
    glfw.set_cursor_pos_callback(LSEngine.current_windowid, _mouse_pos)
    # glutMouseFunc(mouse)
    # glutMotionFunc(mouse_active_drag)
    # glutPassiveMotionFunc(mouse_passive_drag)