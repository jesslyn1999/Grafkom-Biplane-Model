from pywavefront import visualization
import pywavefront
import os
import ctypes
from pyglet.gl import *
from utils.Help import Help
from pyglet.window import key

WINDOW_HELP_WIDTH = 800
WINDOW_HELP_HEIGHT = 600
window_main = pyglet.window.Window(resizable=True)
window_help = pyglet.window.Window(WINDOW_HELP_WIDTH, WINDOW_HELP_HEIGHT,
                                  caption='Biplane model Help', visible=False)
lightfv = ctypes.c_float * 4
rotation = 0
meshes = ""

keys = {
    'x': False,
    'y':False,
    'z':False,
    'ctrl':False,
    'h':False,
    'r': False,
    'up': False,
    'right': False,
    'down': False,
    'left': False,
}

rotation_x, rotation_y, rotation_z = 0, 0, 0
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
    if symbol == key.LEFT:
        keys['left'] = True
    if symbol == key.RIGHT:
        keys['right'] = True
    if symbol == key.X:
        keys['x'] = True
    if symbol == key.Y:
        keys['y'] = True
    if symbol == key.Z:
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

@window_main.event
def on_key_release(symbol, modifiers):
    if symbol == key.LEFT:
        keys['left'] = False
    if symbol == key.RIGHT:
        keys['right'] = False
    if symbol == key.X:
        keys['x'] = False
    if symbol == key.Y:
        keys['y'] = False
    if symbol == key.Z:
        keys['z'] = False
    if symbol == key.H:  # display help window
        keys['h'] = False
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

@window_main.event
def on_draw():
    window_main.clear()
    glLoadIdentity()

    # glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-1.0, 1.0, 1.0, 0.0))
    # glEnable(GL_LIGHT0)

    glTranslated(translation_x, translation_y, translation_z - 80.00)
    glRotatef(rotation_x, 1.0, 0.0, 0.0)
    glRotatef(rotation_y, 0.0, 1.0, 0.0)
    glRotatef(rotation_z, 0.0, 0.0, 1.0)

    # glEnable(GL_LIGHTING)

    visualization.draw(meshes)

def update(dt):
    global rotation_x, rotation_y, rotation_z
    global translation_x, translation_y, translation_z

    if keys['x']:
        rotation_x += 90.0 * dt

        if rotation_x > 360:
            rotation_x = 0.0

    if keys['y']:
        rotation_y += 90.0 * dt

        if rotation_y > 360:
            rotation_y = 0.0

    if keys['z']:
        rotation_z += 90.0 * dt

        if rotation_z > 360:
            rotation_z = 0.0

    if keys['up']:
        translation_y -= 10.0 * dt
    if keys['down']:
        translation_y += 10.0 * dt
    if keys['right']:
        translation_x -= 10.0 * dt
    if keys['left']:
        translation_x += 10.0 * dt


    if keys['h']:
        if not window_help.visible:
            window_help.set_visible()

    if keys['r']:
        print("reset button is pressed")
        rotation_x, rotation_y, rotation_z = 0, 0, 0

    # if not keys['x']:
    #     rotation_x = 0

    # if not keys['y']:
    #     rotation_y = 0

    # if not keys['z']:
    #     rotation_z = 0

if __name__ == "__main__":
    file_abspath = os.path.join(os.getcwd(), "data/biplane_1.obj")
    print("FILE : ", file_abspath)


    # # Iterate vertex data collected in each material
    # for name, material in scene.materials.items():
    #     material.vertex_format
    #     # Contains the vertex list of floats in the format described above
    #     material.vertices
    #     # Material properties
    #     material.diffuse
    #     material.ambient
    #     material.texture
    #
    # visualization.draw(scene)

    help = Help(WINDOW_HELP_WIDTH, WINDOW_HELP_HEIGHT)
    help.show(window_help)

    meshes = pywavefront.Wavefront(file_abspath)

    pyglet.clock.schedule(update)
    pyglet.app.run()
