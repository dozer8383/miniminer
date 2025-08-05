import pyray as pr
import math
from noise import snoise3

pr.set_config_flags(pr.FLAG_MSAA_4X_HINT);
pr.init_window(1920, 1080, "Miniminer")
pr.set_target_fps(144)
pr.disable_cursor()

worldwidth = 40
worldheight = 20
worlddepth = 40
world = []

camera = pr.Camera3D()
camera.position = pr.Vector3(worldwidth/2, worldheight+5, worlddepth/2)
camera.up = pr.Vector3(0, 1, 0)
camera.fovy = 85.0
ymomentum = 0
speed = 0.05
rotspeed = 0.5

groundtex = pr.load_texture("assets/ground.png")

shader = pr.load_shader("assets/vertex.vs", "assets/fragment.fs")
shader.locs[pr.ShaderLocationIndex.SHADER_LOC_MATRIX_MVP] = pr.get_shader_location(shader, "mvp")

block = pr.gen_mesh_cube(1.0, 1.0, 1.0)

ground = pr.load_material_default()
ground.maps[pr.MATERIAL_MAP_DIFFUSE].texture = groundtex

for iz in range(worlddepth):
    world.append([])
    for iy in range(worldheight):
        world[iz].append([])
        for ix in range(worldwidth):
            world[iz][iy].append([])
            if iy > worldheight/2:
                if snoise3(ix/12,iy/12,iz/12,1) < 0-(1*iy/(worldheight)):
                    world[iz][iy][ix] = 1
                else:
                    world[iz][iy][ix] = 0
            else:
                if snoise3(ix/6,iy/6,iz/6,1) > 0.1:
                    world[iz][iy][ix] = 1
                else:
                    world[iz][iy][ix] = 0

while True:
    # pr.update_camera(camera, pr.CAMERA_FIRST_PERSON)
    oldCamPos = camera.position
    pr.update_camera_pro(camera,
                         pr.Vector3(pr.is_key_down(pr.KEY_W)*speed - pr.is_key_down(pr.KEY_S)*speed,
                                    pr.is_key_down(pr.KEY_D)*speed - pr.is_key_down(pr.KEY_A)*speed,
                                    # (pr.is_key_down(pr.KEY_SPACE)*speed - pr.is_key_down(pr.KEY_LEFT_SHIFT)*speed)),
                                    -ymomentum),
                         pr.Vector3(pr.get_mouse_delta().x*rotspeed,
                                    pr.get_mouse_delta().y*rotspeed,
                                    0),
                         0)
                        
    pr.begin_drawing()
    pr.clear_background([50,30,20])
    pr.begin_mode_3d(camera)

    # pr.draw_grid(50, 1)
    for iz in range(worlddepth):
        for iy in range(worldheight):
            for ix in range(worldwidth):
                if world[ix][iy][iz] == 1:
                    try:
                        if not(world[ix+1][iy][iz] != 0 and world[ix-1][iy][iz] != 0 and world[ix][iy+1][iz] != 0 and world[ix][iy-1][iz] != 0 and world[ix][iy][iz+1] != 0 and world[ix][iy][iz-1] != 0):
                            pr.draw_mesh(block,ground,pr.matrix_translate(ix,iy+0.8,iz))
                    except:
                        pr.draw_mesh(block,ground,pr.matrix_translate(ix,iy+0.8,iz))
    
    pr.draw_cube(pr.Vector3(camera.target.x, camera.target.y, camera.target.z), 1, 1, 1, pr.RED)

    pr.end_mode_3d()
    pr.draw_text(f"X:{round(camera.position.x,2)}, Y:{round(camera.position.y)}, Z:{round(camera.position.z)}", 3, 20, 20, pr.WHITE)
    pr.draw_text(f"Xrot:{round(camera.target.x,2)}, Yrot:{round(camera.target.y)}, Zrot:{round(camera.target.z)}", 3, 40, 20, pr.PURPLE)
    pr.draw_fps(3, 3)
    pr.end_drawing()
    if round(camera.position.y)-2 >= worldheight or round(camera.position.y)-2 < 0:
        ymomentum += 0.005
    elif world[round(camera.position.x)][math.floor(camera.position.y)-2][round(camera.position.z)] == 0:
        ymomentum += 0.005
    else:
        ymomentum = 0
        if pr.is_key_down(pr.KEY_SPACE):
            ymomentum = -0.1
        if pr.window_should_close():
            break
    if pr.check_collision_boxes(pr.BoundingBox(pr.Vector3(camera.position.x-0.5, camera.position.y-0.5, camera.position.z-0.5),
                                               pr.Vector3(camera.position.x+0.5, camera.position.y+0.5, camera.position.z+0.5)),
                                 pr.BoundingBox(pr.Vector3(oldCamPos.x-0.5, oldCamPos.y-0.5, oldCamPos.z-0.5),
                                                pr.Vector3(oldCamPos.x+0.5, oldCamPos.y+0.5, oldCamPos.z+0.5))):
        camera.position = oldCamPos
    
pr.close_window()
