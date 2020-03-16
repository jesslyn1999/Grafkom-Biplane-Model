import LSEngine
import os
import LSEngine.LSOParser as LSOParser
import sys
import LSEngine
from LSEngine.Camera import CameraController, Camera
import LSEngine.ShapeBuilder as ShapeBuilder
from OpenGL.GL import *
from LSEngine.Primitives import lerp, gradience
from LSEngine.Behaviour import LSObject
from LSEngine.Mesh import ImmediateMeshRenderer, MeshRenderer, Shader, solidcolor_fragment, solidcolor_vertex
import LSEngine.InputHandler as Input
import LSEngine.InputHandler.Key as Key

import math
import time

counter = 0
day_color = (0.5, 0.8, 1, 1)
night_color = (0.1, 0.2, 0.3, 1)
day_length = 100
rotate_speed = 180
traversed = 0
road_thickness = 0.5
road_width = 30
road_segments = 40
road_segment_length = 5
pavement_thickness = 1.5
pavement_width = 5
tiles = []
zoom_speed = 2

frame_count = 0
start_time = 0

def update():
    # global counter, traversed, tiles
    # counter += LSEngine.delta_time()
    # LSEngine.setting.CLEAR_COLOR = gradience([day_color, night_color, night_color, day_color], [day_length / 4, day_length / 4 * 2, day_length / 4 * 3, day_length], counter % day_length)
    # LSEngine.setting.apply()
    # r_speed = -rotate_speed * LSEngine.delta_time()
    # frontRight.transform.rotate(0, r_speed, 0)
    # backRight.transform.rotate(0, r_speed, 0)
    # frontLeft.transform.rotate(0, r_speed, 0)
    # backLeft.transform.rotate(0, r_speed, 0)
    # move_speed = (-r_speed / 360) * 2 * 2 * math.pi
    # road.transform.translate(-move_speed, 0, 0)
    # traversed += move_speed
    # while traversed > road_segment_length:
    #     tiles[0].transform.translate(len(tiles) * road_segment_length, 0, 0)
    #     tiles.append(tiles.pop(0))
    #     traversed -= road_segment_length
    # while traversed > road_segment_length:
    #     tiles[0].transform.translate(len(tiles) * road_segment_length, 0, 0)
    #     tiles.append(tiles.pop(0))
    #     traversed -= road_segment_length
    # global frame_count
    # frame_count += 1
    
    if Input.is_key_down(Key.key_O): # Key O = Zoom Out
        current_camera_z = camera.get_position()[2]
        if(current_camera_z <= 120):
            camera.set_position((0, 5, current_camera_z + zoom_speed))
            LSEngine.init_camera(camera.get_position(), camera.get_rotation())

    if Input.is_key_down(Key.key_I): # Key I = Zoom In
        current_camera_z = camera.get_position()[2]
        if(current_camera_z >= 30):
            camera.set_position((0, 5, current_camera_z - zoom_speed))
            LSEngine.init_camera(camera.get_position(), camera.get_rotation())

    if Input.is_key_down(Key.key_I): # Key I = Zoom In
        current_camera_z = camera.get_position()[2]
        if(current_camera_z >= 30):
            camera.set_position((0, 5, current_camera_z - zoom_speed))
            LSEngine.init_camera(camera.get_position(), camera.get_rotation())

    if Input.is_key_down(Key.key_I): # Key I = Zoom In
        current_camera_z = camera.get_position()[2]
        if(current_camera_z >= 30):
            camera.set_position((0, 5, current_camera_z - zoom_speed))
            LSEngine.init_camera(camera.get_position(), camera.get_rotation())

if __name__ == "__main__":
    #init window configs
    LSEngine.name = "Our Trial Bro"
    LSEngine.setting.CLEAR_COLOR = (1, 0.8, 0.1, 1)
    LSEngine.init(sys.argv)
    LSEngine.init_camera((0, 0, 30), (0, 0, 0))
    LSEngine.init_input()
    LSEngine.OnUpdate = update

    #define cube
    cube = ShapeBuilder.MakeImmediateRenderObject(LSOParser.LoadLSO(os.path.join(os.getcwd(), "../objects/car.lso")))
    mr = cube.get_component(ImmediateMeshRenderer)
    mr.tint_color = (0.2, 0.3, 0.5, 1)
    cube.transform.translate(0, 0, 0)

    # frontLeft = ShapeBuilder.GenerateImmediateRenderObject(ShapeBuilder.GenerateCylinder, 2, 2, 36)
    # frontLeft.transform.rotate(90, 0, 0)
    # frontLeft.transform.translate(5, 0, -3.1)
    # frontLeft.transform.setParent(cube.transform)
    #add cube
    LSEngine.to_render.append(cube)

    def on_exit():
        end_time = time.time()
        total_time = end_time - start_time
        camera_controller.stop_listening()
        if frame_count > 0:
            print("{} frames over {:0.4} seconds, avg frame per second: {}.".format(frame_count, total_time, int(frame_count/total_time)))

    camera = Camera((0, 5, 70), (0, 0, 0))
    camera_controller = CameraController(LSEngine.camera, 10, 150)
    camera_controller.start()

    #start main loop
    LSEngine.start()
    