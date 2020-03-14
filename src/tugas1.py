from pywavefront import visualization
import pywavefront
import os
import ctypes
from pyglet.gl import *
from utils.Help import Help
from pyglet.window import key
import math

#Define variables 

WINDOW_HELP_WIDTH = 800
WINDOW_HELP_HEIGHT = 600
window_main = pyglet.window.Window(resizable=True)
window_help = pyglet.window.Window(WINDOW_HELP_WIDTH, WINDOW_HELP_HEIGHT,
                                  caption='Biplane model Help', visible=True)
lighting_model = False
texture_model = False

lightfv = ctypes.c_float * 4
rotation = 0
meshes = ""

keys = {
    'x': False,
    'y':False,
    'z':False,
    'shift':False,
    'h':False,
    'r': False,
    'up': False,
    'right': False,
    'down': False,
    'left': False,
    'home':False,
    'i':False,
    'o':False,
    's': False,
}

rotation_x, rotation_y, rotation_z = 0, 0, 0
radius = -20
camera_x, camera_y, camera_z = 0, 0, radius
current_camera_rotation = 0

# Define functions and main methods
translation_x, translation_y, translation_z = 0, 0, 0

@window_main.event
def on_resize(width, height):
    viewport_width, viewport_height = window_main.get_framebuffer_size()
    glViewport(0, 0, viewport_width, viewport_height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60., float(width) / height, 1., 100.)
    glMatrixMode(GL_MODELVIEW)
    return True

@window_main.event
def on_key_press(symbol, modifiers):
    if symbol == key.X: # rotate on x axis
        keys['x'] = True
    if symbol == key.Y: # rotate on y axis
        keys['y'] = True
    if symbol == key.Z: # rotate on z axis
        keys['z'] = True
    if symbol == key.H:  # display help window
        keys['h'] = True
    if symbol == key.R:  # reset model position
        keys['r'] = True
    if symbol == key.UP:  # translate up camera
        keys['up'] = True
    if symbol == key.RIGHT:  # translate right camera
        keys['right'] = True
    if symbol == key.DOWN:  # translate down camera
        keys['down'] = True
    if symbol == key.LEFT:  # translate left camera
        keys['left'] = True
    if symbol == key.I: # zoom-in the model
        keys['i'] = True 
    if symbol == key.O:  # zoom-out the model
        keys['o'] = True
    if symbol == key.LSHIFT or symbol == key.RSHIFT:  # alternate key
        keys['shift'] = True
    if symbol == key.S:  # Enable shade
        keys['s'] = True

@window_main.event
def on_key_release(symbol, modifiers):
    if symbol == key.X: # rotate on x axis
        keys['x'] = False 
    if symbol == key.Y: # rotate on y axis
        keys['y'] = False
    if symbol == key.Z: # rotate on z axis
        keys['z'] = False
    if symbol == key.H:  # display help window
        keys['h'] = False
    if symbol == key.I: # zoom-in the model
        keys['i'] = False 
    if symbol == key.O: # zoom-out the model
        keys['o'] = False
    if symbol == key.R:  # reset model position
        keys['r'] = False
    if symbol == key.UP:  # translate up camera
        keys['up'] = False
    if symbol == key.RIGHT:  # translate right camera
        keys['right'] = False
    if symbol == key.DOWN:  # translate down camera
        keys['down'] = False
    if symbol == key.LEFT:  # translate left camera
        keys['left'] = False
    if symbol == key.LSHIFT or symbol == key.RSHIFT:  # alternate key
        keys['shift'] = False
    if symbol == key.S:  # Enable shade
        keys['s'] = False

@window_main.event
def on_draw():
    window_main.clear()
    glLoadIdentity()

    # glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-1.0, 1.0, 1.0, 0.0))
    # glEnable(GL_LIGHT0)

    gluLookAt(camera_x, camera_y, camera_z, 0, 0, 0, 0, 1, 0)

    glTranslated(translation_x, translation_y, translation_z)
    glRotatef(rotation_x, 1.0, 0.0, 0.0)
    glRotatef(rotation_y, 0.0, 1.0, 0.0)
    glRotatef(rotation_z, 0.0, 0.0, 1.0)

    # glEnable(GL_LIGHTING)

    visualization.draw(meshes, lighting_enabled=lighting_model, textures_enabled=texture_model)

def update(dt):
    global rotation_x, rotation_y, rotation_z
    global current_camera_rotation, radius, camera_x, camera_z
    global translation_x, translation_y, translation_z
    global texture_model, lighting_model

    if keys['x']: # Key x = rotate on x axis
        rotation_x += 90.0 * dt

        if rotation_x > 360:
            rotation_x = 0.0

    if keys['y']: # Key y = rotate on y axis
        rotation_y += 90.0 * dt

        if rotation_y > 360:
            rotation_y = 0.0

    if keys['z']: # Key z = rotate on z axis
        rotation_z += 90.0 * dt

        if rotation_z > 360:
            rotation_z = 0.0

    if keys['h']: # Key h = show help
        if not window_help.visible:
            window_help.set_visible()

    if keys['i']: # Key i = zoom in
        if camera_z < -10:
            radius += 1
            camera_z += 1
    
    if keys['o']: # Key o = zoom out
        if camera_z > -50:
            radius -= 1
            camera_z -= 1

    if keys['up']: #translate model on y 
        translation_y -= 10.0 * dt

    if keys['down']: #translate model on -y
        translation_y += 10.0 * dt

    if keys['right'] and keys['shift']: #translate model on x
        translation_x -= 10.0 * dt

    if keys['left'] and keys['shift']: #translate model on -x
        translation_x += 10.0 * dt
        

    if keys['left'] and not keys['shift']: # Key left = Rotate camera to the left in a circle
        #operate on the angle, get new position
        current_camera_rotation -= 2 * dt
        camera_x = radius * math.sin(current_camera_rotation)
        camera_z = radius * math.cos(current_camera_rotation)


    if keys['right'] and not keys['shift']: # Key right = Rotate camera to the right in a circle
        #operate on the angle, get new position
        current_camera_rotation += 2 * dt
        camera_x = radius * math.sin(current_camera_rotation)
        camera_z = radius * math.cos(current_camera_rotation)


    if keys['r']:
        print("reset button is pressed")
        rotation_x, rotation_y, rotation_z = 0, 0, 0
        radius = -20
        camera_x, camera_y, camera_z = 0, 0, -20
        lighting_model, texture_model = False, False

    if keys['s'] and not keys['shift']:
        print("shading on button is pressed")
        lighting_model, texture_model = True, True

    if keys['s'] and keys['shift']:
        print("shading off button is pressed")
        lighting_model, texture_model = False, False


    # if not keys['x']:
    #     rotation_x = 0

    # if not keys['y']:
    #     rotation_y = 0

    # if not keys['z']:
    #     rotation_z = 0

    # print(current_camera_rotation, camera_x, camera_z)

if __name__ == "__main__":
    file_abspath = os.path.join(os.getcwd(), "data/biplane_shade.obj")
    print("FILE : ", file_abspath)

    help = Help(WINDOW_HELP_WIDTH, WINDOW_HELP_HEIGHT)
    help.show(window_help)

    meshes = pywavefront.Wavefront(file_abspath)

    pyglet.clock.schedule(update)
    pyglet.app.run()
