from OpenGL.GLU import *
from OpenGL.GL import *
import numpy
import os, sys
import signal
from .Camera import Camera, CameraController
from . import InputHandler
from . import ShapeBuilder
import traceback
import glfw
import time

name = 'Untitled'
camera = None
camera_controller = None
current_windowid = None
running = False

class ViewSetting:
    WIDTH, HEIGHT = 800, 800
    FOV, ASPECT_RATIO, NEAR, FAR = 60, HEIGHT / WIDTH, 1.0, 2000.0
    CLEAR_COLOR = (0, 0, 0, 1)
    FRAME_RATE = 0
    VSYNC = True

    def apply(self):
        resize_window(current_windowid, self.WIDTH, self.HEIGHT)
        glClearColor(*self.CLEAR_COLOR)

setting = ViewSetting()
time_scale = 1.0

to_render = []

def add_object(obj):
    to_render.append(obj)

def remove_object(obj):
    to_render.remove(obj)

OnUpdate = lambda: None
OnLateUpdate = lambda: None
OnPreRender = lambda: None
OnPostRender = lambda: None
OnLayoutRender = lambda: None
OnExit = lambda: None

def ambient_light(amb = 0.3):
    glEnable(GL_LIGHTING)
    
    global_ambient = [amb, amb, amb, 0.1]
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, global_ambient)

def point_light(x, y, z, amb, diff, spec):
    glEnable(GL_LIGHTING)
    
    light_ambient = [amb, amb, amb, 1.0]
    light_diffuse = [diff, diff, diff, 1.0]
    light_specular = [spec, spec, spec, 1.0]
    
    light_position = [x, y, z, 1.0]
    
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    
    glEnable(GL_LIGHT0); #enable the light after setting the properties
    # glMaterialfv(GL_FRONT, GL_SPECULAR, light_specular)

def handlesignal(signo, frame):
    # Called when termination signal is received.
    global running
    running = False

def exitprog():
    # Exit from the program.
    glfw.terminate()
    # signal.alarm(1)
    OnExit()
    os._exit(0)

def resize_window(window, w, h):
    # Reset the settings.
    global setting
    if w != 0 and h != 0 and (w != setting.WIDTH or h != setting.HEIGHT):
        setting.WIDTH = w
        setting.HEIGHT = h
        setting.ASPECT_RATIO = w / h
        glViewport(0, 0, w * 2, h * 2)

def init_camera(position=(0, 0, -10), rotation=(0, 0, 0)):
    global camera, camera_controller
    camera = Camera(position, rotation)

def init_input():
    InputHandler.initialize_keyboard()
    InputHandler.initialize_mouse()

def init(argv):
    global current_windowid
    if not glfw.init():
        return False

    current_windowid = glfw.create_window(setting.WIDTH, setting.HEIGHT, name, None, None)

    if not current_windowid:
        glfw.terminate()
        return False

    glfw.make_context_current(current_windowid)

    glClearColor(*setting.CLEAR_COLOR)
    glEnableClientState (GL_VERTEX_ARRAY)
    
    signal.signal(signal.SIGINT, handlesignal)
    signal.signal(signal.SIGTERM, handlesignal)

    # glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_NORMALIZE)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_SPECULAR | GL_AMBIENT_AND_DIFFUSE | GL_EMISSION)
    return True

def enable3D():
    glShadeModel(GL_SMOOTH)
    glEnable(GL_BLEND)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # Set view fustrum.
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(setting.FOV, setting.ASPECT_RATIO, setting.NEAR, setting.FAR)
    glMatrixMode(GL_MODELVIEW)

def enable2D():
    glDisable(GL_CULL_FACE)
    glDisable(GL_DEPTH_TEST)
    # Set view fustrum.
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, setting.WIDTH, setting.HEIGHT, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)

def render():
    global running
    if running:
        try:
            # Clear the window.
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            # Render 2D.
            enable3D()
            glPushMatrix()
            camera.matrix.apply()
            OnPreRender()
            for renderable in to_render:
                renderable.pre_render()
            for renderable in to_render:
                renderable.render()
            for renderable in to_render:
                renderable.post_render()
            OnPostRender()
            glPopMatrix()

            # Draw 2D.
            enable2D()
            glPushMatrix()
            OnLayoutRender()
            glPopMatrix()

            # Swap buffer.
            glfw.swap_buffers(current_windowid)
        except Exception as e:
            running = False
            print(e)
            traceback.print_exc()
            exitprog()
    else:
        exitprog()

def update():
    global running
    if running:
        try:
            for obj in to_render:
                obj.update()
            OnUpdate()
            render()
            OnLateUpdate()
            InputHandler.flush_keys()
        except Exception as e:
            running = False
            print(e)
            traceback.print_exc()
            exitprog()
    else:
        exitprog()

_delta_time = 0.1

def delta_time():
    return _delta_time * time_scale

def start():
    global running
    glfw.set_window_size_callback(current_windowid, resize_window)
    running = True
    if setting.VSYNC:
        # V Sync
        glfw.swap_interval(1)

    while running:
        if glfw.window_should_close(current_windowid):
            running = False
        else:
            start = time.time()
            update()
            glfw.poll_events()
            end = time.time()

            _delta_time = (end - start)

            if setting.FRAME_RATE > 0:
                # Synchronize FPS.
                interval = 1 / setting.FRAME_RATE
                delay = interval - _delta_time
                if delay > 0:
                    time.sleep(delay)
                    _delta_time = interval

    exitprog()