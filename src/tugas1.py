from pywavefront import visualization
import pywavefront
import os
import ctypes
import pyglet
from pyglet.gl import *

window = pyglet.window.Window(resizable=True)

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
def on_draw():
    window.clear()
    glLoadIdentity()

    glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-1.0, 1.0, 1.0, 0.0))
    glEnable(GL_LIGHT0)

    glTranslated(0.0, 0.0, -100.0)
    glRotatef(rotation, 0.0, 1.0, 0.0)
    glRotatef(-25.0, 1.0, 0.0, 0.0)
    glRotatef(45.0, 0.0, 0.0, 1.0)

    glEnable(GL_LIGHTING)

    visualization.draw(meshes)

def update(dt):
    global rotation
    rotation += 90.0 * dt

    if rotation > 720.0:
        rotation = 0.0

if __name__ == "__main__":
    old_dir = "/objects"
    mod_dir = "/data"
    file_abspath = os.path.join(os.getcwd(), "/data/biplane.obj")
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
