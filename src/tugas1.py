from pywavefront import visualization
import pywavefront
import os
import ctypes
import pyglet
from pyglet.gl import *
from pyglet.window import key


window = pyglet.window.Window(resizable=True)

keys = {
    'left':False,
    'right':False,
    'x': False,
    'y':False,
    'z':False
}

rotation_x, rotation_y, rotation_z = 0, 0, 0

@window.event
def on_resize(width, height):
    viewport_width, viewport_height = window.get_framebuffer_size()
    glViewport(0, 0, viewport_width, viewport_height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60., float(width) / height, 1., 100.)
    glMatrixMode(GL_MODELVIEW)
    return True

@window.event
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

@window.event
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

@window.event
def on_draw():
    window.clear()
    glLoadIdentity()

    # glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-1.0, 1.0, 1.0, 0.0))
    # glEnable(GL_LIGHT0)

    glTranslated(0.0, 0.0, -100.0)
    glRotatef(rotation_x, 1.0, 0.0, 0.0)
    glRotatef(rotation_y, 0.0, 1.0, 0.0)
    glRotatef(rotation_z, 0.0, 0.0, 1.0)

    # glEnable(GL_LIGHTING)

    visualization.draw(meshes)

def update(dt):
    global rotation_x, rotation_y, rotation_z
    
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

    # if not keys['x']:    
    #     rotation_x = 0

    # if not keys['y']:    
    #     rotation_y = 0

    # if not keys['z']:    
    #     rotation_z = 0

if __name__ == "__main__":
    file_abspath = os.path.join(os.getcwd(), "../data/biplane.obj")
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

    rotation = 0
    meshes = pywavefront.Wavefront(file_abspath)
    lightfv = ctypes.c_float * 4

    pyglet.clock.schedule(update)
    pyglet.app.run()
