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
                                  caption='Biplane model Help', visible=False)
lightfv = ctypes.c_float * 4
rotation = 0
meshes = ""

keys = {
    'left':False,
    'right':False,
    'x': False,
    'y':False,
    'z':False,
    'ctrl':False,
    'h':False,
    'home':False,
    'i':False,
    'o':False,
}

rotation_x, rotation_y, rotation_z = 0, 0, 0
radius = -20
camera_x, camera_y, camera_z = 0, 0, radius
current_camera_rotation = 0

# Define functions and main methods

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
    if symbol == key.H:
        keys['h'] = True
    if symbol == key.I:
        keys['i'] = True
    if symbol == key.O:
        keys['o'] = True

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
    if symbol == key.H:
        keys['h'] = False
    if symbol == key.I:
        keys['i'] = False
    if symbol == key.O:
        keys['o'] = False

@window_main.event
def on_draw():
    window_main.clear()
    glLoadIdentity()

    # glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-1.0, 1.0, 1.0, 0.0))
    # glEnable(GL_LIGHT0)

    gluLookAt(camera_x, camera_y, camera_z, 0, 0, 0, 0, 1, 0)

    glTranslated(0.0, 0.0, 0.0)
    glRotatef(rotation_x, 1.0, 0.0, 0.0)
    glRotatef(rotation_y, 0.0, 1.0, 0.0)
    glRotatef(rotation_z, 0.0, 0.0, 1.0)

    # glEnable(GL_LIGHTING)

    visualization.draw(meshes)

def update(dt):
    global rotation_x, rotation_y, rotation_z
    global current_camera_rotation, radius, camera_x, camera_z

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
        if radius > -10:
            radius += 1
            camera_z += 1
    
    if keys['o']: # Key o = zoom out
        if radius < 50:
            radius -= 1
            camera_z -= 1

    if keys['left']: # Key left = Rotate camera to the left in a circle
        #operate on the angle, get new position
        current_camera_rotation -= 2 * dt
        camera_x = radius * math.sin(current_camera_rotation)
        camera_z = radius * math.cos(current_camera_rotation)

        

    if keys['right']: # Key right = Rotate camera to the right in a circle
        #operate on the angle, get new position
        current_camera_rotation += 2 * dt
        camera_x = radius * math.sin(current_camera_rotation)
        camera_z = radius * math.cos(current_camera_rotation)

        

    # if not keys['x']:
    #     rotation_x = 0

    # if not keys['y']:
    #     rotation_y = 0

    # if not keys['z']:
    #     rotation_z = 0

    print(current_camera_rotation, camera_x, camera_z)

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
